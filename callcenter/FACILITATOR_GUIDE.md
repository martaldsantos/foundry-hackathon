# Facilitator Guide — Call Center (Intent & Resolution)

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
| 0:15 – 0:35 | **Challenge 1: Build** | Create both agents, test with call data |
| 0:35 – 0:45 | **Challenge 2: Monitor** | Enable GenAI tracing, explore App Insights |
| 0:45 – 1:00 | **Challenge 3: Evaluate** | Run evaluations, interpret quality metrics |
| 1:00 – 1:15 | **Challenge 4: Workflow** | Wire agents into an automated triage pipeline |

### Buffer Time
- Build in 5 min buffer between challenges for reconvene/Q&A
- If a challenge runs short, use the time for open exploration or bonus tasks

## Reconvene Talking Points

### After Challenge 0 → Before Challenge 1
- "Everyone should have a working connection to Foundry. The project you just verified is where your agents will live."
- Bridge: "Portal users — you saw the playground. SDK users — you just talked to the same endpoint programmatically. Both paths lead to the same infrastructure."

### After Challenge 1 → Before Challenge 2
- "You now have two agents that can classify calls and recommend resolutions. But in production, you need visibility into what they're actually doing."
- Bridge: "What if the intent agent misclassifies a security concern as a billing issue? Challenge 2 gives you observability — every agent interaction traced in Application Insights."

### After Challenge 2 → Before Challenge 3
- "You can now see every agent interaction as a trace in App Insights. You know latency, token usage, and can query historical data."
- Bridge: "Seeing traces tells you what happened. Evaluation tells you if the classifications were actually correct. Let's systematically test quality."

### After Challenge 3 → Before Challenge 4
- "You've tested your agents systematically — you know how they score on quality metrics."
- Bridge: "Now let's put them to work together. Challenge 4 builds a multi-agent triage workflow: the Intent Agent classifies all incoming calls, and for each high-priority call the Resolution Agent recommends the optimal action — producing a full Shift Report. The agents persist as production assets; the workflow is your automation layer on top."

### Wrap-Up After Challenge 4 (Workflow)
- Recap the full lifecycle: Build → Monitor → Evaluate → Deploy
- Highlight that portal and SDK both accessed the same underlying platform
- Mention next steps: custom evaluators, multi-agent orchestration, CI/CD integration

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

1. **Start deploy.sh immediately** — Don't wait for the overview talk to finish. Deploy takes a few minutes and participants can explore the portal while it runs.
2. **Encourage portal exploration** — In Challenge 4, participants build the multi-agent workflow visually in the Foundry portal before invoking it via SDK. Make sure they've deployed the agents first.
3. **Keep the call_data.json visible** — Project it on screen or share the link. Participants reference it constantly in Challenge 1.
4. **Don't skip the reconvene** — The 5-min bridges between challenges are where concepts click. They connect the "how" to the "why."
5. **Fallback environment** — Have one pre-provisioned resource group that anyone can use if their deploy fails. Share read-only creds.
6. **Security concern as anchor** — CALL-007 (suspected hack) is the most dramatic scenario. Use it to illustrate why intent classification accuracy matters — a misclassification here could leave a customer's account compromised.
