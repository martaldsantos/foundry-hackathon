# Challenge 4: Production Workflow

Build a multi-agent orchestration workflow for NovaTel Communications and take it to production.

## Scenario

The individual agents you built in Challenge 1 are valuable — but in production, agents need to work
**together** as an automated pipeline. In this challenge you wire the two agents into a full
call center triage workflow, run it from code, then build and test it visually in the Foundry portal.

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
run_intent_classification()     <-- Intent Agent classifies all 7 calls
        |
        v (for each high-priority call)
run_resolution_advisory()       <-- Resolution Agent recommends actions
        |
        v
print_shift_report()            <-- Consolidated Shift Report
```

---

## Part 1 — SDK: Build and Run the Python Workflow

### Step 1: Review the implementation

Open [deploy.py](./deploy.py) and review:

- **`ensure_agents_deployed()`** — lists existing agents, creates `intent-classification-agent` and `resolution-advisor-agent` if not present
- **`run_intent_classification()`** — calls the intent agent, handles the `lookup_customer` function call loop
- **`run_resolution_advisory()`** — calls the resolution agent for each high-priority call
- **`run_call_center_workflow()`** — orchestrates all steps and returns the consolidated report

### Step 2: Run the workflow

```bash
cd callcenter/challenge-4-deploy
python deploy.py
```

Expected output:
```
=== Step 1: Ensure Agents Are Deployed ===
  Found existing: intent-classification-agent
  Found existing: resolution-advisor-agent

=== Step 2a: Intent Classification ===
  CALL-001: billing_dispute (HIGH) — frustrated, retention risk HIGH
  CALL-002: technical_issue (HIGH) — frustrated, retention risk MEDIUM
  CALL-003: cancellation (HIGH) — neutral, retention risk HIGH
  CALL-004: upsell_opportunity (MEDIUM) — positive, retention risk LOW
  CALL-005: account_support (LOW) — frustrated, retention risk LOW
  CALL-006: billing_dispute (HIGH) — frustrated, retention risk MEDIUM
  CALL-007: security_concern (CRITICAL) — anxious, retention risk MEDIUM

=== Step 2b: Resolution Advisory (High-Priority Calls) ===
  Resolving CALL-007 (security_concern)...
  Resolving CALL-001 (billing_dispute)...
  Resolving CALL-003 (cancellation)...

NOVATEL CALL CENTER — SHIFT REPORT
  Total calls processed  : 7
  Critical priority      : 1
  High priority          : 2
  ...
```

---

## Part 2 — Portal: Build and Test the Visual Workflow

### Step 3: Verify agents are deployed in the portal

1. Open [https://ai.azure.com](https://ai.azure.com) (ensure **New Foundry** toggle is **On**)
2. Select your project
3. Left sidebar → **Build** → **Agents**
4. Confirm both agents appear:
   - `intent-classification-agent`
   - `resolution-advisor-agent`

### Step 4: Test the Intent Classification Agent

1. Click **intent-classification-agent** → **Playground**
2. Send:
   ```
   Classify CALL-001 and CALL-007. What are their intents and priority levels?
   ```
3. Watch the `lookup_customer` tool call fire for each call
4. Also try:
   ```
   Classify all calls: CALL-001 through CALL-007. Report intent, priority, sentiment, and retention risk.
   ```

### Step 5: Test the Resolution Advisor Agent

1. Left sidebar → **Agents** → **resolution-advisor-agent** → **Playground**
2. Send:
   ```
   Call CALL-007 from Emma Wilson (basic tier, 8 months):
   - Intent: security_concern
   - Priority: critical
   - Sentiment: anxious
   - Context: Received verification codes she didn't request, unfamiliar device on account.
   Recommend resolution strategy and immediate actions.
   ```
3. Expected structure: **RECOMMENDED ACTION** / **SCRIPT SUGGESTION** / **ESCALATION** / **OFFERS** / **FOLLOW-UP**

### Step 6: Build the workflow in the portal designer

1. Left sidebar → **Build** → **Workflows** → **+ New workflow**
2. In the visual designer:
   - **+ Add step** → Agent → `intent-classification-agent`
     - Input: `Classify all incoming calls and identify any critical or high-priority items.`
   - **+ Add step** → Agent → `resolution-advisor-agent`
     - Wire the output of the first step as input to this step
3. Name it `call-center-triage-workflow`
4. Click **Save** then **Deploy**

### Step 7: Test the workflow in the portal playground

1. Open the workflow → **Playground**
2. Send:
   ```
   Process all incoming calls. Classify each one and provide resolution recommendations for high-priority items.
   ```
3. Watch the steps execute in sequence — classification first, then resolution advisory
4. Review the final consolidated shift report

### Step 8: Invoke the portal workflow from Python (streaming)

Add to your `.env`:
```
WORKFLOW_AGENT_NAME=call-center-triage-workflow
```

Re-run the script — Part B activates automatically:
```bash
python deploy.py
```

You will see each workflow step appear live in the terminal:
```
=== Invoking Portal Workflow: call-center-triage-workflow ===
  --> Step: intent_classification
      [completed] intent_classification
  --> Step: resolution_advisory
      [completed] resolution_advisory
<final report streamed here>
```

### Step 9: View run history and traces

1. Portal → your workflow → **Run history** tab
2. Click the latest run to see the execution timeline — each step, duration, and output
3. Left sidebar → **Operate** → **Tracing** to see the full distributed trace across both agent conversations

---

## Success Criteria

- [ ] Python workflow runs end-to-end: classification → resolution → shift report
- [ ] Both agents visible in the Foundry portal as persistent assets
- [ ] Visual workflow created in the portal and tested in its playground
- [ ] Portal workflow invoked from Python with live step streaming
