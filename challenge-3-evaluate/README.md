# Challenge 3: Evaluate

## Objectives

By the end of this challenge, you will have:
- ✅ Run a systematic evaluation of your agents against a test dataset
- ✅ Used built-in evaluators (task adherence, coherence) to measure quality
- ✅ Interpreted evaluation metrics and identified areas for improvement
- ✅ Understanding of how to integrate evaluations into a CI/CD pipeline

## Time: ~30 minutes

## Context

Monitoring tells you **what's happening** (latency, errors, token usage). Evaluation tells you **if the answers are actually good**.

You have a dataset of 10 test cases — each with a sensor reading snapshot and the expected correct output (classification + recommended action). You'll run your agents against these test cases and measure how well they perform using LLM-as-judge scoring.

## The Evaluation Dataset

The dataset lives at [challenge-4-deploy/evaluation_dataset.json](../challenge-4-deploy/evaluation_dataset.json) — it contains:
- 10 scenarios covering normal, warning, and critical machines
- Each has an `input` (what you send to the agent)
- Each has an `expected_output` (the correct classification and action)

## Get Started

Open [evaluate.py](./evaluate.py) and fill in the TODOs to run evaluations.

```bash
cd challenge-3-evaluate
python evaluate.py
```

See [solutions/evaluate.py](./solutions/evaluate.py) if you get stuck.

## Success Criteria

- [ ] Evaluation runs against all 10 test cases without errors
- [ ] You can see per-row scores for task adherence and coherence
- [ ] You've identified at least one case where the agent could improve
- [ ] You understand the difference between aggregate metrics and per-row analysis
