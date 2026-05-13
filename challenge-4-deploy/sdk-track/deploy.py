"""
Challenge 4: Production Workflow — SDK Track
Build a multi-agent orchestration workflow for TireForge Industries.

The workflow:
  1. Ensure both agents are deployed as persistent production assets.
  2. Run the factory health workflow:
       Anomaly Detection Agent  ->  scans all 5 machines
             | (for each machine with anomalies)
             v
       Fault Diagnosis Agent    ->  diagnoses root cause
             |
             v
       Consolidated Factory Health Report
  3. Print the report.

Usage:
    python deploy.py

Fill in the TODOs to complete the workflow.
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
    return Path(__file__).resolve().parents[3]


env_path = _find_repo_root() / ".env"
load_dotenv(env_path)

PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.1")
SENSOR_DATA_PATH = _find_repo_root() / "challenge-1-build" / "sensor_data.json"

MACHINES = ["MX-001", "EX-002", "CP-003", "CU-004", "IS-005"]
ANOMALY_AGENT_NAME = "anomaly-detection-agent"
DIAGNOSIS_AGENT_NAME = "fault-diagnosis-agent"
# Set WORKFLOW_AGENT_NAME in .env after creating the workflow in the Foundry portal
WORKFLOW_AGENT_NAME = os.getenv("WORKFLOW_AGENT_NAME", "")


# ---------------------------------------------------------------------------
# Tool: check_thresholds (called locally when the anomaly agent invokes it)
# ---------------------------------------------------------------------------

def check_thresholds(machine_id: str) -> str:
    """Read sensor_data.json and check a machine's readings against thresholds."""
    with open(SENSOR_DATA_PATH, "r") as f:
        data = json.load(f)

    machine = next(
        (m for m in data["machines"]
         if m["machine_id"] == machine_id or m["name"] == machine_id),
        None,
    )
    if not machine:
        return json.dumps({"error": f"Machine '{machine_id}' not found"})

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
            "value": value,
            "unit": reading["unit"],
            "min": threshold["min"],
            "max": threshold["max"],
            "in_spec": in_spec,
        }
        if not in_spec:
            direction = "above max" if value > threshold["max"] else "below min"
            ref = threshold["max"] if value > threshold["max"] else threshold["min"]
            pct = abs(value - ref) / ref * 100
            results["anomalies"].append({
                "sensor": sensor,
                "value": value,
                "unit": reading["unit"],
                "deviation": f"{pct:.1f}% {direction}",
            })

    return json.dumps(results, indent=2)


# ---------------------------------------------------------------------------
# Step 1: Ensure production agents exist
# ---------------------------------------------------------------------------

def ensure_agents_deployed() -> tuple:
    """
    Create both agents as persistent versioned assets if they don't already exist.
    If they're already deployed, reuse them — no duplicate versions created.

    Returns:
        (anomaly_agent_name, diagnosis_agent_name)
    """
    print("=== Step 1: Ensure Agents Are Deployed ===")

    # TODO: Import AIProjectClient, FunctionTool, PromptAgentDefinition,
    # and DefaultAzureCredential.
    #
    # 1. Create the client and list existing agents:
    #    existing_names = {a.name for a in client.agents.list()}
    #
    # 2. If ANOMALY_AGENT_NAME is not in existing_names, create it with
    #    create_version() including the check_thresholds FunctionTool.
    #    Print "Deployed: <name>" or "Found existing: <name>".
    #
    # 3. Do the same for DIAGNOSIS_AGENT_NAME (no tools needed).
    #
    # 4. Close the client and return (ANOMALY_AGENT_NAME, DIAGNOSIS_AGENT_NAME).

    print("  (not implemented yet -- fill in the TODO)")
    return ANOMALY_AGENT_NAME, DIAGNOSIS_AGENT_NAME


# ---------------------------------------------------------------------------
# Step 2a: Anomaly scan
# ---------------------------------------------------------------------------

def run_anomaly_scan(anomaly_agent_name: str) -> str:
    """
    Call the anomaly detection agent for all machines.
    The agent will invoke check_thresholds for each machine -- handle the
    function call loop and return the agent's final text response.
    """
    print("\n=== Step 2a: Anomaly Scan ===")

    # TODO: Get the openai client and run the anomaly agent with input:
    #   "Check all machines: MX-001, EX-002, CP-003, CU-004, IS-005.
    #    Report every sensor reading that is out of spec."
    #
    # Handle the function call loop:
    #   while any item.type == "function_call" in response.output:
    #       call check_thresholds(machine_id) for each function_call item
    #       submit results as FunctionCallOutput back to the conversation
    #
    # from openai.types.responses.response_input_param import FunctionCallOutput
    #
    # Return response.output_text after the loop ends.

    print("  (not implemented yet -- fill in the TODO)")
    return ""


