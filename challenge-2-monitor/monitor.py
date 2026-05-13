"""
Challenge 2: Monitor with Application Insights — SDK Track
Enable GenAI tracing and verify traces appear in App Insights.

Usage:
    python monitor.py

IMPORTANT: Environment variables must be set BEFORE importing azure.ai.projects!
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv


def _find_repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists():
            return parent
    return Path(__file__).resolve().parents[2]


# Load environment FIRST — tracing env vars must be set before SDK import
env_path = _find_repo_root() / ".env"
load_dotenv(env_path)

# Verify tracing is enabled
if os.getenv("AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING") != "true":
    print("❌ AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING is not set to 'true' in .env")
    print("   Add: AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true")
    sys.exit(1)

PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.1")
APPINSIGHTS_CONN_STRING = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")


def setup_tracing():
    """Configure OpenTelemetry instrumentation and Azure Monitor export."""
    print("=== Setting up tracing ===")
    print("✅ AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING is enabled")

    # TODO: Set up the AIProjectInstrumentor
    # This auto-instruments all azure-ai-projects SDK calls with OpenTelemetry spans.
    #
    # from azure.ai.projects.telemetry import AIProjectInstrumentor
    # AIProjectInstrumentor().instrument()
    # print("✅ AIProjectInstrumentor configured")

    # TODO: Configure the Azure Monitor exporter
    # This sends collected spans to Application Insights.
    #
    # from azure.monitor.opentelemetry import configure_azure_monitor
    # configure_azure_monitor(
    #     connection_string=APPINSIGHTS_CONN_STRING,
    #     enable_live_metrics=True,
    # )
    # print("✅ Azure Monitor exporter connected")

    pass  # TODO: Remove once implemented


def run_traced_agent_call():
    """Make an agent call that will be captured as a trace."""
    print("\n=== Running traced agent call ===")

    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import PromptAgentDefinition
    from azure.identity import DefaultAzureCredential

    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=DefaultAzureCredential(),
    )
    openai_client = client.get_openai_client()

    # TODO: Create a temporary agent, send a message, and get a response.
    # This interaction will be automatically captured as a distributed trace.
    #
    # agent = client.agents.create_version(
    #     agent_name="tracing-test-agent",
    #     definition=PromptAgentDefinition(
    #         model=MODEL_DEPLOYMENT_NAME,
    #         instructions="You are a factory monitoring assistant. Respond briefly.",
    #     ),
    # )
    #
    # conversation = openai_client.conversations.create()
    # response = openai_client.responses.create(
    #     input="What are the top 3 things to monitor in a curing press?",
    #     conversation=conversation.id,
    #     extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
    # )
    # print(f"✅ Agent responded: {response.output_text[:100]}...")
    #
    # # Cleanup
    # openai_client.conversations.delete(conversation_id=conversation.id)
    # client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)

    # TODO: Uncomment the above and remove this placeholder
    print("   (not implemented yet — fill in the TODO)")

    client.close()


def verify_traces():
    """Wait for traces to propagate and verify they appear in App Insights."""
    print("\n=== Verifying traces in App Insights ===")

    if not APPINSIGHTS_CONN_STRING:
        print("⚠️  APPLICATIONINSIGHTS_CONNECTION_STRING not set — skipping verification")
        print("   You can still check traces manually in the Azure Portal")
        return

    print("⏳ Waiting for traces to propagate (30 seconds)...")
    time.sleep(30)

    print("✅ Traces should now be visible in Application Insights")
    print("   Go to: Azure Portal → Application Insights → Transaction search")
    print("   Filter by: Last 5 minutes, Event type: Dependency")


def main():
    if not PROJECT_CONNECTION_STRING:
        print("❌ PROJECT_CONNECTION_STRING not set. Run challenge 0 first!")
        sys.exit(1)

    setup_tracing()
    run_traced_agent_call()
    verify_traces()

    print("\n🎉 Monitoring is active! Check App Insights for the full trace view.")


if __name__ == "__main__":
    main()
