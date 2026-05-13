# Challenge 1: Build Agents — Portal Track

## Step-by-Step Instructions

### Step 1: Navigate to the Agents Section

1. Open [https://ai.azure.com](https://ai.azure.com) (ensure the **New Foundry** toggle is **On**)
2. Select your **tire-factory-project**
3. In the left sidebar, click **Agents** (under the "Build" section)
4. Click **+ New agent**

### Step 2: Create the Anomaly Detection Agent

1. In the agent creation panel, set the following:
   - **Agent name**: `anomaly-detection-agent`
   - **Model**: Select `gpt-5.1` from the model dropdown
   - **Instructions** (paste this into the Instructions box):

   ```
   You are an industrial anomaly detection agent for TireForge Industries tire manufacturing plant.

   Your job is to analyze sensor readings from factory machines and determine if any readings are outside their normal operating thresholds.

   For each machine you analyze, you should:
   1. Compare each sensor reading (temperature, pressure, vibration, RPM) against its defined thresholds
   2. Flag any readings that are ABOVE the max threshold or BELOW the min threshold
   3. Classify the machine status:
      - "normal" if all readings are within thresholds
      - "warning" if 1 reading is out of spec
      - "critical" if 2+ readings are out of spec OR any single reading is >20% beyond threshold

   Always respond with a structured analysis including:
   - Machine name and ID
   - Each sensor reading vs. its threshold
   - Whether each is IN SPEC or OUT OF SPEC
   - Overall status classification
   - Urgency level (low/medium/high)
   ```

2. Click **Create** to save the agent

### Step 3: Add Knowledge (File Upload)

1. In the agent detail view, scroll to the **Knowledge** section
2. Click **+ Add** → **Files**
3. Upload `sensor_data.json` from the `challenge-1-build/` folder
4. Wait for the file to be indexed (you'll see a green checkmark when ready)

### Step 4: Test the Anomaly Detection Agent

1. In the agent detail view, click **Test** in the top action bar (or click the agent playground icon)
2. You'll enter the Agent playground — make sure `anomaly-detection-agent` is selected
3. In the message box, type:

   ```
   Analyze all 5 machines from the sensor data and tell me which ones have anomalies. 
   For each anomaly, explain what reading is out of spec and by how much.
   ```

4. Click **Send**
5. Verify the agent correctly identifies:
   - **Mixer (MX-001)**: temperature at 92.3°C exceeds max of 90°C, vibration at 4.8 mm/s exceeds max of 4.5 mm/s → Warning
   - **Curing Press (CP-003)**: temperature at 198.5°C exceeds max of 180°C, pressure at 18.2 bar exceeds max of 16.0 bar, vibration at 7.3 mm/s exceeds max of 3.0 mm/s → Critical
   - **Inspection Station (IS-005)**: vibration at 5.2 mm/s exceeds max of 4.0 mm/s → Warning

### Step 5: Create the Fault Diagnosis Agent

1. Navigate back to **Agents** in the left sidebar
2. Click **+ New agent**
3. Set the following:
   - **Agent name**: `fault-diagnosis-agent`
   - **Model**: Select `gpt-5.1`
   - **Instructions**:

   ```
   You are an industrial fault diagnosis agent for TireForge Industries tire manufacturing plant.

   When given information about a machine with anomalous sensor readings, your job is to:
   1. Analyze the pattern of anomalies (which sensors are out of spec, by how much, in what combination)
   2. Determine the most likely root cause based on industrial engineering knowledge
   3. Recommend a specific maintenance action
   4. Estimate urgency (immediate shutdown required / schedule maintenance within 24h / monitor closely)

   Consider these common fault patterns:
   - High temperature + high pressure → possible blockage or valve failure
   - High vibration alone → bearing wear, misalignment, or imbalance
   - High temperature + high vibration → lubrication failure or friction buildup
   - All readings high → systemic failure, recommend immediate shutdown

   Always provide:
   - Likely root cause (1-2 sentences)
   - Recommended action (specific and actionable)
   - Urgency level with justification
   - Any safety warnings if applicable
   ```

4. Click **Create**
5. Add the same `sensor_data.json` file under **Knowledge** → **+ Add** → **Files**

### Step 6: Test the Fault Diagnosis Agent

1. Click **Test** to open the Agent playground with `fault-diagnosis-agent`
2. Send:

   ```
   The curing press (CP-003) has these anomalies:
   - Temperature: 198.5°C (max threshold: 180°C) — 10.3% over
   - Pressure: 18.2 bar (max threshold: 16.0 bar) — 13.8% over
   - Vibration: 7.3 mm/s (max threshold: 3.0 mm/s) — 143% over

   Last maintenance was 2026-03-20 (almost 2 months ago).
   Diagnose the fault and recommend an action.
   ```

3. Verify the agent provides a reasonable diagnosis (likely suggests overdue maintenance, possible seal/valve issue, recommends immediate inspection or shutdown)

## ✅ Done!

Both agents are created and working. Move on to [Challenge 2: Deploy & Expose](../../challenge-2-deploy/).