# ---------------------------------------------------------------------------
# Step 2b: Fault diagnosis per affected machine
# ---------------------------------------------------------------------------

def run_fault_diagnosis(diagnosis_agent_name: str, machine_id: str, anomalies: list) -> str:
    """
    Call the fault diagnosis agent for a single machine.

    Args:
        diagnosis_agent_name: Name of the deployed diagnosis agent.
        machine_id: The machine to diagnose (e.g. 'CP-003').
        anomalies: List of anomaly dicts from check_thresholds().

    Returns:
        The agent's diagnosis (LIKELY CAUSE / MAINTENANCE ACTIONS / URGENCY).
    """
    # TODO: Build an input message describing the machine's anomalies and
    # call the fault-diagnosis-agent via a new conversation.
    # No function call loop needed -- this agent has no tools.
    # Return response.output_text.

    return ""


# ---------------------------------------------------------------------------
# Step 3: Orchestrate the full workflow
# ---------------------------------------------------------------------------

def run_factory_health_workflow(anomaly_agent: str, diagnosis_agent: str) -> dict:
    """
    Orchestrate the full factory health workflow:
      1. Run anomaly scan across all machines.
      2. Use check_thresholds locally to find which machines have anomalies.
      3. For each affected machine, run fault diagnosis.
      4. Return a consolidated report dict.
    """
    # TODO: Call run_anomaly_scan() to get the anomaly report text.
    # Then iterate over MACHINES, calling check_thresholds() locally for each
    # to find machines where len(result["anomalies"]) > 0.
    # For each affected machine, call run_fault_diagnosis().
    # Return a dict with keys:
    #   "anomaly_report", "machines_with_anomalies", "diagnoses",
    #   "total_machines", "problematic_machines"

    return {
        "anomaly_report": "",
        "machines_with_anomalies": [],
        "diagnoses": {},
        "total_machines": len(MACHINES),
        "problematic_machines": 0,
    }


# ---------------------------------------------------------------------------
# Bonus: Invoke a workflow agent created in the Foundry portal
# ---------------------------------------------------------------------------

def run_portal_workflow(
    workflow_name: str,
    query: str = "Run the factory health check on all machines: MX-001, EX-002, CP-003, CU-004, IS-005.",
) -> str:
    """
    Invoke a workflow agent created in the Foundry portal.

    Before calling this:
      1. Open the Foundry portal -> Build -> Workflows -> New workflow
      2. Add the anomaly-detection-agent and fault-diagnosis-agent as steps
      3. Deploy it and note the agent name
      4. Set WORKFLOW_AGENT_NAME=<name> in your .env file

    The response is streamed -- workflow_action events mark each pipeline step.
    """
    # TODO: Create a conversation and stream the response from the workflow agent.
    #
    # Use openai_client.responses.create() with:
    #   stream=True
    #   extra_body={"agent_reference": {"name": workflow_name, "type": "agent_reference"}}
    #   metadata={"x-ms-debug-mode-enabled": "1"}
    #
    # In the event loop, handle:
    #   event.type == "response.output_item.added"  and  event.item.type == "workflow_action"
    #       -> print the step name: event.item.action_id
    #   event.type == "response.output_item.done"   and  event.item.type == "workflow_action"
    #       -> print the step status: event.item.status
    #   event.type == "response.output_text.delta"
    #       -> print streaming text: event.delta
    #   event.type == "response.output_text.done"
    #       -> capture final output: event.text
    #
    # Return the final output text.

    # TODO: Remove placeholder
    return ""


# ---------------------------------------------------------------------------
# Report printer (already implemented)
# ---------------------------------------------------------------------------

def print_factory_report(report: dict):
    """Print the consolidated factory health report."""
    print("\n" + "=" * 60)
    print("TIREFORGE FACTORY HEALTH REPORT")
    print("=" * 60)
    print(f"  Machines checked   : {report['total_machines']}")
    print(f"  Machines affected  : {report['problematic_machines']}")

    if report["machines_with_anomalies"]:
        print(f"  Affected machines  : {', '.join(report['machines_with_anomalies'])}")
        print("\n--- Anomaly Summary ---")
        print(report["anomaly_report"])
        print("\n--- Fault Diagnoses ---")
        for machine_id, diagnosis in report["diagnoses"].items():
            print(f"\n{machine_id}:")
            print(diagnosis)
    else:
        print("\n  All machines operating within normal parameters.")

    print("=" * 60)


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
        output = run_portal_workflow(WORKFLOW_AGENT_NAME)
        print("\nPortal workflow output:")
        print(output)
    else:
        print("\nTip: Create a workflow in the Foundry portal and set")
        print("     WORKFLOW_AGENT_NAME=<name> in .env to invoke it here.")


if __name__ == "__main__":
    main()
