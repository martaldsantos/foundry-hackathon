# Challenge 1: Build Agents

## Objectives

By the end of this challenge, you will have:

- ✅ An **Intent Classification Agent** that analyzes call summaries and categorizes customer intent
- ✅ A **Resolution Advisor Agent** that recommends optimal handling strategies
- ✅ Both agents tested against real call center data

Time: ~35 minutes

## Context

NovaTel Communications receives hundreds of calls daily. Each call has a summary, customer history, and account context. Your agents need to:

1. **Intent Classification**: Analyze the call to determine what the customer needs (billing dispute, tech issue, cancellation risk, upsell opportunity, etc.)
2. **Resolution Advisory**: Given a classified intent + customer context, recommend the best resolution path with scripts, escalation decisions, and available offers

Check out [call_data.json](./call_data.json) to see today's incoming calls.

## Portal or SDK?

Azure AI Foundry gives you two ways to build agents. The **Foundry portal** ([ai.azure.com/nextgen](https://ai.azure.com/nextgen)) provides a visual, no-code interface where you can create agents, attach tools, and test them interactively in a playground — great for exploration and rapid prototyping. The **Azure AI Agents SDK** gives you full programmatic control: you define agent behavior, tools, and orchestration logic in Python, which makes it easy to version, test, and integrate into automated pipelines.

In this challenge we use the **SDK**. The code in [agents.py](./agents.py) creates both agents, registers their tools, and runs them against every call in `call_data.json` — all from the terminal. After the script runs, both agents will also be visible in the portal under **Agents**, so you can inspect them, tweak their instructions, and test them interactively without touching any code.

## Get Started

Open [agents.py](./agents.py) and review the implementation of both agents.

```bash
cd callcenter/challenge-1-build
python agents.py
```

As the script runs, watch the terminal closely — you'll see each agent being created, then each call from `call_data.json` being sent through the **Intent Classification Agent** first, and its output handed off to the **Resolution Advisor Agent**. You'll see the raw agent responses printed for every call, giving you a live view of how the two agents collaborate. Once it completes, head to the [Microsoft Foundry portal](https://ai.azure.com/nextgen), open your project, and navigate to **Agents** in the left sidebar — hit **Refresh** if the agents don't appear immediately, as it can take a few seconds for newly created agents to show up in the portal.

## Success Criteria

- [ ] Intent Classification Agent correctly identifies all 6 intent types across 7 calls
- [ ] Resolution Advisor provides actionable recommendations with scripts and escalation decisions
- [ ] Security concerns are always escalated; billing disputes offer appropriate credits
