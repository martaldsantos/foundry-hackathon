# Challenge 2: Monitor — Portal Track

## Step-by-Step Instructions

### Step 1: Open Application Insights

1. Open the [Azure Portal](https://portal.azure.com)
2. Navigate to your resource group: **foundry-hackathon-rg**
3. Click on your **Application Insights** resource (named `foundry-hack-insights`)
4. You'll land on the **Overview** page

### Step 2: Enable GenAI Tracing in Your Code

Before traces appear in App Insights, the SDK track needs to run with tracing enabled.

Make sure your `.env` contains:
```
AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;...
```

Then run the SDK track file to generate traces:

```bash
cd challenge-2-monitor/sdk-track
python monitor.py
```

### Step 3: View Traces in the Portal

After running `monitor.py`:

1. In Application Insights, click **Transaction search** (left sidebar)
2. Set the time range to **Last 30 minutes**
3. Click **Search**
4. Look for entries of type **Dependency** — these are the LLM calls

Click on any entry to see the full trace:
- **Duration** — how long the model took to respond
- **Tokens** — prompt and completion token counts
- **Custom properties** — agent name, conversation ID

### Step 4: Explore Live Metrics

1. In Application Insights, click **Live metrics** (left sidebar)
2. Keep the window open and run `monitor.py` again in a separate terminal
3. Watch requests appear in real time under **Incoming Requests**

### Step 5: Check the Failures Blade

1. Click **Failures** (left sidebar)
2. If the agent call succeeded you'll see 0 failures — this is expected
3. Note the structure: you can drill down by operation name, exception type, or time

## ✅ Done!

Move on to [Challenge 3: Evaluate](../../challenge-3-evaluate/).

