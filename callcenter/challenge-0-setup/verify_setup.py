"""
Challenge 0: Setup Verification Script
Confirms that authentication and Foundry endpoint are working correctly.

Usage:
    python verify_setup.py

Prerequisites:
    - .env file configured with PROJECT_CONNECTION_STRING and MODEL_DEPLOYMENT_NAME
    - az login completed
    - pip install -r requirements.txt
"""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from azure.ai.agents.aio import AgentsClient
from azure.identity.aio import DefaultAzureCredential


def _find_repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / ".env").exists():
            return parent
    return Path(__file__).resolve().parents[2]


async def main():
    # Step 1: Load environment
    env_path = _find_repo_root() / ".env"
    load_dotenv(env_path)

    project_connection_string = os.getenv("PROJECT_CONNECTION_STRING")
    model_deployment_name = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.1")

    if not project_connection_string:
        print("❌ PROJECT_CONNECTION_STRING not found in .env")
        print("   Run 'bash challenge-0-setup/deploy.sh' to provision resources and auto-generate .env")
        sys.exit(1)

    print("✅ Environment loaded successfully")

    # Step 2: Authenticate
    credential = DefaultAzureCredential()
    print("✅ Authenticated to Azure")

    # Step 3: Connect to Foundry project endpoint
    agents_client = AgentsClient(
        endpoint=project_connection_string,
        credential=credential,
    )
    print("✅ Connected to Foundry project")

    # Step 4: Create a test agent
    agent = await agents_client.create_agent(
        model=model_deployment_name,
        name="setup-verification-agent",
        instructions="You are a helpful assistant. Respond briefly to confirm you are working.",
    )
    print(f"✅ Created test agent: {agent.id}")

    # Step 5: Create a thread and send a message
    thread = await agents_client.threads.create()
    await agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content="Say 'Hello! I'm working correctly.' and nothing else.",
    )

    # Step 6: Run the agent and get response
    run = await agents_client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,
    )

    if run.status == "failed":
        print(f"❌ Agent run failed: {run.last_error}")
        await agents_client.delete_agent(agent.id)
        await credential.close()
        await agents_client.close()
        sys.exit(1)

    assistant_message = None
    messages = agents_client.messages.list(thread_id=thread.id)
    async for msg in messages:
        if msg.role == "assistant" and getattr(msg, "text_messages", None):
            assistant_message = msg.text_messages[-1].text.value
            break

    print(f"✅ Agent response: \"{assistant_message}\"")

    # Step 7: Cleanup
    await agents_client.delete_agent(agent.id)
    print("✅ Cleaned up test agent")

    await credential.close()
    await agents_client.close()

    print("\n🎉 Setup verified! You're ready for Challenge 1.")


if __name__ == "__main__":
    asyncio.run(main())
