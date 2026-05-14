# Challenge 1: Build Agents

## Objectives

By the end of this challenge, you will have:
- ✅ An **Intent Classification Agent** that analyzes call summaries and categorizes customer intent
- ✅ A **Resolution Advisor Agent** that recommends optimal handling strategies
- ✅ Both agents tested against real call center data

## Time: ~20 minutes

## Context

NovaTel Communications receives hundreds of calls daily. Each call has a summary, customer history, and account context. Your agents need to:

1. **Intent Classification**: Analyze the call to determine what the customer needs (billing dispute, tech issue, cancellation risk, upsell opportunity, etc.)
2. **Resolution Advisory**: Given a classified intent + customer context, recommend the best resolution path with scripts, escalation decisions, and available offers

Check out [call_data.json](./call_data.json) to see today's incoming calls.

## Get Started

Open [agents.py](./agents.py) and review the implementation of both agents.

```bash
cd callcenter/challenge-1-build
python agents.py
```

## Success Criteria

- [ ] Intent Classification Agent correctly identifies all 6 intent types across 7 calls
- [ ] Resolution Advisor provides actionable recommendations with scripts and escalation decisions
- [ ] Security concerns are always escalated; billing disputes offer appropriate credits
