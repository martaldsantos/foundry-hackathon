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

from dotenv import load_dotenv


async def main():
    # Step 1: Load environment
    env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    load_dotenv(env_path)

    project_connection_string = os.getenv("PROJECT_CONNECTION_STRING")
    model_deployment_name = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.1")

    if not project_connection_string:
        print("❌ PROJECT_CONNECTION_STRING not found in .env")
        print("   Run 'cp infra/.env.template .env' and fill in the values from deploy.sh output")
        sys.exit(1)

    print("✅ Environment loaded successfully")

    # Step 2: Authenticate
    from azure.identity.aio import DefaultAzureCredential

    credential = DefaultAzureCredential()
    print("✅ Authenticated to Azure")

    # Step 3: Connect to Foundry
    from azure.ai.projects.aio import AIProjectClient

    project_client = AIProjectClient(
        endpoint=project_connection_string,
        credential=credential,
    )
    print("✅ Connected to Foundry project")

    # Step 4: Create a test agent
    agent = await project_client.agents.create_agent(
        model=model_deployment_name,
        name="setup-verification-agent",
        instructions="You are a helpful assistant. Respond briefly to confirm you are working.",
    )
    print(f"✅ Created test agent: {agent.id}")

    # Step 5: Create a thread and send a message
    thread = await project_client.agents.create_thread()
    await project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Say 'Hello! I'm working correctly.' and nothing else.",
    )

    # Step 6: Run the agent and get response
    run = await project_client.agents.create_and_process_run(
        thread_id=thread.id,
        agent_id=agent.id,
    )

    if run.status == "failed":
        print(f"❌ Agent run failed: {run.last_error}")
        await project_client.agents.delete_agent(agent.id)
        await credential.close()
        await project_client.close()
        sys.exit(1)

    messages = await project_client.agents.list_messages(thread_id=thread.id)
    assistant_message = None
    for msg in messages.data:
        if msg.role == "assistant":
            assistant_message = msg.content[0].text.value
            break

    print(f"✅ Agent response: \"{assistant_message}\"")

    # Step 7: Cleanup
    await project_client.agents.delete_agent(agent.id)
    print("✅ Cleaned up test agent")

    await credential.close()
    await project_client.close()

    print("\n🎉 Setup verified! You're ready for Challenge 1.")


if __name__ == "__main__":
    asyncio.run(main())
