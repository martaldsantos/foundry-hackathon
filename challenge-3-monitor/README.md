# Challenge 3: Monitor with Application Insights

## Objectives

By the end of this challenge, you will have:
- ✅ GenAI tracing enabled for your Foundry agents
- ✅ Agent interactions visible as traces in Application Insights
- ✅ Written a KQL query to analyze agent latency and token usage
- ✅ Understanding of how to debug agent behavior in production

## Time: ~50 minutes

## Context

Your agents are deployed and exposed via APIM. But how do you know they're working well? What if an agent gives a bad answer? What if latency spikes?

**Application Insights** with **GenAI tracing** gives you:
- Full trace of every agent interaction (user message → model call → tool calls → response)
- Token usage per request
- Latency breakdown (network, model inference, tool execution)
- Error tracking and alerting

## Choose Your Track

| Track | Go to |
|-------|-------|
| Portal Track | [portal-track/README.md](./portal-track/README.md) |
| SDK Track | [sdk-track/README.md](./sdk-track/README.md) |

## Success Criteria

- [ ] You can see at least one agent trace in Application Insights
- [ ] The trace shows the full conversation flow (user → agent → tool → response)
- [ ] You've written a KQL query that shows average latency per agent
- [ ] You understand where to look when an agent misbehaves
