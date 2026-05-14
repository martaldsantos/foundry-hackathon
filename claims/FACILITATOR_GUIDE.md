# Facilitator Guide — Claims Processing Lab

## Pre-Event Checklist

### One Week Before
- [ ] Verify Azure subscription has sufficient quota for gpt-5.1 in swedencentral
- [ ] Test `challenge-0-setup/deploy.sh` end-to-end in a clean subscription
- [ ] Confirm model availability: `az cognitiveservices model list --location swedencentral --query "[?model.name=='gpt-5.1']"`
- [ ] Ensure participants have Contributor role on the resource group (or subscription)

### Day Of
- [ ] Have participants run `challenge-0-setup/deploy.sh` at the very start
- [ ] Verify WiFi/network can reach Azure endpoints
- [ ] Have a pre-provisioned "fallback" environment ready if someone's deploy fails
- [ ] Print or share this timing guide

## Timing Guide

| Time | Challenge | Activity |
|------|-----------|----------|
| 0:00 – 0:15 | **Challenge 0: Setup** | Deploy infra, verify auth, explore Foundry portal |
| 0:15 – 0:35 | **Challenge 1: Build** | Create both agents, test with claims data |
| 0:35 – 0:45 | **Challenge 2: Monitor** | Enable GenAI tracing, explore App Insights |
| 0:45 – 1:00 | **Challenge 3: Evaluate** | Run evaluations, interpret quality metrics |
| 1:00 – 1:15 | **Challenge 4: Workflow** | Wire agents into an automated claims processing pipeline |

### Buffer Time
- Build in 5 min buffer between challenges for reconvene/Q&A
- If a challenge runs short, use the time for open exploration or bonus tasks

## Reconvene Talking Points

### After Challenge 0 → Before Challenge 1
- "Everyone should have a working connection to Foundry. The project you just verified is where your agents will live."
- Bridge: "Now let's build the brains — two agents that can triage and decide on insurance claims automatically."

### After Challenge 1 → Before Challenge 2
- "You now have two agents that can assess claims and recommend actions. But in production, you need visibility into what they're actually doing — especially with financial decisions."
- Bridge: "Challenge 2 is about observability — enabling tracing so every agent interaction is captured in Application Insights. If an agent wrongly denies a claim, you need to see exactly why."

### After Challenge 2 → Before Challenge 3
- "You can now see every agent interaction as a trace in App Insights. You know latency, token usage, and can query historical decisions."
- Bridge: "Seeing traces tells you what happened. Evaluation tells you if the decisions were actually correct. Let's systematically test quality against known-good cases."

### After Challenge 3 → Before Challenge 4
- "You've tested your agents systematically — you know how they score on quality metrics."
- Bridge: "Now let's put them to work together. Challenge 4 builds a multi-agent workflow: the Triage Agent assesses all claims, and for each flagged claim the Decision Agent recommends an action — producing a full Claims Processing Report."

### Wrap-Up After Challenge 4
- Recap the full lifecycle: Build → Monitor → Evaluate → Deploy
- Highlight that portal and SDK both accessed the same underlying platform
- Discuss real-world considerations: human-in-the-loop for high-value claims, regulatory compliance, audit trails
- Mention next steps: custom evaluators, CI/CD integration, connecting to actual claims management systems

## Common Errors & Fixes

### Authentication Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `DefaultAzureCredential failed` | Not logged in to Azure CLI | Run `az login` |
| `AuthorizationFailed` | Missing RBAC role | Assign `Cognitive Services Contributor` on the resource |
| `InvalidSubscription` | Wrong subscription active | `az account set --subscription <id>` |

### Quota & Region Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `InsufficientQuota` | Not enough TPM for gpt-5.1 | Reduce `--sku-capacity` in deploy.sh or request quota increase |
| `ModelNotFound` | Model not available in region | Check `az cognitiveservices model list --location swedencentral` |
| `ResourceNotFound` after deploy | Resources still provisioning | Wait 2-3 min and retry |

### SDK Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: azure.ai.projects` | Package not installed | `pip install azure-ai-projects>=2.0.0` |
| `AttributeError: 'AIProjectClient' has no attribute 'agents'` | Using SDK v1 patterns | Ensure `azure-ai-projects>=2.0.0` installed |
| Async errors in Jupyter | Event loop conflict | Use `nest_asyncio` or run from terminal instead |

## Tips for Success

1. **Start deploy.sh immediately** — Don't wait for the overview talk to finish. Deploy takes a few minutes.
2. **Keep the claims_data.json visible** — Project it on screen or share the link. Participants reference it constantly in Challenge 1.
3. **Discuss real-world implications** — Insurance claims have regulatory requirements. Use this to motivate why monitoring and evaluation matter.
4. **Don't skip the reconvene** — The 5-min bridges between challenges connect the "how" to the "why."
5. **Fallback environment** — Have one pre-provisioned resource group that anyone can use if their deploy fails.
