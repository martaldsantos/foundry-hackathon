"""
Challenge 4: Production Workflow -- SDK Track
Multi-agent orchestration workflow for TireForge Industries.
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
SENSOR_DATA_PATH = Path(__file__).resolve().parent.parent / "challenge-1-build" / "sensor_data.json"

MACHINES = ["MX-001", "EX-002", "CP-003", "CU-004", "IS-005"]
ANOMALY_AGENT_NAME = "anomaly-detection-agent"
DIAGNOSIS_AGENT_NAME = "fault-diagnosis-agent"
# Set WORKFLOW_AGENT_NAME in .env after creating the workflow in the Foundry portal
WORKFLOW_AGENT_NAME = os.getenv("WORKFLOW_AGENT_NAME", "")


def check_thresholds(machine_id: str) -> str:
    with open(SENSOR_DATA_PATH, "r") as f:
        data = json.load(f)
    machine = next(
        (m for m in data["machines"]
         if m["machine_id"] == machine_id or m["name"] == machine_id),
        None,
    )
    if not machine:
        return json.dumps({"error": f"Machine not found: {machine_id}"})
    results = {
        "machine_id": machine["machine_id"],
        "name": machine["name"],
        "status": machine["status"],
        "anomalies": [],
        "all_readings": {},
    }
    for sensor, reading in machine["readings"].items():
        value = reading["value"]
        threshold = machine["thresholds"][sensor]
        in_spec = threshold["min"] <= value <= threshold["max"]
        results["all_readings"][sensor] = {
            "value": value, "unit": reading["unit"],
            "min": threshold["min"], "max": threshold["max"], "in_spec": in_spec,
        }
        if not in_spec:
            direction = "above max" if value > threshold["max"] else "below min"
            ref = threshold["max"] if value > threshold["max"] else threshold["min"]
            pct = abs(value - ref) / ref * 100
            results["anomalies"].append({
                "sensor": sensor, "value": value,
                "unit": reading["unit"], "deviation": f"{pct:.1f}% {direction}",
            })
    return json.dumps(results, indent=2)


def ensure_agents_deployed() -> tuple:
    """Create both agents if not already deployed; reuse existing ones."""
    print("=== Step 1: Ensure Agents Are Deployed ===")

    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
    from azure.identity import DefaultAzureCredential

    check_thresholds_tool = FunctionTool(
        name="check_thresholds",
        description="Check sensor readings against thresholds for a given machine.",
        parameters={
            "type": "object",
            "properties": {
                "machine_id": {"type": "string", "description": "Machine ID e.g. MX-001"},
            },
            "required": ["machine_id"],
        },
        strict=False,
    )

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    existing_names = {a.name for a in client.agents.list()}

    if ANOMALY_AGENT_NAME not in existing_names:
        client.agents.create_version(
            agent_name=ANOMALY_AGENT_NAME,
            definition=PromptAgentDefinition(
                model=MODEL_DEPLOYMENT_NAME,
                instructions=(
                    "You are an industrial sensor anomaly detection expert for TireForge Industries. "
                    "When asked to check machines, use the check_thresholds tool for each machine ID. "
                    "Report every sensor reading that is out of spec: machine name, sensor, current value, "
                    "threshold violated, and deviation percentage. "
                    "Use WARNING or CRITICAL labels. Be concise and structured."
                ),
                tools=[check_thresholds_tool],
            ),
        )
        print(f"  Deployed: {ANOMALY_AGENT_NAME}")
    else:
        print(f"  Found existing: {ANOMALY_AGENT_NAME}")

    if DIAGNOSIS_AGENT_NAME not in existing_names:
        client.agents.create_version(
            agent_name=DIAGNOSIS_AGENT_NAME,
            definition=PromptAgentDefinition(
                model=MODEL_DEPLOYMENT_NAME,
                instructions=(
                    "You are a mechanical fault diagnosis expert for TireForge Industries. "
                    "Given anomalies from a machine, identify the most likely root cause and recommend "
                    "specific maintenance actions. Estimate urgency: IMMEDIATE, WITHIN 24H, or MONITOR. "
                    "Format: LIKELY CAUSE: ... / MAINTENANCE ACTIONS: ... / URGENCY: ..."
                ),
            ),
        )
        print(f"  Deployed: {DIAGNOSIS_AGENT_NAME}")
    else:
        print(f"  Found existing: {DIAGNOSIS_AGENT_NAME}")

    client.close()
    return ANOMALY_AGENT_NAME, DIAGNOSIS_AGENT_NAME


def run_anomaly_scan(anomaly_agent_name: str) -> str:
    """Call the anomaly detection agent for all machines; handle function call loop."""
    print("\n=== Step 2a: Anomaly Scan ===")

    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    from openai.types.responses.response_input_param import FunctionCallOutput

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    openai_client = client.get_openai_client()
    agent_ref = {"agent_reference": {"name": anomaly_agent_name, "type": "agent_reference"}}

    conversation = openai_client.conversations.create()
    response = openai_client.responses.create(
        input=(
            f"Check all machines: {', '.join(MACHINES)}. "
            "Report every sensor reading that is out of spec."
        ),
        conversation=conversation.id,
        extra_body=agent_ref,
    )

    while any(item.type == "function_call" for item in response.output):
        tool_outputs = []
        for item in response.output:
            if item.type == "function_call":
                args = json.loads(item.arguments)
                result = check_thresholds(args.get("machine_id", ""))
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


def run_fault_diagnosis(diagnosis_agent_name: str, machine_id: str, anomalies: list) -> str:
    """Call the fault diagnosis agent for a single machine."""
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    openai_client = client.get_openai_client()
    agent_ref = {"agent_reference": {"name": diagnosis_agent_name, "type": "agent_reference"}}

    anomaly_text = "\n".join(
        f"  - {a['sensor']}: {a['value']} {a['unit']} ({a['deviation']})"
        for a in anomalies
    )
    input_text = (
        f"Machine {machine_id} has the following out-of-spec readings:\n"
        f"{anomaly_text}\n"
        "Diagnose the fault and recommend maintenance actions."
    )

    conversation = openai_client.conversations.create()
    response = openai_client.responses.create(
        input=input_text,
        conversation=conversation.id,
        extra_body=agent_ref,
    )
    diagnosis = response.output_text
    openai_client.conversations.delete(conversation_id=conversation.id)
    client.close()
    return diagnosis


def run_factory_health_workflow(anomaly_agent: str, diagnosis_agent: str) -> dict:
    """Orchestrate: anomaly scan -> per-machine diagnosis -> consolidated report."""
    anomaly_report = run_anomaly_scan(anomaly_agent)
    print(anomaly_report)

    print("\n=== Step 2b: Fault Diagnosis ===")
    diagnoses = {}
    machines_with_anomalies = []

    for machine_id in MACHINES:
        result = json.loads(check_thresholds(machine_id))
        if result.get("anomalies"):
            machines_with_anomalies.append(machine_id)
            print(f"  Diagnosing {machine_id}...")
            diagnosis = run_fault_diagnosis(diagnosis_agent, machine_id, result["anomalies"])
            diagnoses[machine_id] = diagnosis

    return {
        "anomaly_report": anomaly_report,
        "machines_with_anomalies": machines_with_anomalies,
        "diagnoses": diagnoses,
        "total_machines": len(MACHINES),
        "problematic_machines": len(machines_with_anomalies),
    }


def print_factory_report(report: dict):
    print("\n" + "=" * 60)
    print("TIREFORGE FACTORY HEALTH REPORT")
    print("=" * 60)
    print(f"  Machines checked   : {report['total_machines']}")
    print(f"  Machines affected  : {report['problematic_machines']}")

    if report["machines_with_anomalies"]:
        print(f"  Affected machines  : {', '.join(report['machines_with_anomalies'])}")
        print("\n--- Fault Diagnoses ---")
        for machine_id, diagnosis in report["diagnoses"].items():
            print(f"\n{machine_id}:")
            print(diagnosis)
    else:
        print("\n  All machines operating within normal parameters.")

    print("=" * 60)


def run_portal_workflow(
    workflow_name: str,
    query: str = "Run the factory health check on all machines: MX-001, EX-002, CP-003, CU-004, IS-005.",
) -> str:
    """
    Invoke a workflow agent created in the Foundry portal.

    The response is streamed so you can observe each workflow step as it runs.
    workflow_action events mark the start and end of each step in the pipeline.

    Before calling this:
      1. Open the Foundry portal -> Build -> Workflows -> New workflow
      2. Add the anomaly-detection-agent and fault-diagnosis-agent as steps
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
    anomaly_agent, diagnosis_agent = ensure_agents_deployed()
    report = run_factory_health_workflow(anomaly_agent, diagnosis_agent)
    print_factory_report(report)

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
