# 📞 Scenario: Call Center Triage — NovaTel Communications

## Background

**NovaTel Communications** is a telecom provider handling hundreds of customer calls daily across their support center. Today's queue has 7 active calls spanning different issue types:

- **CALL-001** — Maria Gonzalez (Premium, 3 years) — Unexpected charge dispute
- **CALL-002** — James Liu (Basic, 4 months) — Internet dropping repeatedly
- **CALL-003** — Priya Sharma (Premium, 18 months) — Wants to cancel (moving)
- **CALL-004** — Robert Chen (Business, 2 years) — Adding 7 phone lines
- **CALL-005** — Sarah Mitchell (Basic, 5 years) — Can't navigate new app
- **CALL-006** — David Park (Premium, 1 year) — Charged for returned device
- **CALL-007** — Emma Wilson (Basic, 8 months) — Suspected account hack

## Your Mission

Build an AI agent system that:

1. **Classifies intent** — Determines what each customer needs (billing, tech, cancellation, upsell, support, security)
2. **Advises resolution** — Recommends the best handling strategy based on customer context
3. **Produces a shift report** — Consolidated triage with prioritized action items

## Challenges

| # | Challenge | What You'll Do | Time |
|---|-----------|---------------|------|
| 0 | [Setup](./challenge-0-setup/README.md) | Deploy Microsoft Foundry infrastructure | 20 min |
| 1 | [Build Agents](./challenge-1-build/README.md) | Create Intent Classification + Resolution Advisor agents | 35 min |
| 2 | [Monitor](./challenge-2-monitor/README.md) | Enable GenAI tracing with Application Insights | 20 min |
| 3 | [Evaluate](./challenge-3-evaluate/README.md) | Run systematic quality evaluations | 25 min |
| 4 | [Production Workflow](./challenge-4-deploy/README.md) | Multi-agent orchestration + portal workflow | 20 min |

## The Agent Lifecycle

These four challenges follow the same arc that engineering teams use when taking AI agent systems to production. Each phase builds directly on the previous one — skipping any of them leaves a gap that will surface as an incident in production.

### 1. Build — Define what your agents can do

Before you can run, monitor, or evaluate anything, you need agents that work. This phase establishes the foundation: each agent gets a **system prompt** that defines its role, constraints, and reasoning approach, plus the **tools** it needs to act on real data rather than guessing from training knowledge alone. An agent with a vague system prompt or missing tools will produce plausible-sounding but wrong answers — no amount of monitoring or evaluation will compensate for a design that was wrong from the start.

For NovaTel, this means creating an Intent Classification Agent that knows the difference between a cancellation risk and a billing dispute, and a Resolution Advisor that knows which retention offers apply to which customer tiers — grounded in real account data via `lookup_customer`.

### 2. Monitor — See what’s actually happening

Once your agents are running, you need **observability**. This phase instruments every interaction as a distributed trace — capturing the full reasoning chain from user input through model call, tool invocations, and final response. AI agent failures are often silent: the agent returns a response that looks successful but misclassified, skipped a tool call, or produced a subtly wrong answer. Without traces, these failures are invisible — you have no way to diagnose what went wrong, measure latency regressions after a prompt change, or understand token costs at scale.

### 3. Evaluate — Measure whether outputs are actually correct

Monitoring tells you the agent is *running*. Evaluation tells you it’s doing the *right thing*. This phase runs your agents against a curated dataset of inputs with known expected outputs, then uses an LLM-as-judge to score each response on coherence and relevance. The result is a **repeatable, version-trackable quality score** — something you can compare before and after changing a system prompt, switching models, or adding a new tool. Spot-checking a handful of responses manually doesn’t scale and doesn’t catch regressions.

### 4. Deploy — Orchestrate agents into a production workflow

The final phase graduates you from running individual agents in scripts to building a **multi-agent pipeline** in the Microsoft Foundry portal. The agents are wired together in sequence — the first agent’s output becomes the second agent’s input — and the workflow is exposed as a testable, deployable endpoint with a run history. This is what production looks like: not a script you trigger manually, but an orchestrated system with a stable interface, backed by the monitoring and evaluation infrastructure you built in the previous phases.

For NovaTel, this means moving from a script that processes 7 test calls to a portal workflow that can triage an entire shift’s queue, with full trace history and quality scores that supervisors can inspect and trust.

---

This lifecycle — **Build → Monitor → Evaluate → Deploy** — is the production standard for AI agent systems. By the end of these challenges you’ll have experienced every phase hands-on and have a working, observable, evaluated, and deployed multi-agent system.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Microsoft Foundry                       │
│                                                         │
│  ┌─────────────────┐      ┌──────────────────────┐     │
│  │ Intent Agent    │      │  Resolution Advisor  │     │
│  │ (+ tool:        │─────▶│  Agent               │     │
│  │  lookup_cust.)  │      │                      │     │
│  └────────┬────────┘      └──────────┬───────────┘     │
│           │                          │                  │
│           ▼                          ▼                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │       Call Center Triage Workflow                │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌──────────────┐  ┌───────────────┐  ┌────────────┐  │
│  │ App Insights │  │  Evaluation   │  │  Tracing   │  │
│  └──────────────┘  └───────────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────┘
```
