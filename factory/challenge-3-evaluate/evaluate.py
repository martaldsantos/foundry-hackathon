"""
Challenge 3: Evaluate — SDK Track
Run evaluations against the test dataset using built-in evaluators.

Usage:
    python evaluate.py
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


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
AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID", "")
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP", "foundry-hackathon-rg")
PROJECT_NAME = os.getenv("PROJECT_NAME", "tire-factory-project")
EVAL_DATASET_PATH = Path(__file__).resolve().parent.parent / "challenge-4-deploy" / "evaluation_dataset.json"


def load_dataset() -> list:
    """Load the evaluation dataset."""
    with open(EVAL_DATASET_PATH, "r") as f:
        return json.load(f)


def run_agent_on_dataset(dataset: list) -> list:
    """Run the anomaly detection agent on each test case and collect responses."""
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import PromptAgentDefinition
    from azure.identity import DefaultAzureCredential

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    openai_client = client.get_openai_client()

    agent = client.agents.create_version(
        agent_name="eval-anomaly-agent",
        definition=PromptAgentDefinition(
            model=MODEL_DEPLOYMENT_NAME,
            instructions=(
                "You are an industrial anomaly detection agent. "
                "Analyze sensor readings against thresholds and classify machine status. "
                "Respond with: classification (normal/warning/critical), list of anomalies, "
                "urgency level (low/medium/high), and recommended action."
            ),
        ),
    )

    results = []
    print(f"Processing {len(dataset)} test cases...")

    for i, test_case in enumerate(dataset, 1):
        conversation = openai_client.conversations.create()
        response = openai_client.responses.create(
            input=test_case["input"],
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
        )
        response_text = response.output_text
        openai_client.conversations.delete(conversation_id=conversation.id)

        results.append({
            "id": test_case["id"],
            "input": test_case["input"],
            "expected_output": test_case["expected_output"],
            "actual_output": response_text,
        })
        classification = test_case["expected_output"]["classification"]
        print(f"  [{i}/{len(dataset)}] {test_case['id']}: {classification} classification")

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
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider

    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    )

    model_config = AzureOpenAIModelConfiguration(
        azure_endpoint=FOUNDRY_ENDPOINT,
        azure_deployment=MODEL_DEPLOYMENT_NAME,
        azure_ad_token_provider=token_provider,
    )

    eval_data = [
        {"query": r["input"], "response": r["actual_output"]}
        for r in results
    ]

    azure_ai_project = {
        "subscription_id": AZURE_SUBSCRIPTION_ID,
        "resource_group_name": RESOURCE_GROUP,
        "project_name": PROJECT_NAME,
    }

    print(f"Evaluating {len(eval_data)} responses with CoherenceEvaluator + RelevanceEvaluator...")
    result = evaluate(
        data=eval_data,
        evaluators={
            "coherence": CoherenceEvaluator(model_config),
            "relevance": RelevanceEvaluator(model_config),
        },
        azure_ai_project=azure_ai_project,
        evaluation_name="anomaly-detection-evaluation",
    )

    studio_url = result.get("studio_url")
    if studio_url:
        print(f"\nResults visible in Foundry portal:")
        print(f"  {studio_url}")
    else:
        print("\nEvaluation complete. Navigate to Foundry portal -> Evaluation tab.")

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
