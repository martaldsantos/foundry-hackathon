# Challenge 4: Production Workflow — Portal Track

## Overview

In this portal track you will explore the deployed agents, build a multi-agent
workflow in the Foundry visual designer, and test it directly from the portal.

---

## Step 1: Verify Agents Are Deployed

1. Open [https://ai.azure.com](https://ai.azure.com) (ensure **New Foundry** toggle is **On**)
2. Select your **tire-factory-project**
3. In the left sidebar → **Build** → **Agents**
4. Confirm both agents appear in the list:
   - `anomaly-detection-agent`
   - `fault-diagnosis-agent`

> If they are not listed, run `python challenge-4-deploy/sdk-track/solutions/deploy.py` first.

---

## Step 2: Test the Anomaly Detection Agent

1. Click **anomaly-detection-agent** to open it
2. In the **Playground** panel on the right, send this message:
   ```
   Check machines MX-001 and CP-003 for anomalies.
   ```
3. Watch the agent invoke the `check_thresholds` tool for each machine
4. Expected response: a structured report listing out-of-spec sensors with deviation percentages

Try also:
```
Check all machines: MX-001, EX-002, CP-003, CU-004, IS-005. Report every sensor out of spec.
```

---

## Step 3: Test the Fault Diagnosis Agent

1. Go back to **Agents** and open **fault-diagnosis-agent**
2. In the Playground, send:
   ```
   Machine CP-003 has the following anomalies:
   - vibration: 8.7 mm/s (max 5.0, 74% above max)
   - temperature: 97°C (max 85, 14.1% above max)
   Diagnose the fault and recommend maintenance actions.
   ```
3. Expected response structure:
   - **LIKELY CAUSE**: ...
   - **MAINTENANCE ACTIONS**: ...
   - **URGENCY**: IMMEDIATE / WITHIN 24H / MONITOR

---

## Step 4: Build the Workflow in the Portal

Now wire the two agents into a visual multi-agent workflow.

1. In the left sidebar → **Build** → **Workflows**
2. Click **+ New workflow**
3. In the workflow designer:
   - Click **+ Add step** → choose **Agent** → select `anomaly-detection-agent`
     - Input: `Run a full factory health check on all machines: MX-001, EX-002, CP-003, CU-004, IS-005.`
   - Click **+ Add step** → choose **Agent** → select `fault-diagnosis-agent`
     - Input: connect to the output of the previous step (use the **wire** between nodes)
4. Name the workflow: `factory-health-workflow`
5. Click **Save** then **Deploy**

---

## Step 5: Test the Workflow in the Portal Playground

1. Once deployed, open the workflow and click **Playground**
2. Send this test message:
   ```
   Run a full factory health check. Check all 5 machines for anomalies and diagnose any faults found.
   ```
3. Observe the workflow executing step-by-step:
   - The anomaly detection step runs first (you may see a "running…" indicator per step)
   - The fault diagnosis step runs next using the anomaly output as context
4. Review the final consolidated report in the response

---

## Step 6: Invoke the Portal Workflow from Python

Now invoke the same portal workflow from code with live streaming:

1. Add to your `.env` file:
   ```
   WORKFLOW_AGENT_NAME=factory-health-workflow
   ```
2. Run the solution:
   ```bash
   cd challenge-4-deploy/sdk-track
   python solutions/deploy.py
   ```
3. In the terminal you will see each workflow step appear in real time:
   ```
   === Invoking Portal Workflow: factory-health-workflow ===
     --> Step: anomaly_scan
         [completed] anomaly_scan
     --> Step: fault_diagnosis
         [completed] fault_diagnosis
   <final report streamed here>
   ```

---

## Step 7: View Run History and Traces

1. In the portal, open your workflow → **Run history** tab
2. Click on the latest run to see the execution timeline — each agent step, duration, and output
3. Navigate to **Tracing** (left sidebar → **Operate**) to see the full distributed trace
   spanning both agent conversations

