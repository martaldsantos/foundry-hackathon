"""
Challenge 2: Deploy & Expose — SDK Track
Version agents and verify APIM gateway.

Usage:
    python deploy.py

Fill in the TODOs to complete the deployment verification.
"""

import asyncio
import os
import sys
from pathlib import Path

import aiohttp
from dotenv import load_dotenv


# Load environment
env_path = Path(__file__).resolve().parent.parent.parent / "challenge-0-setup" / ".env"
load_dotenv(env_path)

PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-5.1")
APIM_GATEWAY_URL = os.getenv("APIM_GATEWAY_URL")
APIM_SUBSCRIPTION_KEY = os.getenv("APIM_SUBSCRIPTION_KEY")


async def create_versioned_agent():
    """Create a named, versioned production agent."""
    from azure.identity.aio import DefaultAzureCredential
    from azure.ai.projects.aio import AIProjectClient

    credential = DefaultAzureCredential()
    client = AIProjectClient(
        endpoint=PROJECT_CONNECTION_STRING,
        credential=credential,
    )

    # TODO: Create a production-ready agent with a versioned name
    # Use the same system prompt from Challenge 1's AnomalyDetectionAgent
    # but with a production-appropriate name like "anomaly-detection-v1"
    #
    # agent = await client.agents.create_agent(
    #     model=MODEL_DEPLOYMENT_NAME,
    #     name="anomaly-detection-v1",
    #     instructions="...",  # Your production system prompt
    # )
    # print(f"✅ Created production agent: anomaly-detection-v1 ({agent.id})")

    # TODO: Uncomment and fill in the above

    await credential.close()
    await client.close()


async def verify_apim_gateway():
    """Verify the APIM gateway is working and rate limiting is active."""
    if not APIM_GATEWAY_URL or not APIM_SUBSCRIPTION_KEY:
        print("⚠️  APIM_GATEWAY_URL or APIM_SUBSCRIPTION_KEY not set in .env")
        print("   If APIM is still provisioning, skip this step and come back later.")
        return

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": APIM_SUBSCRIPTION_KEY,
    }

    payload = {
        "messages": [
            {"role": "user", "content": "Say 'APIM gateway working' and nothing else."}
        ],
        "model": MODEL_DEPLOYMENT_NAME,
        "max_tokens": 20,
    }

    # TODO: Make a POST request to the APIM gateway to verify it responds
    # The endpoint is typically: {APIM_GATEWAY_URL}/ai/openai/deployments/{MODEL_DEPLOYMENT_NAME}/chat/completions?api-version=2024-02-15-preview
    #
    # Use aiohttp:
    # async with aiohttp.ClientSession() as session:
    #     url = f"{APIM_GATEWAY_URL}/ai/openai/deployments/{MODEL_DEPLOYMENT_NAME}/chat/completions?api-version=2024-02-15-preview"
    #     async with session.post(url, json=payload, headers=headers) as resp:
    #         if resp.status == 200:
    #             data = await resp.json()
    #             print(f"✅ Model responds through APIM: {data['choices'][0]['message']['content']}")
    #         else:
    #             print(f"❌ APIM returned status {resp.status}: {await resp.text()}")

    # TODO: Test rate limiting by making 11+ rapid requests
    # After 10 requests in a minute, you should get a 429 status code
    #
    # rate_limited = False
    # async with aiohttp.ClientSession() as session:
    #     for i in range(12):
    #         async with session.post(url, json=payload, headers=headers) as resp:
    #             if resp.status == 429:
    #                 rate_limited = True
    #                 print(f"✅ Rate limiting active (got 429 on request #{i+1})")
    #                 break
    #
    # if not rate_limited:
    #     print("⚠️  Rate limiting didn't trigger — check your APIM policy")

    pass  # TODO: Remove this once you implement the above


async def main():
    if not PROJECT_CONNECTION_STRING:
        print("❌ PROJECT_CONNECTION_STRING not set. Run challenge 0 first!")
        sys.exit(1)

    print("=== Agent Versioning ===")
    await create_versioned_agent()

    print("\n=== APIM Gateway Verification ===")
    await verify_apim_gateway()

    print("\n🎉 Deployment verified!")


if __name__ == "__main__":
    asyncio.run(main())
