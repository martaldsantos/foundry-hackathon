# Challenge 1: Build Agents

## Objectives

By the end of this challenge, you will have:
- ✅ A **Claims Triage Agent** that assesses incoming claims and flags risks
- ✅ A **Claims Decision Agent** that analyzes flagged claims and recommends actions
- ✅ Both agents tested against real claims data

Time: ~35 minutes

## Context

ClaimSight Insurance processes hundreds of claims daily. Each claim has associated metrics: document completeness, damage-vs-estimate consistency, fraud risk score, and policy coverage match. Your agents need to:

1. **Claims Triage**: Compare claim metrics against acceptable thresholds and flag claims that need attention
2. **Claims Decision**: Given a flagged claim, determine the recommended action (approve, investigate, request documents, or deny)

Check out [claims_data.json](./claims_data.json) to see the current batch of claims.

## Get Started

Open [agents.py](./agents.py) and review the implementation of both agents.

```bash
cd claims/challenge-1-build
python agents.py
```

## Success Criteria

- [ ] Claims Triage Agent correctly identifies the 2 warning + 1 critical claim
- [ ] Claims Decision Agent provides reasonable action recommendations
- [ ] Both agents respond coherently when given a claim's metrics
