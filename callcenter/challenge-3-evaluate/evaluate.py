"""
Challenge 3: Evaluate — SDK Track
Run evaluations against the test dataset using built-in evaluators.

Usage:
    python evaluate.py
"""

import json
import os
import sys
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential


def _find_repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists():
            return parent
    return Path(__file__).resolve().parents[2]


# Load environment
env_path = _find_repo_root() / ".env"
load_dotenv(env_path)

PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.1")
FOUNDRY_ENDPOINT = os.getenv("FOUNDRY_ENDPOINT", "")
EVAL_DATASET_PATH = Path(__file__).resolve().parent.parent / "challenge-4-deploy" / "evaluation_dataset.json"
# Use a recent API version compatible with GPT-5.x deployments on the new Foundry endpoint
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2025-01-01-preview")


def load_dataset() -> list:
    """Load the evaluation dataset."""
    with open(EVAL_DATASET_PATH, "r") as f:
        return json.load(f)


def run_agent_on_dataset(dataset: list) -> list:
    """Run the intent classification agent on each test case and collect responses."""
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import PromptAgentDefinition

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    openai_client = client.get_openai_client()

    agent = client.agents.create_version(
        agent_name="eval-intent-agent",
        definition=PromptAgentDefinition(
            model=MODEL_DEPLOYMENT_NAME,
            instructions=(
                "You are a call center intent classification agent. "
                "Analyze the call summary and classify it. "
                "Respond with: intent category (billing_dispute/technical_issue/cancellation/"
                "upsell_opportunity/account_support/security_concern), priority (critical/high/medium/low), "
                "sentiment (frustrated/neutral/positive/anxious), retention risk (high/medium/low), "
                "and recommended action summary."
            ),
        ),
    )

    results = []
    print(f"Processing {len(dataset)} test cases...")

    for i, test_case in enumerate(dataset, 1):
        try:
            conversation = openai_client.conversations.create()
            response = openai_client.responses.create(
                input=test_case["input"],
                conversation=conversation.id,
                extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
            )
            response_text = response.output_text
            openai_client.conversations.delete(conversation_id=conversation.id)
        except Exception as exc:
            print(f"  [{i}/{len(dataset)}] {test_case['id']}: agent call failed — {exc}")
            response_text = ""

        results.append({
            "id": test_case["id"],
            "input": test_case["input"],
            "expected_output": test_case["expected_output"],
            "actual_output": response_text,
        })
        intent = test_case["expected_output"]["intent"]
        print(f"  [{i}/{len(dataset)}] {test_case['id']}: {intent}")

    client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
    client.close()

    return results


def run_evaluators(results: list):
    """
    Run built-in LLM-as-judge evaluators using the azure-ai-evaluation SDK.
    Results are uploaded to the Foundry portal (Evaluation tab) automatically.
    """
    print("\n=== Running Evaluators ===")

    from azure.ai.evaluation import (
        AzureOpenAIModelConfiguration,
        CoherenceEvaluator,
        RelevanceEvaluator,
        evaluate,
    )
    # On Python 3.13, isinstance(v, typing.Any) raises TypeError inside validate_model_config,
    # so passing credential= inside AzureOpenAIModelConfiguration is broken.
    # Work-around: keep model_config credential-free; pass credential= directly to each
    # evaluator constructor — it routes through AsyncPrompty.token_credential and bypasses
    # validate_model_config entirely.
    credential = DefaultAzureCredential()
    model_config = AzureOpenAIModelConfiguration(
        azure_endpoint=FOUNDRY_ENDPOINT,
        azure_deployment=MODEL_DEPLOYMENT_NAME,
        api_version=OPENAI_API_VERSION,
    )

    eval_data = [
        {"query": r["input"], "response": r["actual_output"]}
        for r in results
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as temp_data_file:
        for item in eval_data:
            temp_data_file.write(json.dumps(item) + "\n")
        eval_data_path = temp_data_file.name

    # Pass as string → SDK uses the new AI Foundry (OneDP) upload path
    azure_ai_project = PROJECT_CONNECTION_STRING

    print(f"Evaluating {len(eval_data)} responses with CoherenceEvaluator + RelevanceEvaluator...")
    result = None
    try:
        result = evaluate(
            data=eval_data_path,
            evaluators={
                "coherence": CoherenceEvaluator(model_config, credential=credential, is_reasoning_model=True),
                "relevance": RelevanceEvaluator(model_config, credential=credential, is_reasoning_model=True),
            },
            azure_ai_project=azure_ai_project,
            evaluation_name="call-center-intent-evaluation",
            credential=credential,
        )
    except Exception as exc:
        print(f"\n❌ evaluate() failed: {exc}")
        raise
    finally:
        try:
            os.remove(eval_data_path)
        except OSError:
            pass

    studio_url = result.get("studio_url") if result else None
    if studio_url:
        print(f"\nResults visible in Foundry portal:")
        print(f"  {studio_url}")
    else:
        print(
            "\nEvaluation uploaded. Open the Foundry portal → Evaluation tab "
            "and look for: 'call-center-intent-evaluation'"
        )

    metrics = result.get("metrics", {})
    if metrics:
        print("\nMetrics summary:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.2f}" if isinstance(v, float) else f"  {k}: {v}")


def main():
    if not PROJECT_CONNECTION_STRING:
        print("❌ PROJECT_CONNECTION_STRING not set. Run challenge 0 first!")
        sys.exit(1)

    print("=== Running Evaluation ===")

    dataset = load_dataset()
    print(f"Loaded {len(dataset)} test cases from evaluation_dataset.json")

    results = run_agent_on_dataset(dataset)
    run_evaluators(results)

    print("\n🎉 Evaluation complete!")


if __name__ == "__main__":
    main()
