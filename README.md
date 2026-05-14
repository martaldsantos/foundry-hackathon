# 🤖 Foundry Lab: Build AI Agents with Azure AI Foundry

A hands-on step-by-step lab that teaches you to **build, monitor, evaluate, and orchestrate AI agents** using the Azure AI Foundry SDK. Complete in ~75 minutes.

## Choose Your Scenario

All paths teach the same Foundry concepts — pick the one that resonates with your audience:

| Scenario | Industry | Description | Start Here |
|----------|----------|-------------|------------|
| 🏭 **Factory** | Manufacturing | Detect machine anomalies and diagnose faults at TireForge Industries | [Factory Lab →](./factory/) |
| 📋 **Claims** | Insurance | Triage incoming claims and recommend actions at ClaimSight Insurance | [Claims Lab →](./claims/) |
| 📞 **Call Center** | Telecom | Classify call intents and advise resolutions at NovaTel Communications | [Call Center Lab →](./callcenter/) |

All scenarios follow the same 5-challenge structure:

| # | Challenge | Duration | What You'll Learn |
|---|-----------|----------|-------------------|
| 0 | **Setup** | 15 min | Provision Azure AI Foundry, deploy a model, verify auth |
| 1 | **Build Agents** | 20 min | Create two agents with tools and system prompts |
| 2 | **Monitor** | 10 min | Enable GenAI tracing with Application Insights |
| 3 | **Evaluate** | 15 min | Run LLM-as-judge evaluations against test datasets |
| 4 | **Workflow** | 15 min | Orchestrate agents in a multi-step pipeline |

## Prerequisites

- **Azure subscription** with Contributor access
- **Python 3.10+** installed locally
- **Azure CLI** (`az`) installed and logged in (`az login`)
- A terminal (bash, PowerShell, or WSL)
- ~15 minutes for infrastructure provisioning

## Structure

Each scenario is self-contained with its own setup (Challenge 0) through deployment (Challenge 4):

```
foundry-hackathon/
├── factory/                 ← 🏭 Factory scenario (challenges 0-4)
│   ├── challenge-0-setup/
│   ├── challenge-1-build/
│   ├── challenge-2-monitor/
│   ├── challenge-3-evaluate/
│   └── challenge-4-deploy/
├── claims/                  ← 📋 Claims scenario (challenges 0-4)
│   ├── challenge-0-setup/
│   ├── challenge-1-build/
│   ├── challenge-2-monitor/
│   ├── challenge-3-evaluate/
│   └── challenge-4-deploy/
├── callcenter/              ← 📞 Call Center scenario (challenges 0-4)
│   ├── challenge-0-setup/
│   ├── challenge-1-build/
│   ├── challenge-2-monitor/
│   ├── challenge-3-evaluate/
│   └── challenge-4-deploy/
└── requirements.txt         ← Shared dependencies
```


## Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/martaldsantos/foundry-hackathon.git && cd foundry-hackathon

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Login to Azure
az login

# 4. Pick your scenario and deploy infrastructure (~5 min)
#    Factory:
cd factory/challenge-0-setup && bash deploy.sh && cd ..
#    Claims:
cd claims/challenge-0-setup && bash deploy.sh && cd ..
#    Call Center:
cd callcenter/challenge-0-setup && bash deploy.sh && cd ..

# 5. Start Challenge 1!
#    Factory:     cd factory/challenge-1-build && python agents.py
#    Claims:      cd claims/challenge-1-build && python agents.py
#    Call Center: cd callcenter/challenge-1-build && python agents.py
```

### Using GitHub Codespaces?

To open GitHub Codespaces, click on the button below:

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/)

Please select your forked repository from the dropdown and, if necessary, adjust other settings of GitHub Codespace.


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

- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [azure-ai-projects SDK Reference](https://learn.microsoft.com/python/api/azure-ai-projects/)
