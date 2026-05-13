# Challenge 2: Monitor — SDK Track

## Step-by-Step Instructions

### Overview

You'll enable GenAI tracing in your Python code so that every agent interaction is captured as a distributed trace in Application Insights.

### Step 1: Tracing Architecture

```
Your Python Code
    │
    ├── AIProjectInstrumentor  (auto-instruments all SDK calls)
    │       │
    │       ▼
    ├── OpenTelemetry SDK  (collects spans)
    │       │
    │       ▼
    └── Azure Monitor Exporter  (sends to App Insights)
            │
            ▼
    Application Insights  (stores & visualises traces)
```

### Step 2: Configure Environment Variables

Make sure these are in your `.env`:
```
AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;...
```

> ⚠️ These env vars must be set **before** any `azure.ai.projects` import runs. The script loads `.env` at the top for this reason.

### Step 3: Fill in the TODOs

Open `monitor.py` and complete:

1. **`setup_tracing()`** — Initialize `AIProjectInstrumentor` and configure the Azure Monitor exporter
2. **`run_traced_agent_call()`** — Run an agent interaction that gets automatically captured as a trace

### Step 4: Run

```bash
cd challenge-2-monitor/sdk-track
python monitor.py
```

### Expected Output

```
=== Setting up tracing ===
✅ AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING is enabled
✅ AIProjectInstrumentor configured
✅ Azure Monitor exporter connected

=== Running traced agent call ===
✅ Agent responded: ...

=== Verifying traces in App Insights ===
⏳ Waiting for traces to propagate (30 seconds)...
✅ Traces should now be visible in Application Insights

🎉 Monitoring is active!
```

### Step 5: View traces in the Portal

1. Go to **Azure Portal → Application Insights → Transaction search**
2. Filter: **Last 5 minutes**, Event type: **Dependency**
3. Look for entries named after the agent or model deployment

## ✅ Done!

Move on to [Challenge 3: Evaluate](../../challenge-3-evaluate/).
