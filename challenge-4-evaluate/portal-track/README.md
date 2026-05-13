# Challenge 4: Evaluate — Portal Track

## Step-by-Step Instructions

### Step 1: Navigate to Evaluations in Foundry

1. Open [https://ai.azure.com](https://ai.azure.com) (ensure **New Foundry** toggle is **On**)
2. Select your **tire-factory-project**
3. In the left sidebar, click **Evaluation** (under the "Operate" section)
4. Click **+ New evaluation**

### Step 2: Configure the Evaluation

1. **What do you want to evaluate?**: Select **Agent**
2. **Select agent**: Choose your `anomaly-detection-agent`
3. Click **Next**

### Step 3: Upload the Test Dataset

1. Under **Test data**, click **Upload file**
2. Upload `evaluation_dataset.json` from the `challenge-4-evaluate/` folder
3. Map the columns:
   - **Input column**: Select `input`
   - **Expected output column**: Select `expected_output`
4. Click **Next**

### Step 4: Select Evaluators

Select the following built-in evaluators:

1. **Task Adherence** ✅
   - Measures if the agent's response actually addresses what was asked
   - Scale: 1-5 (5 = perfectly addresses the task)

2. **Coherence** ✅
   - Measures if the response is logically consistent and well-structured
   - Scale: 1-5 (5 = perfectly coherent)

3. **Groundedness** ✅ (optional)
   - Measures if the response is factually grounded in the provided context
   - Scale: 1-5 (5 = fully grounded)

4. Click **Next**

### Step 5: Run the Evaluation

1. Review your configuration
2. Click **Submit**
3. Wait for the evaluation to complete (usually 2-5 minutes for 10 rows)

### Step 6: Interpret Results

Once complete, you'll see:

#### Aggregate Metrics
- **Average Task Adherence**: Target ≥ 4.0
- **Average Coherence**: Target ≥ 4.0
- **Average Groundedness**: Target ≥ 3.5

#### Per-Row Results
1. Click on individual rows to see:
   - The input that was sent
   - The agent's actual response
   - The expected output
   - Scores per evaluator
   - Evaluator reasoning (why it gave that score)

### Step 7: Identify Improvement Areas

Look for:
- **Low task adherence scores** — The agent didn't address the question properly
- **Low coherence scores** — The response was contradictory or poorly structured
- **Patterns** — Does the agent struggle with certain machine types? Critical vs. normal?

Common findings:
- Agent might be verbose when a concise classification was expected
- Agent might not match the exact format of the expected output (that's OK if the content is right)
- Critical scenarios might get lower groundedness if the agent speculates about causes

### Step 8: Compare Agents (Bonus)

1. Run the same evaluation against your `fault-diagnosis-agent`
2. Compare: Which agent is better at following instructions? Which is more coherent?
3. This comparison helps you decide which system prompt is more effective

## ✅ Done!

You've completed all 5 challenges! 🎉

Go back to the [main README](../../README.md) for wrap-up resources.
