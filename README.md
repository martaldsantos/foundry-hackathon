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


## Quick Start

There are two ways to get started — pick one:

> **First step for both options:** [Fork this repository](https://github.com/martaldsantos/foundry-hackathon/fork) to your own GitHub account.

### Option A: GitHub Codespaces (recommended)

No local installs needed. Everything runs in a cloud dev environment.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/martaldsantos/foundry-hackathon)

1. Click the badge above (select your fork if applicable)
2. Wait for the Codespace to build (~2 min)
3. In the terminal, login to Azure and deploy your scenario:

```bash
az login
```

4. Start Challenge 0!

---

### Option B: Local environment

Run everything on your own machine. Requires Python 3.10+ and Azure CLI.

```bash
# 1. Clone this repo
git clone https://github.com/martaldsantos/foundry-hackathon.git
cd foundry-hackathon

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Login to Azure
az login
```
4. Start Challenge 0!

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
