# Challenge 2: Deploy & Expose — SDK Track

## Step-by-Step Instructions

### Overview

In this challenge you'll:
1. Version your agents (so you can roll back if needed)
2. Verify the APIM gateway is working programmatically
3. Call the Foundry model through APIM instead of directly

### Step 1: Understand deploy.py

Open `deploy.py` and review the structure. You need to fill in:
1. **Agent versioning** — Create a named, versioned agent that persists
2. **APIM verification** — Call the APIM gateway endpoint and confirm it responds

### Step 2: Fill in the TODOs

Complete the TODO sections in `deploy.py`.

### Step 3: Run

```bash
cd challenge-2-deploy/sdk-track
python deploy.py
```

### Expected Output

```
=== Agent Versioning ===
✅ Created production agent: anomaly-detection-v1 (agent-xxxxx)

=== APIM Gateway Verification ===
✅ APIM gateway is online
✅ Model responds through APIM gateway
✅ Rate limiting is active (got 429 after 10+ rapid calls)

🎉 Deployment verified! Agents are production-ready.
```

## ✅ Done!

Move on to [Challenge 3: Monitor](../../challenge-3-monitor/).
