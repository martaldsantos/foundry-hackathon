# 🤖 Foundry Lab: Build AI Agents with Microsoft Foundry

A hands-on step-by-step lab that teaches you to **build, monitor, evaluate, and orchestrate AI agents** using the Microsoft Foundry SDK. Complete in ~75 minutes.

## Choose Your Scenario

All paths teach the same Foundry concepts — pick the one that resonates with you the most:

| Scenario | Industry | Description | Start Here |
|----------|----------|-------------|------------|
| 🏭 **Factory** | Manufacturing | Detect machine anomalies and diagnose faults at TireForge Industries | [Factory Lab →](./factory/) |
| 📋 **Claims** | Insurance | Triage incoming claims and recommend actions at ClaimSight Insurance | [Claims Lab →](./claims/) |
| 📞 **Call Center** | Telecom | Classify call intents and advise resolutions at NovaTel Communications | [Call Center Lab →](./callcenter/) |

All scenarios follow the same 5-challenge structure:

| # | Challenge | Duration | What You'll Learn |
|---|-----------|----------|-------------------|
| 0 | **Setup** | 15 min | Provision Microsoft Foundry, deploy a model, verify auth |
| 1 | **Build Agents** | 20 min | Create two agents with tools and system prompts |
| 2 | **Monitor** | 10 min | Enable GenAI tracing with Application Insights |
| 3 | **Evaluate** | 15 min | Run LLM-as-judge evaluations against test datasets |
| 4 | **Workflow** | 15 min | Orchestrate agents in a multi-step pipeline |

## Prerequisites

- **Azure subscription** with Contributor access
- **Python 3.10+** installed locally (not needed for Codespaces)
- **Azure CLI** (`az`) installed and logged in
- ~15 minutes for infrastructure provisioning

## Architecture

Both scenarios follow the same architecture pattern:

```
┌──────────────────────────────────────────────────────┐
│                  Microsoft Foundry                     │
│  ┌──────────────────┐    ┌──────────────────────────┐│
│  │ Detection Agent  │    │ Recommendation Agent     ││
│  │ (persistent v1)  │    │ (persistent v1)          ││
│  └────────┬─────────┘    └───────────┬──────────────┘│
│           │                          │                │
│           └──────────┬───────────────┘                │
│                      │                                │
├──────────────────────┼────────────────────────────────┤
│         Application Insights                          │
│         (GenAI traces, latency, token usage)          │
└──────────────────────┼────────────────────────────────┘
                       │
              ┌────────┴────────┐
              │ Python SDK /    │
              │ Any Client      │
              └─────────────────┘
```

## Resources

- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [azure-ai-projects SDK Reference](https://learn.microsoft.com/python/api/azure-ai-projects/)
