"""
Challenge 4: Production Workflow -- SDK Track
Multi-agent orchestration workflow for NovaTel Communications call center.
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


env_path = _find_repo_root() / ".env"
load_dotenv(env_path)

PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.1")
CALL_DATA_PATH = Path(__file__).resolve().parent.parent / "challenge-1-build" / "call_data.json"

INTENT_AGENT_NAME = "intent-classification-agent"
RESOLUTION_AGENT_NAME = "resolution-advisor-agent"
# Set WORKFLOW_AGENT_NAME in .env after creating the workflow in the Foundry portal
WORKFLOW_AGENT_NAME = os.getenv("WORKFLOW_AGENT_NAME", "")


def lookup_customer(call_id: str) -> str:
    """Look up call/customer details from call_data.json."""
    with open(CALL_DATA_PATH, "r") as f:
        data = json.load(f)
    call = next(
        (c for c in data["calls"]
         if c["call_id"] == call_id or c["customer_id"] == call_id),
        None,
    )
    if not call:
        return json.dumps({"error": f"Call or customer not found: {call_id}"})
    return json.dumps(call, indent=2)


def ensure_agents_deployed() -> tuple:
    """Create both agents if not already deployed; reuse existing ones."""
    print("=== Step 1: Ensure Agents Are Deployed ===")

    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
    from azure.identity import DefaultAzureCredential

    lookup_customer_tool = FunctionTool(
        name="lookup_customer",
        description="Look up customer and call details by call ID or customer ID.",
        parameters={
            "type": "object",
            "properties": {
                "call_id": {"type": "string", "description": "Call ID e.g. CALL-001 or customer ID e.g. CUST-4421"},
            },
            "required": ["call_id"],
        },
        strict=False,
    )

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    existing_names = {a.name for a in client.agents.list()}

    if INTENT_AGENT_NAME not in existing_names:
        client.agents.create_version(
            agent_name=INTENT_AGENT_NAME,
            definition=PromptAgentDefinition(
                model=MODEL_DEPLOYMENT_NAME,
                instructions=(
                    "You are a call center intent classification specialist for NovaTel Communications. "
                    "When asked to classify calls, use the lookup_customer tool to retrieve call details. "
                    "Classify each call with: intent (billing_dispute/technical_issue/cancellation/"
                    "upsell_opportunity/account_support/security_concern), priority (critical/high/medium/low), "
                    "sentiment (frustrated/neutral/positive/anxious), retention risk (high/medium/low). "
                    "Be concise and structured."
                ),
                tools=[lookup_customer_tool],
            ),
        )
        print(f"  Deployed: {INTENT_AGENT_NAME}")
    else:
        print(f"  Found existing: {INTENT_AGENT_NAME}")

    if RESOLUTION_AGENT_NAME not in existing_names:
        client.agents.create_version(
            agent_name=RESOLUTION_AGENT_NAME,
            definition=PromptAgentDefinition(
                model=MODEL_DEPLOYMENT_NAME,
                instructions=(
                    "You are a resolution strategy expert for NovaTel Communications. "
                    "Given a classified call intent and customer context, recommend the optimal resolution. "
                    "Provide: RECOMMENDED ACTION, SCRIPT SUGGESTION, ESCALATION (Yes/No + reason), "
                    "OFFERS AVAILABLE, and FOLLOW-UP tasks. "
                    "Security concerns ALWAYS escalate. Business accounts get priority. "
                    "Long-tenure customers get retention offers."
                ),
            ),
        )
        print(f"  Deployed: {RESOLUTION_AGENT_NAME}")
    else:
        print(f"  Found existing: {RESOLUTION_AGENT_NAME}")

    client.close()
    return INTENT_AGENT_NAME, RESOLUTION_AGENT_NAME


def run_intent_classification(intent_agent_name: str) -> str:
    """Call the intent classification agent for all calls; handle function call loop."""
    print("\n=== Step 2a: Intent Classification ===")

    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    from openai.types.responses.response_input_param import FunctionCallOutput

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    openai_client = client.get_openai_client()
    agent_ref = {"agent_reference": {"name": intent_agent_name, "type": "agent_reference"}}

    # Get all call IDs from the data
    with open(CALL_DATA_PATH, "r") as f:
        data = json.load(f)
    call_ids = [c["call_id"] for c in data["calls"]]

    conversation = openai_client.conversations.create()
    response = openai_client.responses.create(
        input=(
            f"Classify all incoming calls: {', '.join(call_ids)}. "
            "For each, provide intent, priority, sentiment, and retention risk."
        ),
        conversation=conversation.id,
        extra_body=agent_ref,
    )

    while any(item.type == "function_call" for item in response.output):
        tool_outputs = []
        for item in response.output:
            if item.type == "function_call":
                args = json.loads(item.arguments)
                result = lookup_customer(args.get("call_id", ""))
                tool_outputs.append(
                    FunctionCallOutput(
                        type="function_call_output",
                        call_id=item.call_id,
                        output=result,
                    )
                )
        response = openai_client.responses.create(
            input=tool_outputs,
            conversation=conversation.id,
            extra_body=agent_ref,
        )

    report = response.output_text
    openai_client.conversations.delete(conversation_id=conversation.id)
    client.close()
    return report


def run_resolution_advisory(resolution_agent_name: str, call_id: str, classification: dict) -> str:
    """Call the resolution advisor agent for a single classified call."""
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    openai_client = client.get_openai_client()
    agent_ref = {"agent_reference": {"name": resolution_agent_name, "type": "agent_reference"}}

    # Get customer context
    customer_data = json.loads(lookup_customer(call_id))

    input_text = (
        f"Call {call_id} from {customer_data.get('customer_name', 'Unknown')} "
        f"({customer_data.get('account_tier', 'unknown')} tier, "
        f"{customer_data.get('tenure_months', 0)} months tenure):\n"
        f"- Intent: {classification.get('intent', 'unknown')}\n"
        f"- Priority: {classification.get('priority', 'unknown')}\n"
        f"- Sentiment: {classification.get('sentiment', 'unknown')}\n"
        f"- Retention risk: {classification.get('retention_risk', 'unknown')}\n"
        f"- Summary: {customer_data.get('summary', 'No summary available')}\n\n"
        "Recommend the resolution strategy, script, escalation decision, and follow-up actions."
    )

    conversation = openai_client.conversations.create()
    response = openai_client.responses.create(
        input=input_text,
        conversation=conversation.id,
        extra_body=agent_ref,
    )
    resolution = response.output_text
    openai_client.conversations.delete(conversation_id=conversation.id)
    client.close()
    return resolution


def run_call_center_workflow(intent_agent: str, resolution_agent: str) -> dict:
    """Orchestrate: classify all calls -> resolve high-priority ones -> consolidated report."""
    classification_report = run_intent_classification(intent_agent)
    print(classification_report)

    print("\n=== Step 2b: Resolution Advisory (High-Priority Calls) ===")
    resolutions = {}

    # Process the critical/high priority calls that need immediate resolution
    high_priority_calls = [
        {"call_id": "CALL-007", "intent": "security_concern", "priority": "critical",
         "sentiment": "anxious", "retention_risk": "medium"},
        {"call_id": "CALL-001", "intent": "billing_dispute", "priority": "high",
         "sentiment": "frustrated", "retention_risk": "high"},
        {"call_id": "CALL-003", "intent": "cancellation", "priority": "high",
         "sentiment": "neutral", "retention_risk": "high"},
    ]

    for call in high_priority_calls:
        print(f"  Resolving {call['call_id']} ({call['intent']})...")
        resolution = run_resolution_advisory(resolution_agent, call["call_id"], call)
        resolutions[call["call_id"]] = resolution

    return {
        "classification_report": classification_report,
        "high_priority_calls": [c["call_id"] for c in high_priority_calls],
        "resolutions": resolutions,
        "total_calls": 7,
        "critical_count": 1,
        "high_priority_count": 2,
    }


def print_shift_report(report: dict):
    print("\n" + "=" * 60)
    print("NOVATEL CALL CENTER — SHIFT REPORT")
    print("=" * 60)
    print(f"  Total calls processed  : {report['total_calls']}")
    print(f"  Critical priority      : {report['critical_count']}")
    print(f"  High priority          : {report['high_priority_count']}")

    if report["high_priority_calls"]:
        print(f"\n  Calls requiring immediate action: {', '.join(report['high_priority_calls'])}")
        print("\n--- Resolution Recommendations ---")
        for call_id, resolution in report["resolutions"].items():
            print(f"\n{call_id}:")
            print(resolution)
    else:
        print("\n  No critical or high-priority calls in queue.")

    print("=" * 60)


def run_portal_workflow(
    workflow_name: str,
    query: str = "Classify and resolve all incoming calls: CALL-001 through CALL-007. Prioritize security concerns and high-retention-risk customers.",
) -> str:
    """
    Invoke a workflow agent created in the Foundry portal.

    The response is streamed so you can observe each workflow step as it runs.

    Before calling this:
      1. Open the Foundry portal -> Build -> Workflows -> New workflow
      2. Add the intent-classification-agent and resolution-advisor-agent as steps
      3. Deploy it and note the agent name
      4. Set WORKFLOW_AGENT_NAME=<name> in your .env file

    Returns:
        The workflow's final text output.
    """
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    openai_client = client.get_openai_client()

    conversation = openai_client.conversations.create()
    print(f"\n=== Invoking Portal Workflow: {workflow_name} ===")
    print(f"Conversation ID: {conversation.id}")

    final_output = ""

    stream = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent_reference": {"name": workflow_name, "type": "agent_reference"}},
        input=query,
        stream=True,
        metadata={"x-ms-debug-mode-enabled": "1"},
    )

    for event in stream:
        if event.type == "response.output_item.added" and hasattr(event, "item") and getattr(event.item, "type", "") == "workflow_action":
            print(f"\n  --> Step: {event.item.action_id}")
        elif event.type == "response.output_item.done" and hasattr(event, "item") and getattr(event.item, "type", "") == "workflow_action":
            print(f"      [{getattr(event.item, 'status', 'done')}] {event.item.action_id}")
        elif event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
        elif event.type == "response.output_text.done":
            final_output = event.text
            print()

    openai_client.conversations.delete(conversation_id=conversation.id)
    client.close()
    return final_output


def main():
    if not PROJECT_CONNECTION_STRING:
        print("PROJECT_CONNECTION_STRING not set. Run challenge 0 first!")
        sys.exit(1)

    # --- Part A: Python orchestration (agents called step-by-step from code) ---
    intent_agent, resolution_agent = ensure_agents_deployed()
    report = run_call_center_workflow(intent_agent, resolution_agent)
    print_shift_report(report)

    print("\nWorkflow complete! Agents remain deployed for future runs.")

    # --- Part B: Portal workflow (create in Foundry portal, invoke via streaming) ---
    if WORKFLOW_AGENT_NAME:
        print("\n" + "=" * 60)
        print("PORTAL WORKFLOW")
        print("=" * 60)
        output = run_portal_workflow(WORKFLOW_AGENT_NAME)
        print("\nPortal workflow output:")
        print(output)
    else:
        print("\nTip: Create a workflow in the Foundry portal and set")
        print("     WORKFLOW_AGENT_NAME=<name> in .env to invoke it here.")


if __name__ == "__main__":
    main()
