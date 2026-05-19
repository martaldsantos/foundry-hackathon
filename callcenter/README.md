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
