# Challenge 3: Evaluate — SDK Track

## Step-by-Step Instructions

### Overview

You'll run a systematic evaluation of your anomaly detection agent against the 10-row test dataset, using LLM-as-judge evaluators to measure quality.

### Step 1: Understand the Evaluation Flow

```
evaluation_dataset.json  (10 test cases)
         │
         ▼
  Your Agent  (processes each input)
         │
         ▼
  Evaluators  (LLM-as-judge: score 1-5)
         │
         ▼
  Metrics  (passed / failed / per-row scores)
```

### Step 2: Fill in the TODOs

Open `evaluate.py` and complete:

1. **`run_agent_on_dataset()`** — For each test case, create a conversation, send the input, collect the response text
2. **`run_evaluators()`** — Create an evaluation with `task_adherence` and `coherence` criteria, run it against collected results, and poll until complete

### Step 3: Run

```bash
cd challenge-3-evaluate/sdk-track
python evaluate.py
```

### Expected Output

```
=== Running Evaluation ===
Loaded 10 test cases from evaluation_dataset.json
Processing 10 test cases...
  [1/10] eval-001: normal classification
  [2/10] eval-002: warning classification
  ...
  [10/10] eval-010: normal classification

=== Running Evaluators ===
Evaluation run started: evalrun-xxx
  Status: in_progress...
  Status: in_progress...

Evaluation complete — status: completed
  Passed: 9  Failed: 1  Errors: 0

🎉 Evaluation complete!
```
✅ Agent responded (captured as trace)

=== Verifying traces in App Insights ===
⏳ Waiting for traces to propagate (30 seconds)...
✅ Found 1 trace(s) in Application Insights
   - Duration: 2340ms
   - Tokens: 156 prompt + 89 completion

🎉 Monitoring is active! Check App Insights for the full trace view.
```

### Tips

- Traces take 30-60 seconds to appear in App Insights
- Set `AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true` **before** importing the SDK client
- The `AIProjectInstrumentor` must be called before creating any `AIProjectClient` instance
- Content capture (`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT`) is great for debugging but should be off in production for privacy

## ✅ Done!

Move on to [Challenge 4: Workflow](../../challenge-4-deploy/).
