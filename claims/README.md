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
- ~20 minutes for infrastructure provisioning (run `challenge-0-setup/deploy.sh` from the repo root first!)

## Structure

All challenges are Python SDK-based. Challenge 4 also walks you through the Foundry portal to build and test the multi-agent workflow visually.

## Challenges

| # | Challenge | Duration | What You'll Do |
|---|-----------|----------|----------------|
| 0 | [Setup](./challenge-0-setup/README.md) | 20 min | Provision resources, verify auth |
| 1 | [Build Agents](./challenge-1-build/README.md) | 35 min | Create claims triage & decision agents |
| 2 | [Monitor](./challenge-2-monitor/README.md) | 20 min | Enable tracing, explore App Insights |
| 3 | [Evaluate](./challenge-3-evaluate/README.md) | 25 min | Run evaluations, interpret quality metrics |
| 4 | [Workflow](./challenge-4-deploy/README.md) | 20 min | Build a multi-agent workflow: triage → decision → claims report |

## The Agent Lifecycle

These four challenges follow the same arc that engineering teams use when taking AI agent systems to production. Each phase builds directly on the previous one — skipping any of them leaves a gap that will surface as an incident in production.

### 1. Build — Define what your agents can do

Before you can run, monitor, or evaluate anything, you need agents that work. This phase establishes the foundation: each agent gets a **system prompt** that defines its role, constraints, and reasoning approach, plus the **tools** it needs to act on real data rather than guessing from training knowledge alone. An agent with a vague system prompt or missing tools will produce plausible-sounding but wrong answers — no amount of monitoring or evaluation will compensate for a design that was wrong from the start.

For ClaimSight, this means creating a Claims Triage Agent that assesses incoming claim metrics against acceptable thresholds via `assess_claim`, and a Claims Decision Agent that translates those risk flags into concrete actions — approve, investigate, request documents, or deny.

### 2. Monitor — See what’s actually happening

Once your agents are running, you need **observability**. This phase instruments every interaction as a distributed trace — capturing the full reasoning chain from user input through model call, tool invocations, and final response. AI agent failures are often silent: the agent returns a response that looks successful but misclassified, skipped a tool call, or produced a subtly wrong answer. Without traces, these failures are invisible — you have no way to diagnose what went wrong, measure latency regressions after a prompt change, or understand token costs at scale.

### 3. Evaluate — Measure whether outputs are actually correct

Monitoring tells you the agent is *running*. Evaluation tells you it’s doing the *right thing*. This phase runs your agents against a curated dataset of inputs with known expected outputs, then uses an LLM-as-judge to score each response on coherence and relevance. The result is a **repeatable, version-trackable quality score** — something you can compare before and after changing a system prompt, switching models, or updating the policy documents in your knowledge base. Spot-checking a handful of responses manually doesn’t scale and doesn’t catch regressions.

### 4. Deploy — Orchestrate agents into a production workflow

The final phase graduates you from running individual agents in scripts to building a **multi-agent pipeline** in the Microsoft Foundry portal. The agents are wired together in sequence — the first agent’s output becomes the second agent’s input — and the workflow is exposed as a testable, deployable endpoint with a run history. This is what production looks like: not a script you trigger manually, but an orchestrated system with a stable interface, backed by the monitoring and evaluation infrastructure you built in the previous phases.

For ClaimSight, this means moving from a script that triages 5 test claims to a portal workflow that can process an entire claims batch, with full trace history and quality scores that compliance teams and auditors can inspect alongside every approve or deny decision.

---

This lifecycle — **Build → Monitor → Evaluate → Deploy** — is the production standard for AI agent systems. By the end of these challenges you’ll have experienced every phase hands-on and have a working, observable, evaluated, and deployed multi-agent system.

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


## Next Steps

Completing these challenges gives you a working multi-agent system with observability and evaluation in place. Here are the directions you can take it further:

**Deploy as a hosted agent endpoint**
Microsoft Foundry can host your agents as persistent, scalable API endpoints — no infrastructure to manage. Once hosted, your claims intake system can submit new claims directly to the Triage Agent and receive a structured decision (approve / investigate / request documents / deny) without any manual triage step.

**Add more tools to your agents**
The `assess_claim` function in this lab uses local mock data. In production you'd replace it with tools that call real systems:
- A `fetch_policy` tool querying your policy management system for the exact coverage terms, exclusions, and limits applicable to a specific claim
- A `check_fraud_database` tool querying a fraud intelligence service for known patterns matching the claimant's history
- A `request_documents` tool that automatically triggers a document request workflow in your DMS when the agent recommends it

**Build a knowledge base**
Upload ClaimSight's insurance policy documents, regulatory compliance guidelines, and fraud pattern library to a Microsoft Foundry knowledge base. Attach it to the Claims Decision Agent as a File Search tool so its recommendations cite actual policy language — producing decisions that are auditable and defensible to regulators.

**Integrate evaluations into CI/CD**
Run your evaluation dataset automatically on every pull request or deployment. If the coherence or relevance score drops below a threshold (e.g. 3.5 out of 5), block the release. In a regulated industry, this isn't just good practice — it's the kind of quality gate that compliance and audit teams expect to see documented.

**Explore advanced agent patterns**
- **Parallelise** triage across all incoming claims simultaneously instead of sequentially
- **Add confidence thresholds** — if the Triage Agent's fraud risk assessment falls in an ambiguous range, route to a senior adjuster rather than passing to the Decision Agent automatically
- **Human-in-the-loop** — for high-value claims (above a configurable threshold), always require human adjuster sign-off before the Decision Agent's recommendation is acted on

**Fine-tune for your domain**
Use your evaluation results to identify systematic errors — claim types the agent consistently misjudges or fraud indicators it underweights. Use those cases to refine system prompts, add targeted few-shot examples, or fine-tune the underlying model on ClaimSight's historical claim decisions.
