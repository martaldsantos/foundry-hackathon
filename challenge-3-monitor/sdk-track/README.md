# Challenge 3: Monitor — SDK Track

## Step-by-Step Instructions

### Overview

You'll enable GenAI tracing in your Python code so that every agent interaction is captured as a distributed trace in Application Insights. Then you'll query those traces programmatically.

### Step 1: Understand the Tracing Architecture

```
Your Python Code
    │
    ├── AIProjectInstrumentor (auto-instruments SDK calls)
    │       │
    │       ▼
    ├── OpenTelemetry SDK (collects spans)
    │       │
    │       ▼
    └── Azure Monitor Exporter (sends to App Insights)
            │
            ▼
    Application Insights (stores & queries traces)
```

### Step 2: Configure Environment Variables

Make sure these are in your `.env`:
```
AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;...
```

The first enables GenAI tracing, the second captures full message content in traces (useful for debugging, disable in production with PII concerns).

### Step 3: Fill in the TODOs

Open `tracing.py` and complete:

1. **Instrumentor setup** — Initialize `AIProjectInstrumentor` and configure the Azure Monitor exporter
2. **Agent call with tracing** — Run an agent interaction that gets captured as a trace
3. **Query traces** — Verify traces appeared in Application Insights

### Step 4: Run

```bash
cd challenge-3-monitor/sdk-track
python tracing.py
```

### Expected Output

```
=== Setting up tracing ===
✅ AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING is enabled
✅ AIProjectInstrumentor configured
✅ Azure Monitor exporter connected

=== Running traced agent call ===
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

Move on to [Challenge 4: Evaluate](../../challenge-4-evaluate/).
