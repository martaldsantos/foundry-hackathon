# Challenge 4: Production Workflow — SDK Track

## Overview

Wire the two TireForge agents into a production-ready multi-agent workflow.

## File

`deploy.py` — fill in the TODOs to complete the workflow.

## Steps

### Step 1 — `ensure_agents_deployed()`
- List existing agents with `client.agents.list()`
- Create `anomaly-detection-agent` (with `check_thresholds` FunctionTool) if not present
- Create `fault-diagnosis-agent` (no tools) if not present
- Agents are versioned assets — they persist across runs

### Step 2a — `run_anomaly_scan(anomaly_agent_name)`
- Create a conversation and call the anomaly agent
- **Handle the function call loop**: the agent will call `check_thresholds` for each machine
  - Check `item.type == "function_call"` in `response.output`
  - Call `check_thresholds(machine_id)` locally for each call
  - Submit results back as `FunctionCallOutput` list
- Return `response.output_text` when the loop ends

### Step 2b — `run_fault_diagnosis(diagnosis_agent_name, machine_id, anomalies)`
- Build a prompt describing the machine's anomalies
- Call the fault-diagnosis-agent (no function call loop needed)
- Return the diagnosis text

### Step 3 — `run_factory_health_workflow(anomaly_agent, diagnosis_agent)`
- Call `run_anomaly_scan()` for all machines
- Use `check_thresholds()` locally to find which machines have anomalies
- Call `run_fault_diagnosis()` for each affected machine
- Return the consolidated report dict

## Run

```bash
cd challenge-4-deploy/sdk-track
python deploy.py
```

## Solution

```bash
python solutions/deploy.py
```

---

## Bonus — Part B: Portal Workflow (visible in Foundry Workflows tab)

The Python orchestration above calls the agents step-by-step from code. Azure AI Foundry also has a **visual Workflow designer** that creates a multi-agent pipeline you can see and trigger directly from the portal.

### Create the workflow in the portal

1. Open [https://ai.azure.com](https://ai.azure.com) → your project → **Build** → **Workflows**
2. Click **New workflow**
3. Add `anomaly-detection-agent` as the first step
4. Add `fault-diagnosis-agent` as the second step, wired to receive the anomaly output
5. Name it (e.g. `factory-health-workflow`) and click **Deploy**

### Set the environment variable

```bash
# In your .env file:
WORKFLOW_AGENT_NAME=factory-health-workflow
```

### Invoke from Python (streaming)

The `run_portal_workflow()` function in `deploy.py` calls the portal-created workflow and streams the response. As each step in the pipeline runs, a `workflow_action` event is emitted — you see the execution live:

```
=== Invoking Portal Workflow: factory-health-workflow ===
  --> Step: anomaly_scan
      [completed] anomaly_scan
  --> Step: fault_diagnosis_CP-003
      [completed] fault_diagnosis_CP-003
<final report text>
```

Re-run `deploy.py` after setting `WORKFLOW_AGENT_NAME` — Part B will execute automatically.
