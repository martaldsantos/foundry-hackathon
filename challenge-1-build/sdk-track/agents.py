"""
Challenge 1: Build Agents — SDK Track
Anomaly Detection Agent and Fault Diagnosis Agent for TireForge Industries.

Usage:
    python agents.py

Fill in the TODOs to complete both agents.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


# Load environment
env_path = Path(__file__).resolve().parent.parent.parent / "challenge-0-setup" / ".env"
load_dotenv(env_path)

PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.1")
SENSOR_DATA_PATH = Path(__file__).resolve().parent.parent / "sensor_data.json"


# =============================================================================
# Tool Function: check_thresholds
# This is already implemented — agents can call this to get threshold analysis
# =============================================================================

def check_thresholds(machine_id: str) -> str:
    """
    Reads sensor_data.json and checks if a machine's readings are within thresholds.
    Returns a JSON string with the analysis.
    """
    with open(SENSOR_DATA_PATH, "r") as f:
        data = json.load(f)

    machine = None
    for m in data["machines"]:
        if m["machine_id"] == machine_id or m["name"] == machine_id:
            machine = m
            break

    if not machine:
        return json.dumps({"error": f"Machine '{machine_id}' not found"})

    results = {
        "machine_id": machine["machine_id"],
        "name": machine["name"],
        "status": machine["status"],
        "last_maintenance": machine["last_maintenance"],
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
            deviation = ""
            if value > threshold["max"]:
                pct = ((value - threshold["max"]) / threshold["max"]) * 100
                deviation = f"{pct:.1f}% above max"
            elif value < threshold["min"]:
                pct = ((threshold["min"] - value) / threshold["min"]) * 100
                deviation = f"{pct:.1f}% below min"

            results["anomalies"].append({
                "sensor": sensor,
                "value": value,
                "unit": reading["unit"],
                "threshold_min": threshold["min"],
                "threshold_max": threshold["max"],
                "deviation": deviation,
            })

    return json.dumps(results, indent=2)


# Tool definition for the agent (OpenAI function-calling format)
CHECK_THRESHOLDS_TOOL = {
    "type": "function",
    "function": {
        "name": "check_thresholds",
        "description": "Check if a machine's sensor readings are within normal operating thresholds. Returns anomalies if any readings are out of spec.",
        "parameters": {
            "type": "object",
            "properties": {
                "machine_id": {
                    "type": "string",
                    "description": "The machine ID (e.g., 'MX-001') or name (e.g., 'mixer') to check",
                }
            },
            "required": ["machine_id"],
        },
    },
}


# =============================================================================
# Anomaly Detection Agent
# =============================================================================

class AnomalyDetectionAgent:
    def __init__(self):
        self.agent = None
        self.client = None

    async def create(self):
        """Create the anomaly detection agent in Foundry."""
        from azure.identity.aio import DefaultAzureCredential
        from azure.ai.projects.aio import AIProjectClient

        credential = DefaultAzureCredential()
        self.client = AIProjectClient(
            endpoint=PROJECT_CONNECTION_STRING,
            credential=credential,
        )

        # TODO: Define the system prompt for the anomaly detection agent.
        # The agent should:
        # - Analyze sensor readings against thresholds
        # - Classify status as normal/warning/critical
        # - Provide structured output with each reading's status
        system_prompt = """
        # TODO: Write your system prompt here
        # Hint: Tell the agent its role, how to classify anomalies,
        # and what format to respond in.
        """

        # TODO: Create the agent with the system prompt and the check_thresholds tool
        # Use: self.client.agents.create_agent(...)
        # Parameters needed: model, name, instructions, tools
        self.agent = None  # TODO: Replace with actual create_agent call

        return self.agent

    async def run(self, input_text: str) -> str:
        """Run the anomaly detection agent with the given input."""
        # TODO: Implement the agent run flow:
        # 1. Create a thread: await self.client.agents.create_thread()
        # 2. Add user message: await self.client.agents.create_message(thread_id=..., role="user", content=input_text)
        # 3. Create and process run: await self.client.agents.create_and_process_run(thread_id=..., agent_id=self.agent.id)
        #    NOTE: If the agent calls the check_thresholds tool, you need to handle it!
        #    Use create_run + poll loop, or create_and_process_run with tool handling
        # 4. Get messages: await self.client.agents.list_messages(thread_id=...)
        # 5. Return the assistant's response text

        # TODO: Replace this with your implementation
        raise NotImplementedError("Fill in the run() method")

    async def cleanup(self):
        """Delete the agent and close connections."""
        if self.agent:
            await self.client.agents.delete_agent(self.agent.id)
        if self.client:
            await self.client.close()


# =============================================================================
# Fault Diagnosis Agent
# =============================================================================

class FaultDiagnosisAgent:
    def __init__(self):
        self.agent = None
        self.client = None

    async def create(self):
        """Create the fault diagnosis agent in Foundry."""
        from azure.identity.aio import DefaultAzureCredential
        from azure.ai.projects.aio import AIProjectClient

        credential = DefaultAzureCredential()
        self.client = AIProjectClient(
            endpoint=PROJECT_CONNECTION_STRING,
            credential=credential,
        )

        # TODO: Define the system prompt for the fault diagnosis agent.
        # The agent should:
        # - Analyze patterns in anomalous readings
        # - Determine likely root causes
        # - Recommend specific maintenance actions
        # - Estimate urgency (immediate/24h/monitor)
        system_prompt = """
        # TODO: Write your system prompt here
        # Hint: Include common fault patterns (high temp + high pressure = blockage,
        # high vibration = bearing wear, etc.)
        """

        # TODO: Create the agent with the system prompt
        # This agent doesn't need the check_thresholds tool (it receives pre-analyzed data)
        # Use: self.client.agents.create_agent(...)
        self.agent = None  # TODO: Replace with actual create_agent call

        return self.agent

    async def run(self, input_text: str) -> str:
        """Run the fault diagnosis agent with the given input."""
        # TODO: Implement the agent run flow (same pattern as AnomalyDetectionAgent.run)
        # 1. Create thread
        # 2. Add message
        # 3. Run agent
        # 4. Get response

        # TODO: Replace this with your implementation
        raise NotImplementedError("Fill in the run() method")

    async def cleanup(self):
        """Delete the agent and close connections."""
        if self.agent:
            await self.client.agents.delete_agent(self.agent.id)
        if self.client:
            await self.client.close()


# =============================================================================
# Main — Test both agents
# =============================================================================

async def main():
    if not PROJECT_CONNECTION_STRING:
        print("❌ PROJECT_CONNECTION_STRING not set. Run challenge 0 first!")
        sys.exit(1)

    print("=== Anomaly Detection Agent ===")
    print("Creating agent...")

    anomaly_agent = AnomalyDetectionAgent()
    await anomaly_agent.create()
    print(f"✅ Created: {anomaly_agent.agent.id}")

    print("\nAnalyzing all machines...")
    anomaly_result = await anomaly_agent.run(
        "Check all 5 machines (MX-001, EX-002, CP-003, CU-004, IS-005) "
        "and report which ones have anomalies. For each anomaly, state the "
        "sensor, its current value, the threshold it violates, and by how much."
    )
    print(anomaly_result)

    print("\n=== Fault Diagnosis Agent ===")
    print("Creating agent...")

    diagnosis_agent = FaultDiagnosisAgent()
    await diagnosis_agent.create()
    print(f"✅ Created: {diagnosis_agent.agent.id}")

    print("\nDiagnosing critical machine: curing_press...")
    diagnosis_result = await diagnosis_agent.run(
        "The curing press (CP-003) has these anomalies:\n"
        "- Temperature: 198.5°C (max threshold: 180°C) — 10.3% over\n"
        "- Pressure: 18.2 bar (max threshold: 16.0 bar) — 13.8% over\n"
        "- Vibration: 7.3 mm/s (max threshold: 3.0 mm/s) — 143% over\n\n"
        "Last maintenance was 2026-03-20 (almost 2 months ago).\n"
        "Diagnose the fault and recommend an action."
    )
    print(diagnosis_result)

    # Cleanup
    print("\nCleaning up agents...")
    await anomaly_agent.cleanup()
    await diagnosis_agent.cleanup()
    print("✅ Done!")


if __name__ == "__main__":
    asyncio.run(main())
