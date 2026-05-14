# Challenge 4: Production Workflow

Build a multi-agent orchestration workflow for TireForge Industries and take it to production.

## Scenario

The individual agents you built in Challenge 1 are valuable — but in production, agents need to work
**together** as an automated pipeline. In this challenge you wire the two agents into a full
factory health workflow, run it from code, then build and test it visually in the Foundry portal.

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
run_anomaly_scan()          <-- Anomaly Detection Agent checks all 5 machines
        |
        v (for each machine with anomalies)
run_fault_diagnosis()       <-- Fault Diagnosis Agent diagnoses root cause
        |
        v
print_factory_report()      <-- Consolidated Health Report
```

---

## Part 1 — SDK: Build and Run the Python Workflow

### Step 1: Review the implementation

Open [deploy.py](./deploy.py) and review:

- **`ensure_agents_deployed()`** — lists existing agents, creates `anomaly-detection-agent` and `fault-diagnosis-agent` if not present
- **`run_anomaly_scan()`** — calls the anomaly agent, handles the `check_thresholds` function call loop
- **`run_fault_diagnosis()`** — calls the diagnosis agent for each affected machine
- **`run_factory_health_workflow()`** — orchestrates all steps and returns the consolidated report

### Step 2: Run the workflow

```bash
cd factory/challenge-4-deploy
python deploy.py
```

Expected output:
```
=== Step 1: Ensure Agents Are Deployed ===
  Found existing: anomaly-detection-agent
  Found existing: fault-diagnosis-agent

=== Step 2a: Anomaly Scan ===
  CP-003 CRITICAL: vibration 143% above max, pressure 13.8% above max, temperature 10.3% above max
  MX-001 WARNING: vibration 6.7% above max, temperature 2.6% above max
  IS-005 WARNING: vibration 30% above max
  ...

=== Step 2b: Fault Diagnosis ===
  Diagnosing CP-003...
  Diagnosing MX-001...
  Diagnosing IS-005...

TIREFORGE FACTORY HEALTH REPORT
  Machines checked   : 5
  Machines affected  : 2
  ...
```

---

## Part 2 — Portal: Build and Test the Visual Workflow

### Step 3: Verify agents are deployed in the portal

1. Open [https://ai.azure.com](https://ai.azure.com) (ensure **New Foundry** toggle is **On**)
2. Select your **tire-factory-project**
3. Left sidebar → **Build** → **Agents**
4. Confirm both agents appear:
   - `anomaly-detection-agent`
   - `fault-diagnosis-agent`

### Step 4: Test the Anomaly Detection Agent

1. Click **anomaly-detection-agent** → **Playground**
2. Send:
   ```
   Check machines MX-001 and CP-003 for anomalies.
   ```
3. Watch the `check_thresholds` tool call fire for each machine
4. Also try:
   ```
   Check all machines: MX-001, EX-002, CP-003, CU-004, IS-005. Report every sensor out of spec.
   ```

### Step 5: Test the Fault Diagnosis Agent

1. Left sidebar → **Agents** → **fault-diagnosis-agent** → **Playground**
2. Send:
   ```
   Machine CP-003 has the following anomalies:
  - temperature: 198.5 celsius (max 180, 10.3% above max)
  - pressure: 18.2 bar (max 16.0, 13.8% above max)
  - vibration: 7.3 mm/s (max 3.0, 143% above max)
   Diagnose the fault and recommend maintenance actions.
   ```
3. Expected structure: **LIKELY CAUSE** / **MAINTENANCE ACTIONS** / **URGENCY**

### Step 6: Build the workflow in the portal designer

1. Left sidebar → **Build** → **Workflows** → **+ New workflow**
2. In the visual designer:
   - **+ Add step** → Agent → `anomaly-detection-agent`
     - Input: `Run a full factory health check on all machines: MX-001, EX-002, CP-003, CU-004, IS-005.`
   - **+ Add step** → Agent → `fault-diagnosis-agent`
     - Wire the output of the first step as input to this step
3. Name it `factory-health-workflow`
4. Click **Save** then **Deploy**

### Step 7: Test the workflow in the portal playground

1. Open the workflow → **Playground**
2. Send:
   ```
   Run a full factory health check. Check all 5 machines for anomalies and diagnose any faults found.
   ```
3. Watch the steps execute in sequence — anomaly scan first, then fault diagnosis
4. Review the final consolidated report

### Step 8: Invoke the portal workflow from Python (streaming)

Add to your `.env`:
```
WORKFLOW_AGENT_NAME=factory-health-workflow
```

Re-run the script — Part B activates automatically:
```bash
python deploy.py
```

You will see each workflow step appear live in the terminal:
```
=== Invoking Portal Workflow: factory-health-workflow ===
  --> Step: anomaly_scan
      [completed] anomaly_scan
  --> Step: fault_diagnosis
      [completed] fault_diagnosis
<final report streamed here>
```

### Step 9: View run history and traces

1. Portal → your workflow → **Run history** tab
2. Click the latest run to see the execution timeline — each step, duration, and output
3. Left sidebar → **Operate** → **Tracing** to see the full distributed trace across both agent conversations

---

## Success Criteria

- [ ] Python workflow runs end-to-end: anomaly scan → diagnosis → factory health report
- [ ] Both agents visible in the Foundry portal as persistent assets
- [ ] Visual workflow created in the portal and tested in its playground
- [ ] Portal workflow invoked from Python with live step streaming
