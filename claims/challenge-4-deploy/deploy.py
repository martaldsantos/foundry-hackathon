"""
Challenge 4: Production Workflow — Claims Processing
Multi-agent orchestration workflow for ClaimSight Insurance.
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
CLAIMS_DATA_PATH = Path(__file__).resolve().parent.parent / "challenge-1-build" / "claims_data.json"

CLAIMS = ["CLM-001", "CLM-002", "CLM-003", "CLM-004", "CLM-005"]
TRIAGE_AGENT_NAME = "claims-triage-agent"
DECISION_AGENT_NAME = "claims-decision-agent"
# Set WORKFLOW_AGENT_NAME in .env after creating the workflow in the Foundry portal
WORKFLOW_AGENT_NAME = os.getenv("WORKFLOW_AGENT_NAME", "")


def assess_claim(claim_id: str) -> str:
    with open(CLAIMS_DATA_PATH, "r") as f:
        data = json.load(f)
    claim = next(
        (c for c in data["claims"] if c["claim_id"] == claim_id),
        None,
    )
    if not claim:
        return json.dumps({"error": f"Claim not found: {claim_id}"})
    results = {
        "claim_id": claim["claim_id"],
        "type": claim["type"],
        "claimant": claim["claimant"],
        "status": claim["status"],
        "documents_submitted": claim["documents_submitted"],
        "flags": [],
        "all_metrics": {},
    }
    for metric, reading in claim["metrics"].items():
        value = reading["value"]
        threshold = claim["thresholds"][metric]
        in_spec = threshold["min"] <= value <= threshold["max"]
        results["all_metrics"][metric] = {
            "value": value, "unit": reading["unit"],
            "min": threshold["min"], "max": threshold["max"], "in_spec": in_spec,
        }
        if not in_spec:
            if value > threshold["max"]:
                pct = ((value - threshold["max"]) / threshold["max"]) * 100
                deviation = f"{pct:.1f}% above max"
            else:
                pct = ((threshold["min"] - value) / threshold["min"]) * 100
                deviation = f"{pct:.1f}% below min"
            results["flags"].append({
                "metric": metric, "value": value,
                "unit": reading["unit"], "deviation": deviation,
            })
    return json.dumps(results, indent=2)


def ensure_agents_deployed() -> tuple:
    """Create both agents if not already deployed; reuse existing ones."""
    print("=== Step 1: Ensure Agents Are Deployed ===")

    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
    from azure.identity import DefaultAzureCredential

    assess_claim_tool = FunctionTool(
        name="assess_claim",
        description="Assess an insurance claim's metrics against thresholds.",
        parameters={
            "type": "object",
            "properties": {
                "claim_id": {"type": "string", "description": "Claim ID e.g. CLM-001"},
            },
            "required": ["claim_id"],
        },
        strict=False,
    )

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    existing_names = {a.name for a in client.agents.list()}

    if TRIAGE_AGENT_NAME not in existing_names:
        client.agents.create_version(
            agent_name=TRIAGE_AGENT_NAME,
            definition=PromptAgentDefinition(
                model=MODEL_DEPLOYMENT_NAME,
                instructions=(
                    "You are an insurance claims triage specialist for ClaimSight Insurance. "
                    "When asked to assess claims, use the assess_claim tool for each claim ID. "
                    "Report every metric that is flagged: claim ID, metric name, current value, "
                    "threshold violated, and deviation. "
                    "Use WARNING or CRITICAL labels. Be concise and structured."
                ),
                tools=[assess_claim_tool],
            ),
        )
        print(f"  Deployed: {TRIAGE_AGENT_NAME}")
    else:
        print(f"  Found existing: {TRIAGE_AGENT_NAME}")

    if DECISION_AGENT_NAME not in existing_names:
        client.agents.create_version(
            agent_name=DECISION_AGENT_NAME,
            definition=PromptAgentDefinition(
                model=MODEL_DEPLOYMENT_NAME,
                instructions=(
                    "You are a senior claims adjuster for ClaimSight Insurance. "
                    "Given flags from a claim assessment, recommend an action: "
                    "APPROVE, REQUEST DOCUMENTS, INVESTIGATE, or DENY. "
                    "Provide reasoning and estimate urgency: IMMEDIATE, WITHIN 48H, or STANDARD. "
                    "Format: RECOMMENDED ACTION: ... / REASONING: ... / NEXT STEPS: ... / URGENCY: ..."
                ),
            ),
        )
        print(f"  Deployed: {DECISION_AGENT_NAME}")
    else:
        print(f"  Found existing: {DECISION_AGENT_NAME}")

    client.close()
    return TRIAGE_AGENT_NAME, DECISION_AGENT_NAME


def run_claims_triage(triage_agent_name: str) -> str:
    """Call the claims triage agent for all claims; handle function call loop."""
    print("\n=== Step 2a: Claims Triage ===")

    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    from openai.types.responses.response_input_param import FunctionCallOutput

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    openai_client = client.get_openai_client()
    agent_ref = {"agent_reference": {"name": triage_agent_name, "type": "agent_reference"}}

    conversation = openai_client.conversations.create()
    response = openai_client.responses.create(
        input=(
            f"Assess all claims: {', '.join(CLAIMS)}. "
            "Report every metric that is outside acceptable thresholds."
        ),
        conversation=conversation.id,
        extra_body=agent_ref,
    )

    while any(item.type == "function_call" for item in response.output):
        tool_outputs = []
        for item in response.output:
            if item.type == "function_call":
                args = json.loads(item.arguments)
                result = assess_claim(args.get("claim_id", ""))
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


def run_claims_decision(decision_agent_name: str, claim_id: str, flags: list) -> str:
    """Call the claims decision agent for a single flagged claim."""
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    openai_client = client.get_openai_client()
    agent_ref = {"agent_reference": {"name": decision_agent_name, "type": "agent_reference"}}

    flag_text = "\n".join(
        f"  - {f['metric']}: {f['value']} {f['unit']} ({f['deviation']})"
        for f in flags
    )
    input_text = (
        f"Claim {claim_id} has the following flags:\n"
        f"{flag_text}\n"
        "Recommend an action and provide next steps."
    )

    conversation = openai_client.conversations.create()
    response = openai_client.responses.create(
        input=input_text,
        conversation=conversation.id,
        extra_body=agent_ref,
    )
    decision = response.output_text
    openai_client.conversations.delete(conversation_id=conversation.id)
    client.close()
    return decision


def run_claims_workflow(triage_agent: str, decision_agent: str) -> dict:
    """Orchestrate: triage all claims -> per-claim decision -> consolidated report."""
    triage_report = run_claims_triage(triage_agent)
    print(triage_report)

    print("\n=== Step 2b: Claims Decisions ===")
    decisions = {}
    flagged_claims = []

    for claim_id in CLAIMS:
        result = json.loads(assess_claim(claim_id))
        if result.get("flags"):
            flagged_claims.append(claim_id)
            print(f"  Deciding on {claim_id}...")
            decision = run_claims_decision(decision_agent, claim_id, result["flags"])
            decisions[claim_id] = decision

    return {
        "triage_report": triage_report,
        "flagged_claims": flagged_claims,
        "decisions": decisions,
        "total_claims": len(CLAIMS),
        "problematic_claims": len(flagged_claims),
    }


def print_claims_report(report: dict):
    print("\n" + "=" * 60)
    print("CLAIMSIGHT INSURANCE — CLAIMS PROCESSING REPORT")
    print("=" * 60)
    print(f"  Claims assessed    : {report['total_claims']}")
    print(f"  Claims flagged     : {report['problematic_claims']}")

    if report["flagged_claims"]:
        print(f"  Flagged claims     : {', '.join(report['flagged_claims'])}")
        print("\n--- Decisions ---")
        for claim_id, decision in report["decisions"].items():
            print(f"\n{claim_id}:")
            print(decision)
    else:
        print("\n  All claims passed triage — no flags detected.")

    print("=" * 60)


def run_portal_workflow(
    workflow_name: str,
    query: str = "Process all insurance claims: CLM-001, CLM-002, CLM-003, CLM-004, CLM-005.",
) -> str:
    """
    Invoke a workflow agent created in the Foundry portal.

    The response is streamed so you can observe each workflow step as it runs.

    Before calling this:
      1. Open the Foundry portal -> Build -> Workflows -> New workflow
      2. Add the claims-triage-agent and claims-decision-agent as steps
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
            print()  # newline after streamed text

    openai_client.conversations.delete(conversation_id=conversation.id)
    client.close()
    return final_output


def main():
    if not PROJECT_CONNECTION_STRING:
        print("PROJECT_CONNECTION_STRING not set. Run challenge 0 first!")
        sys.exit(1)

    # --- Part A: Python orchestration (agents called step-by-step from code) ---
    triage_agent, decision_agent = ensure_agents_deployed()
    report = run_claims_workflow(triage_agent, decision_agent)
    print_claims_report(report)

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
