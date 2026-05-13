# 🏭 Foundry Hackathon: AI Agents for Predictive Manufacturing

## Scenario

You work at **TireForge Industries**, a tire manufacturing plant with 5 critical machines on the production floor. Each machine emits real-time sensor data (temperature, pressure, vibration, RPM). Lately, unexpected failures have been causing costly downtime.

Your mission: **Build AI agents using Microsoft Foundry** that can detect anomalies in sensor readings and diagnose potential faults before machines break down.

You'll build two agents:
1. **Anomaly Detection Agent** — Monitors sensor data and flags readings outside normal thresholds
2. **Fault Diagnosis Agent** — Takes flagged anomalies and recommends maintenance actions

## The Machines

| Machine | Role | Status |
|---------|------|--------|
| Mixer | Blends raw rubber compounds | ⚠️ Warning |
| Extruder | Shapes rubber into treads | ✅ Normal |
| Curing Press | Vulcanizes tire under heat/pressure | 🔴 Critical |
| Cooling Unit | Brings cured tires to safe temp | ✅ Normal |
| Inspection Station | QA checks via vibration analysis | ⚠️ Warning |

## Prerequisites

- **Azure subscription** with Contributor access
- **Python 3.10+** installed locally
- **Azure CLI** (`az`) installed and logged in (`az login`)
- A terminal (bash, PowerShell, or WSL)
- ~15 minutes for infrastructure provisioning (run `challenge-0-setup/deploy.sh` first!)

## Choose Your Track

Each challenge offers two paths:

| Track | Best for | You'll use |
|-------|----------|------------|
| **Portal Track** | Visual learners, less coding experience | Azure Portal, Foundry UI |
| **SDK Track** | Developers, automation-minded | Python, azure-ai-projects SDK |

You can mix tracks across challenges — they cover the same concepts.

## Challenges

| # | Challenge | Duration | What You'll Do |
|---|-----------|----------|----------------|
| 0 | [Setup](./challenge-0-setup/) | 20 min | Provision resources, verify auth |
| 1 | [Build Agents](./challenge-1-build/) | 50 min | Create anomaly detection & fault diagnosis agents |
| 2 | [Monitor](./challenge-2-monitor/) | 30 min | Enable tracing, explore App Insights |
| 3 | [Evaluate](./challenge-3-evaluate/) | 30 min | Run evaluations, interpret quality metrics |
| 4 | [Workflow](./challenge-4-deploy/) | 30 min | Build a multi-agent workflow: anomaly scan → fault diagnosis → factory health report |

**Total time: ~2.5 hours**

## Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/martaldsantos/foundry-hackathon.git && cd foundry-hackathon

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Login to Azure
az login

# 4. Deploy infrastructure & auto-generate .env (~5 min)
bash challenge-0-setup/deploy.sh

# 5. Start Challenge 0!
```

> **Using GitHub Codespaces?** Click **Code → Codespaces → New codespace** on the repo page. Dependencies install automatically via the devcontainer — skip steps 1-2 and start at step 3 (az login).

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                  Azure AI Foundry                     │
│  ┌──────────────────┐    ┌──────────────────────────┐│
│  │ Anomaly Agent    │    │ Fault Diagnosis Agent    ││
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
