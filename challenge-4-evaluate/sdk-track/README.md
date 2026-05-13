# Challenge 4: Evaluate — SDK Track

## Step-by-Step Instructions

### Overview

You'll run a systematic evaluation of your anomaly detection agent against the 10-row test dataset, using built-in evaluators to measure quality.

### Step 1: Understand the Evaluation Flow

```
evaluation_dataset.json (10 test cases)
         │
         ▼
  Your Agent (processes each input)
         │
         ▼
  Evaluators (score each response)
         │
         ▼
  Metrics (aggregate + per-row scores)
```

### Step 2: Fill in the TODOs

Open `evaluate.py` and complete:

1. **Load the dataset** — Read evaluation_dataset.json
2. **Run agent against each input** — Get the agent's response for each test case
3. **Run evaluators** — Score each response using built-in evaluators
4. **Print results** — Show aggregate metrics and per-row scores

### Step 3: Run

```bash
cd challenge-4-evaluate/sdk-track
python evaluate.py
```

### Expected Output

```
=== Running Evaluation ===
Processing 10 test cases...
  [1/10] eval-001: normal classification ✓
  [2/10] eval-002: warning classification ✓
  [3/10] eval-003: critical classification ✓
  ...
  [10/10] eval-010: normal classification ✓

=== Evaluation Results ===
Aggregate Metrics:
  Task Adherence:  4.2 / 5.0
  Coherence:       4.5 / 5.0

Per-Row Scores:
  eval-001: adherence=5, coherence=5 — Normal correctly identified
  eval-002: adherence=4, coherence=4 — Warning detected, slightly verbose
  eval-003: adherence=5, coherence=5 — Critical correctly identified
  ...

Areas for Improvement:
  - eval-008: adherence=3 — Agent missed one anomaly in multi-failure scenario

🎉 Evaluation complete!
```

### Tips

- The evaluation uses the OpenAI client's eval API via `project_client.get_openai_client()`
- Built-in evaluators include: `builtin.task_adherence`, `builtin.coherence`, `builtin.violence`
- You can also create custom evaluators with your own grading criteria
- Per-row analysis is more useful than aggregate scores for improving prompts

## ✅ Done!

You've completed all 5 challenges! 🎉
