# 🏭 Scenario: Predictive Maintenance — TireForge Industries

## Background

**TireForge Industries** operates a tire manufacturing plant with 5 critical machines:

- **MX-001** (Mixer) — Blends raw rubber compounds
- **EX-002** (Extruder) — Shapes rubber into tire tread profiles
- **CP-003** (Curing Press) — Vulcanizes tires under heat and pressure
- **CU-004** (Cooling Unit) — Gradually cools cured tires
- **IS-005** (Inspection Station) — Quality assurance via vibration analysis

Each machine emits real-time sensor data: temperature, pressure, vibration, and RPM.

## Your Mission

Build an AI agent system that:

1. **Detects anomalies** — Compares sensor readings against thresholds
2. **Diagnoses faults** — Reasons about root causes from anomaly patterns
3. **Reports health** — Produces a consolidated factory health report

## Challenges

| # | Challenge | What You'll Do | Time |
|---|-----------|---------------|------|
| 0 | [Setup](./challenge-0-setup/README.md) | Deploy Microsoft Foundry infrastructure | 20 min |
| 1 | [Build Agents](./challenge-1-build/README.md) | Create Anomaly Detection + Fault Diagnosis agents | 35 min |
| 2 | [Monitor](./challenge-2-monitor/README.md) | Enable GenAI tracing with Application Insights | 20 min |
| 3 | [Evaluate](./challenge-3-evaluate/README.md) | Run systematic quality evaluations | 25 min |
| 4 | [Production Workflow](./challenge-4-deploy/README.md) | Multi-agent orchestration + portal workflow | 20 min |

## The Agent Lifecycle

These four challenges follow the same arc that engineering teams use when taking AI agent systems to production. Each phase builds directly on the previous one — skipping any of them leaves a gap that will surface as an incident in production.

### 1. Build — Define what your agents can do

Before you can run, monitor, or evaluate anything, you need agents that work. This phase establishes the foundation: each agent gets a **system prompt** that defines its role, constraints, and reasoning approach, plus the **tools** it needs to act on real data rather than guessing from training knowledge alone. An agent with a vague system prompt or missing tools will produce plausible-sounding but wrong answers — no amount of monitoring or evaluation will compensate for a design that was wrong from the start.

For TireForge, this means creating an Anomaly Detection Agent that compares live sensor readings against known thresholds via `check_thresholds`, and a Fault Diagnosis Agent that reasons about root causes from those anomalies and recommends specific maintenance actions.

### 2. Monitor — See what’s actually happening

Once your agents are running, you need **observability**. This phase instruments every interaction as a distributed trace — capturing the full reasoning chain from user input through model call, tool invocations, and final response. AI agent failures are often silent: the agent returns a response that looks successful but misclassified, skipped a tool call, or produced a subtly wrong answer. Without traces, these failures are invisible — you have no way to diagnose what went wrong, measure latency regressions after a prompt change, or understand token costs at scale.

### 3. Evaluate — Measure whether outputs are actually correct

Monitoring tells you the agent is *running*. Evaluation tells you it’s doing the *right thing*. This phase runs your agents against a curated dataset of inputs with known expected outputs, then uses an LLM-as-judge to score each response on coherence and relevance. The result is a **repeatable, version-trackable quality score** — something you can compare before and after changing a system prompt, switching models, or adding a new tool. Spot-checking a handful of responses manually doesn’t scale and doesn’t catch regressions.

### 4. Deploy — Orchestrate agents into a production workflow

The final phase graduates you from running individual agents in scripts to building a **multi-agent pipeline** in the Microsoft Foundry portal. The agents are wired together in sequence — the first agent’s output becomes the second agent’s input — and the workflow is exposed as a testable, deployable endpoint with a run history. This is what production looks like: not a script you trigger manually, but an orchestrated system with a stable interface, backed by the monitoring and evaluation infrastructure you built in the previous phases.

For TireForge, this means moving from a script that checks 5 machines to a portal workflow that can scan an entire production floor’s sensor feed, with traces and evaluation scores that maintenance managers can inspect and trust before acting on a fault diagnosis.

---

This lifecycle — **Build → Monitor → Evaluate → Deploy** — is the production standard for AI agent systems. By the end of these challenges you’ll have experienced every phase hands-on and have a working, observable, evaluated, and deployed multi-agent system.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Microsoft Foundry                       │
│                                                         │
│  ┌─────────────────┐      ┌──────────────────────┐     │
│  │ Anomaly Agent   │      │  Fault Diagnosis     │     │
│  │ (+ tool:        │─────▶│  Agent               │     │
│  │  check_thresh.) │      │                      │     │
│  └────────┬────────┘      └──────────┬───────────┘     │
│           │                          │                  │
│           ▼                          ▼                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Factory Health Workflow                  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────────┐  ┌───────────────┐  ┌────────────┐  │
│  │ App Insights │  │  Evaluation   │  │  Tracing   │  │
│  └──────────────┘  └───────────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────┘
```
