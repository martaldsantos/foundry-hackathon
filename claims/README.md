# 📋 Foundry Lab: AI Agents for Insurance Claims Processing

## Scenario

You work at **ClaimSight Insurance**, a property and auto insurance company that processes hundreds of claims daily. Each claim has associated metrics: document completeness, damage-vs-estimate consistency, fraud risk scoring, and policy coverage matching. Lately, fraudulent claims and processing delays have been costing the company millions.

Your mission: **Build AI agents using Microsoft Foundry** that can triage incoming claims and make intelligent processing decisions — flagging suspicious claims for investigation while fast-tracking legitimate ones.

You'll build two agents:
1. **Claims Triage Agent** — Assesses claim metrics against acceptable thresholds and flags anomalies
2. **Claims Decision Agent** — Takes flagged claims and recommends actions (approve, investigate, request documents, deny)

## The Claims

| Claim | Type | Claimant | Status |
|-------|------|----------|--------|
| CLM-001 | Auto Collision | Maria Torres | 🔴 Critical |
| CLM-002 | Property Water Damage | James Chen | ✅ Normal |
| CLM-003 | Auto Theft | Robert Kim | ⚠️ Warning |
| CLM-004 | Property Fire | Sarah Williams | ✅ Normal |
| CLM-005 | Auto Collision | David Okafor | ⚠️ Warning |

## Prerequisites

- **Azure subscription** with Contributor access
- **Python 3.10+** installed locally
- **Azure CLI** (`az`) installed and logged in (`az login`)
- A terminal (bash, PowerShell, or WSL)
- ~15 minutes for infrastructure provisioning (run `challenge-0-setup/deploy.sh` from the repo root first!)

## Structure

All challenges are Python SDK-based. Challenge 4 also walks you through the Foundry portal to build and test the multi-agent workflow visually.

## Challenges

| # | Challenge | Duration | What You'll Do |
|---|-----------|----------|----------------|
| 0 | [Setup](../challenge-0-setup/) | 15 min | Provision resources, verify auth |
| 1 | [Build Agents](./challenge-1-build/) | 20 min | Create claims triage & decision agents |
| 2 | [Monitor](./challenge-2-monitor/) | 10 min | Enable tracing, explore App Insights |
| 3 | [Evaluate](./challenge-3-evaluate/) | 15 min | Run evaluations, interpret quality metrics |
| 4 | [Workflow](./challenge-4-deploy/) | 15 min | Build a multi-agent workflow: triage → decision → claims report |

## Quick Start

```bash
# 1. Complete Challenge 0 (shared setup) from the repo root
bash challenge-0-setup/deploy.sh

# 2. Start Challenge 1
cd claims/challenge-1-build
python agents.py
```

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                  Microsoft Foundry                     │
│  ┌──────────────────┐    ┌──────────────────────────┐│
│  │ Claims Triage    │    │ Claims Decision Agent    ││
│  │ Agent            │    │ (persistent v1)          ││
│  │ (persistent v1)  │    │                          ││
│  │                  │    │ Recommends: APPROVE /    ││
│  │ Tools:           │    │ INVESTIGATE / REQUEST /  ││
│  │ - assess_claim   │    │ DENY                    ││
│  └──────────────────┘    └──────────────────────────┘│
│                                                      │
│  ┌─────────────────────────────────────────────────┐ │
│  │ Application Insights (GenAI Tracing)            │ │
│  │ Traces every agent call, tool invocation,       │ │
│  │ token usage, and latency                        │ │
│  └─────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘
         ▲                           ▲
         │                           │
    assess_claim()            Decision input
    (local tool)              (from triage flags)
         │                           │
┌────────┴───────────────────────────┴─────────────────┐
│              Python Orchestration (deploy.py)         │
│  1. Triage all claims                                │
│  2. For each flagged claim → get decision            │
│  3. Print consolidated claims report                 │
└──────────────────────────────────────────────────────┘
```
