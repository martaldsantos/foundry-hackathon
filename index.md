# Foundry Lab — Build AI Agents with Azure AI Foundry

A hands-on lab where you build, monitor, evaluate, and orchestrate AI agents using the **Microsoft Foundry SDK**.

## Choose Your Scenario

Pick one of the three industry scenarios below. Each follows the same five-challenge arc — setup, build, monitor, evaluate, and deploy a multi-agent workflow.

| Scenario | Domain | Agents You'll Build |
|----------|--------|---------------------|
| [🏭 Factory](./factory/README.md) | Predictive Maintenance | Anomaly Detection + Fault Diagnosis |
| [📋 Claims](./claims/README.md) | Insurance Claims Processing | Claims Triage + Claims Decision |
| [📞 Call Center](./callcenter/README.md) | Customer Support | Intent Classification + Resolution Advisor |

## Challenge Structure

Every scenario follows the same five challenges:

| # | Challenge | Duration |
|---|-----------|----------|
| 0 | **Setup** — Deploy Microsoft Foundryinfrastructure | 20 min |
| 1 | **Build Agents** — Create two AI agents with tools | 35 min |
| 2 | **Monitor** — Enable GenAI tracing with Application Insights | 20 min |
| 3 | **Evaluate** — Run systematic quality evaluations | 25 min |
| 4 | **Workflow** — Multi-agent orchestration via the Foundry portal | 20 min |

## Prerequisites

- Azure subscription with Contributor access
- Python 3.10+
- Azure CLI (`az`) installed and authenticated (`az login`)
- A terminal (bash, PowerShell, or WSL)
