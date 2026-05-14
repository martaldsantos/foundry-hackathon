# Challenge 4: Production Workflow

Build a multi-agent orchestration workflow for ClaimSight Insurance and take it to production.

## Scenario

The individual agents you built in Challenge 1 are valuable — but in production, agents need to work
**together** as an automated pipeline. In this challenge you wire the two agents into a full
claims processing workflow, run it from code, then build and test it visually in the Foundry portal.

## Learning Objectives

- Deploy persistent production agents (create once, reuse forever)
- Orchestrate multiple agents step-by-step in a Python workflow
- Build the same workflow visually in the Foundry portal
- Invoke the portal workflow from Python with live streaming
- View run history and traces in the portal

## The Workflow

```
ensure_agents_deployed()
        |
        v
run_claims_triage()             <-- Claims Triage Agent assesses all 5 claims
        |
        v (for each flagged claim)
run_claims_decision()           <-- Claims Decision Agent recommends action
        |
        v
print_claims_report()           <-- Consolidated Claims Processing Report
```

---

## Part 1 — SDK: Build and Run the Python Workflow

### Step 1: Review the implementation

Open [deploy.py](./deploy.py) and review:

- **`ensure_agents_deployed()`** — lists existing agents, creates `claims-triage-agent` and `claims-decision-agent` if not present
- **`run_claims_triage()`** — calls the triage agent, handles the `assess_claim` function call loop
- **`run_claims_decision()`** — calls the decision agent for each flagged claim
- **`run_claims_workflow()`** — orchestrates all steps and returns the consolidated report

### Step 2: Run the workflow

```bash
cd claims/challenge-4-deploy
python deploy.py
```

Expected output:
```
=== Step 1: Ensure Agents Are Deployed ===
  Found existing: claims-triage-agent
  Found existing: claims-decision-agent

=== Step 2a: Claims Triage ===
  CLM-001 CRITICAL: fraud_risk_score 64% above max, damage_vs_estimate_match 25.7% below min
  CLM-003 WARNING: completeness 25% below min
  CLM-005 WARNING: fraud_risk_score 16% above max, damage_vs_estimate_match 8.6% below min
  ...

=== Step 2b: Claims Decisions ===
  Deciding on CLM-001...
  Deciding on CLM-003...
  Deciding on CLM-005...

CLAIMSIGHT INSURANCE — CLAIMS PROCESSING REPORT
  Claims assessed    : 5
  Claims flagged     : 3
  ...
```

---

## Part 2 — Portal: Build the Workflow Visually

### Step 3: Create the workflow in Foundry portal

1. Open the [Azure AI Foundry portal](https://ai.azure.com)
2. Navigate to **Build** → **Workflows** → **New workflow**
3. Add two steps:
   - Step 1: `claims-triage-agent` — "Assess all claims and report flags"
   - Step 2: `claims-decision-agent` — "For each flagged claim, recommend an action"
4. Deploy the workflow and note the agent name

### Step 4: Invoke from Python

Set `WORKFLOW_AGENT_NAME=<your-workflow-name>` in `.env`, then re-run:

```bash
python deploy.py
```

The portal workflow will execute with streaming output showing each step.

## Success Criteria

- [ ] Both agents deployed and visible in the Foundry portal
- [ ] Python workflow produces a consolidated claims report
- [ ] Portal workflow executes and streams results
- [ ] You can see the workflow run history in the portal
