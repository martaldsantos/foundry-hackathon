"""
Challenge 4: Evaluate — SDK Track
Run evaluations against the test dataset using built-in evaluators.

Usage:
    python evaluate.py

Fill in the TODOs to complete the evaluation pipeline.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


# Load environment
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)

PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.1")
EVAL_DATASET_PATH = Path(__file__).resolve().parent.parent / "evaluation_dataset.json"


async def load_dataset() -> list:
    """Load the evaluation dataset."""
    with open(EVAL_DATASET_PATH, "r") as f:
        return json.load(f)


async def run_agent_on_dataset(dataset: list) -> list:
    """Run the anomaly detection agent on each test case and collect responses."""
    from azure.identity.aio import DefaultAzureCredential
    from azure.ai.projects.aio import AIProjectClient

    credential = DefaultAzureCredential()
    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=credential,
    )

    # Create the agent for evaluation
    agent = await client.agents.create_agent(
        model=MODEL_DEPLOYMENT_NAME,
        name="eval-anomaly-agent",
        instructions=(
            "You are an industrial anomaly detection agent. "
            "Analyze sensor readings against thresholds and classify machine status. "
            "Respond with: classification (normal/warning/critical), list of anomalies, "
            "urgency level (low/medium/high), and recommended action."
        ),
    )

    results = []
    print(f"Processing {len(dataset)} test cases...")

    for i, test_case in enumerate(dataset, 1):
        # TODO: For each test case, create a thread, send the input, run the agent,
        # and collect the response.
        #
        # thread = await client.agents.create_thread()
        # await client.agents.create_message(
        #     thread_id=thread.id,
        #     role="user",
        #     content=test_case["input"],
        # )
        # run = await client.agents.create_and_process_run(
        #     thread_id=thread.id,
        #     agent_id=agent.id,
        # )
        #
        # response_text = ""
        # if run.status == "completed":
        #     messages = await client.agents.list_messages(thread_id=thread.id)
        #     for msg in messages.data:
        #         if msg.role == "assistant":
        #             response_text = msg.content[0].text.value
        #             break
        #
        # results.append({
        #     "id": test_case["id"],
        #     "input": test_case["input"],
        #     "expected_output": test_case["expected_output"],
        #     "actual_output": response_text,
        # })
        #
        # classification = test_case["expected_output"]["classification"]
        # print(f"  [{i}/{len(dataset)}] {test_case['id']}: {classification} classification")

        # TODO: Remove this placeholder once you implement the above
        results.append({
            "id": test_case["id"],
            "input": test_case["input"],
            "expected_output": test_case["expected_output"],
            "actual_output": "",  # Will be filled by your implementation
        })
        print(f"  [{i}/{len(dataset)}] {test_case['id']}: (not implemented yet)")

    # Cleanup
    await client.agents.delete_agent(agent.id)
    await credential.close()
    await client.close()

    return results


async def run_evaluators(results: list):
    """Run built-in evaluators on the agent's responses."""
    print("\n=== Running Evaluators ===")

    # TODO: Use the OpenAI evals API to evaluate responses.
    # The pattern is:
    #
    # from azure.identity.aio import DefaultAzureCredential
    # from azure.ai.projects.aio import AIProjectClient
    #
    # credential = DefaultAzureCredential()
    # client = AIProjectClient(
    #     endpoint=PROJECT_CONNECTION_STRING,
    #     credential=credential,
    # )
    #
    # # Get the OpenAI client for evals
    # openai_client = await client.get_openai_client()
    #
    # # Create an evaluation
    # eval_obj = openai_client.evals.create(
    #     name="anomaly-detection-eval",
    #     data_source_config={
    #         "type": "custom",
    #         "item_schema": {
    #             "type": "object",
    #             "properties": {
    #                 "input": {"type": "string"},
    #                 "expected_output": {"type": "string"},
    #                 "actual_output": {"type": "string"},
    #             }
    #         },
    #         "include_sample_schema": True,
    #     },
    #     testing_criteria=[
    #         {
    #             "type": "label_model",
    #             "name": "task_adherence",
    #             "model": MODEL_DEPLOYMENT_NAME,
    #             "input": [
    #                 {"role": "system", "content": "Score 1-5 how well the actual output addresses the task in the input. 5=perfectly addresses it."},
    #                 {"role": "user", "content": "Input: {{item.input}}\nExpected: {{item.expected_output}}\nActual: {{item.actual_output}}"}
    #             ],
    #             "passing_labels": ["4", "5"],
    #             "labels": ["1", "2", "3", "4", "5"],
    #         },
    #         {
    #             "type": "label_model",
    #             "name": "coherence",
    #             "model": MODEL_DEPLOYMENT_NAME,
    #             "input": [
    #                 {"role": "system", "content": "Score 1-5 how coherent and well-structured the response is. 5=perfectly coherent."},
    #                 {"role": "user", "content": "Response: {{item.actual_output}}"}
    #             ],
    #             "passing_labels": ["4", "5"],
    #             "labels": ["1", "2", "3", "4", "5"],
    #         },
    #     ],
    # )
    #
    # # Run the evaluation with your data
    # eval_run = openai_client.evals.runs.create(
    #     eval_id=eval_obj.id,
    #     data_source={
    #         "type": "jsonl",
    #         "source": {
    #             "type": "file_content",
    #             "content": [
    #                 {
    #                     "input": r["input"],
    #                     "expected_output": json.dumps(r["expected_output"]),
    #                     "actual_output": r["actual_output"],
    #                 }
    #                 for r in results
    #             ],
    #         },
    #     },
    # )
    #
    # # Print results
    # print(f"\nEvaluation run: {eval_run.id}")
    # print(f"Status: {eval_run.status}")
    # # Poll until complete, then print metrics
    #
    # await credential.close()
    # await client.close()

    # Placeholder output showing what the results should look like
    print("  (Evaluators not implemented yet — fill in the TODOs)")
    print("\n  When implemented, you'll see:")
    print("  Aggregate Metrics:")
    print("    Task Adherence:  ?.? / 5.0")
    print("    Coherence:       ?.? / 5.0")
    print("\n  Per-Row Scores:")
    for r in results:
        classification = r["expected_output"]["classification"]
        print(f"    {r['id']}: adherence=?, coherence=? — {classification}")


async def main():
    if not PROJECT_CONNECTION_STRING:
        print("❌ PROJECT_CONNECTION_STRING not set. Run challenge 0 first!")
        sys.exit(1)

    print("=== Running Evaluation ===")

    # Step 1: Load dataset
    dataset = await load_dataset()
    print(f"Loaded {len(dataset)} test cases from evaluation_dataset.json")

    # Step 2: Run agent on each test case
    results = await run_agent_on_dataset(dataset)

    # Step 3: Run evaluators
    await run_evaluators(results)

    print("\n🎉 Evaluation complete!")


if __name__ == "__main__":
    asyncio.run(main())
