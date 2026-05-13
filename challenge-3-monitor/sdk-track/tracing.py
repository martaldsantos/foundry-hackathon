"""
Challenge 3: Monitor with Application Insights — SDK Track
Enable GenAI tracing and verify traces appear in App Insights.

Usage:
    python tracing.py

IMPORTANT: Environment variables must be set BEFORE importing azure.ai.projects!
Fill in the TODOs to complete the tracing setup.
"""

import asyncio
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# Load environment FIRST — tracing env vars must be set before SDK import
env_path = Path(__file__).resolve().parent.parent.parent / "challenge-0-setup" / ".env"
load_dotenv(env_path)

# Verify tracing is enabled
if os.getenv("AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING") != "true":
    print("❌ AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING is not set to 'true' in .env")
    print("   Add: AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true")
    sys.exit(1)

PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.1")
APPINSIGHTS_CONN_STRING = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")


async def setup_tracing():
    """Configure OpenTelemetry instrumentation and Azure Monitor export."""
    print("=== Setting up tracing ===")
    print("✅ AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING is enabled")

    # TODO: Set up the AIProjectInstrumentor
    # This auto-instruments all azure-ai-projects SDK calls with OpenTelemetry spans.
    #
    # from azure.ai.projects.telemetry import AIProjectInstrumentor
    #
    # AIProjectInstrumentor().instrument()
    # print("✅ AIProjectInstrumentor configured")

    # TODO: Configure the Azure Monitor exporter
    # This sends collected spans to Application Insights.
    #
    # from azure.monitor.opentelemetry import configure_azure_monitor
    #
    # configure_azure_monitor(
    #     connection_string=APPINSIGHTS_CONN_STRING,
    #     # Enable logging of prompt/completion content (disable in production)
    #     enable_live_metrics=True,
    # )
    # print("✅ Azure Monitor exporter connected")

    pass  # TODO: Remove once implemented


async def run_traced_agent_call():
    """Make an agent call that will be captured as a trace."""
    print("\n=== Running traced agent call ===")

    from azure.identity.aio import DefaultAzureCredential
    from azure.ai.projects.aio import AIProjectClient

    credential = DefaultAzureCredential()
    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=credential,
    )

    # TODO: Create a temporary agent, send a message, and get a response.
    # This interaction will be automatically captured as a distributed trace.
    #
    # agent = await client.agents.create_agent(
    #     model=MODEL_DEPLOYMENT_NAME,
    #     name="tracing-test-agent",
    #     instructions="You are a factory monitoring assistant. Respond briefly.",
    # )
    #
    # thread = await client.agents.create_thread()
    # await client.agents.create_message(
    #     thread_id=thread.id,
    #     role="user",
    #     content="What are the top 3 things to monitor in a curing press?",
    # )
    #
    # run = await client.agents.create_and_process_run(
    #     thread_id=thread.id,
    #     agent_id=agent.id,
    # )
    #
    # if run.status == "completed":
    #     messages = await client.agents.list_messages(thread_id=thread.id)
    #     for msg in messages.data:
    #         if msg.role == "assistant":
    #             print(f"✅ Agent responded: {msg.content[0].text.value[:100]}...")
    #             break
    # else:
    #     print(f"❌ Agent run failed: {run.status}")
    #
    # # Cleanup
    # await client.agents.delete_agent(agent.id)

    # TODO: Uncomment the above and remove this placeholder
    print("   (not implemented yet — fill in the TODO)")

    await credential.close()
    await client.close()


async def verify_traces():
    """Wait for traces to propagate and verify they appear in App Insights."""
    print("\n=== Verifying traces in App Insights ===")

    if not APPINSIGHTS_CONN_STRING:
        print("⚠️  APPLICATIONINSIGHTS_CONNECTION_STRING not set — skipping verification")
        print("   You can still check traces manually in the Azure Portal")
        return

    # Traces take time to propagate
    print("⏳ Waiting for traces to propagate (30 seconds)...")
    await asyncio.sleep(30)

    # TODO: Query Application Insights for recent traces
    # You can use the Azure Monitor Query SDK or just direct the user to the portal.
    #
    # Option 1: Direct user to portal
    print("✅ Traces should now be visible in Application Insights")
    print("   Go to: Azure Portal → Application Insights → Transaction search")
    print("   Filter by: Last 5 minutes, Event type: Dependency")
    #
    # Option 2 (bonus): Query programmatically using azure-monitor-query
    # from azure.identity.aio import DefaultAzureCredential
    # from azure.monitor.query.aio import LogsQueryClient
    #
    # credential = DefaultAzureCredential()
    # logs_client = LogsQueryClient(credential)
    #
    # # Get workspace ID from App Insights connection string
    # query = """
    # dependencies
    # | where timestamp > ago(5m)
    # | where type contains "AI" or type contains "OpenAI"
    # | summarize count(), avg(duration) by target
    # """
    #
    # # Note: You'll need the Log Analytics workspace ID for this query
    # # result = await logs_client.query_workspace(workspace_id, query, timespan="PT5M")
    #
    # await credential.close()


async def main():
    if not PROJECT_CONNECTION_STRING:
        print("❌ PROJECT_CONNECTION_STRING not set. Run challenge 0 first!")
        sys.exit(1)

    await setup_tracing()
    await run_traced_agent_call()
    await verify_traces()

    print("\n🎉 Monitoring is active! Check App Insights for the full trace view.")


if __name__ == "__main__":
    asyncio.run(main())
