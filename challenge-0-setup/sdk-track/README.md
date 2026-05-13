# Challenge 0: Setup — SDK Track

## Step-by-Step Instructions

### Step 1: Install Dependencies

```bash
# From the repo root
pip install -r requirements.txt
```

This installs:
- `azure-ai-projects>=2.0.0` — The Foundry SDK
- `azure-identity` — Azure authentication
- `python-dotenv` — Load environment variables from `.env`
- `aiohttp` — Async HTTP (required for async SDK)

### Step 2: Configure Your Environment

1. Run the deploy script (if you haven't already) — it auto-generates your `.env`:
   ```bash
   bash challenge-0-setup/deploy.sh
   ```

2. Verify the `.env` file exists at the repository root (`.env`) with at minimum:
   - `PROJECT_CONNECTION_STRING` — Your Foundry project endpoint
   - `MODEL_DEPLOYMENT_NAME` — Should be `gpt-5.1`

### Step 3: Run the Verification Script

```bash
cd challenge-0-setup/sdk-track
python verify_setup.py
```

### What the Script Does

1. Loads your `.env` configuration
2. Authenticates using `DefaultAzureCredential` (your `az login` session)
3. Creates a temporary test agent
4. Sends it a simple message
5. Prints the agent's response
6. Cleans up (deletes the test agent)

### Expected Output

```
✅ Environment loaded successfully
✅ Authenticated to Azure
✅ Connected to Foundry project
✅ Created test agent: agent-xxxxx
✅ Agent response: "Hello! I'm working correctly..."
✅ Cleaned up test agent
🎉 Setup verified! You're ready for Challenge 1.
```

### Troubleshooting

| Error | Fix |
|-------|-----|
| `DefaultAzureCredential failed` | Run `az login` first |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `ResourceNotFoundError` | Check `PROJECT_CONNECTION_STRING` in `.env` |
| `AuthorizationFailed` | Ask facilitator to assign `Cognitive Services Contributor` role |

## ✅ Done!

Your local environment can talk to Foundry. Move on to [Challenge 1: Build Agents](../../challenge-1-build/).
