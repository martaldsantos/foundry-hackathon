# Challenge 2: Monitor with Application Insights

## Objectives

By the end of this challenge, you will have:
- ✅ GenAI tracing enabled for your Foundry agents
- ✅ Agent interactions visible as traces in Application Insights
- ✅ Understanding of how to debug agent behaviour in production

Time: ~10 minutes

## Context

Your agents work — but how do you know they're working **well**? What if an agent gives a bad answer? What if latency spikes? What if a tool call fails silently?

**Application Insights** with **GenAI tracing** gives you:
- Full trace of every agent interaction (user message → model call → tool calls → response)
- Token usage per request
- Latency breakdown (network, model inference, tool execution)
- Error tracking and alerting

## Prerequisites

Make sure your `.env` has:
```
AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;...
```

## Get Started

Open [monitor.py](./monitor.py) and review the tracing setup.

```bash
cd factory/challenge-2-monitor
python monitor.py
```

## Success Criteria

- [ ] You can see at least one agent trace in Application Insights
- [ ] The trace shows the full conversation flow (user → agent → tool → response)
- [ ] You understand where to look when an agent misbehaves
