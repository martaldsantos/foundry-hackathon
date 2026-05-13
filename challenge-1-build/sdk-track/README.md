# Challenge 1: Build Agents — SDK Track

## Step-by-Step Instructions

### Overview

You'll implement two agents in `agents.py`:
1. **AnomalyDetectionAgent** — Compares sensor readings against thresholds
2. **FaultDiagnosisAgent** — Diagnoses root causes and recommends actions

The file has stubs with TODOs. Your job is to fill them in.

### Step 1: Understand the Sensor Data

Open `../sensor_data.json` and familiarize yourself with the structure:
- 5 machines, each with readings (temperature, pressure, vibration, rpm)
- Each reading has a threshold (min/max)
- 2 machines are in "warning", 1 in "critical", 2 "normal"

### Step 2: Fill in the TODOs

Open `agents.py` and complete:

1. **`check_thresholds` function** — Already implemented as a tool function. Read through it to understand how it works.

2. **`AnomalyDetectionAgent.create()`** — Fill in:
   - The system prompt (instructions for how the agent should analyze sensor data)
   - The tool definition that lets the agent call `check_thresholds`

3. **`AnomalyDetectionAgent.run(input_text)`** — Fill in:
   - Create a thread, add the user message, run the agent, return the response

4. **`FaultDiagnosisAgent.create()`** — Fill in:
   - The system prompt (instructions for fault diagnosis and recommendations)

5. **`FaultDiagnosisAgent.run(input_text)`** — Fill in:
   - Same pattern as AnomalyDetectionAgent

### Step 3: Run and Test

```bash
cd challenge-1-build/sdk-track
python agents.py
```

The `main()` function at the bottom will:
1. Create both agents
2. Run the anomaly detector on all machines
3. Feed the anomalies into the fault diagnosis agent
4. Print results
5. Clean up

### Tips

- The `check_thresholds` tool reads from `sensor_data.json` and returns which readings are out of spec
- System prompts should be specific about output format
- Don't forget to handle the tool call flow: when the agent wants to call a tool, you need to submit the tool output back

### Expected Output

```
=== Anomaly Detection Agent ===
Analyzing all machines...

Machine: mixer (MX-001) — WARNING
  ⚠️ temperature: 92.3°C (max: 90°C)
  ⚠️ vibration: 4.8 mm/s (max: 4.5 mm/s)

Machine: curing_press (CP-003) — CRITICAL
  🔴 temperature: 198.5°C (max: 180°C)
  🔴 pressure: 18.2 bar (max: 16.0 bar)
  🔴 vibration: 7.3 mm/s (max: 3.0 mm/s)

Machine: inspection_station (IS-005) — WARNING
  ⚠️ vibration: 5.2 mm/s (max: 4.0 mm/s)

=== Fault Diagnosis Agent ===
Diagnosing critical machine: curing_press...

Diagnosis: [agent's analysis here]
```

## ✅ Done!

Both agents are working via the SDK. Move on to [Challenge 2: Deploy & Expose](../../challenge-2-deploy/).
