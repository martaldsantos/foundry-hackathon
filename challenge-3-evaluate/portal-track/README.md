# Challenge 3: Monitor — Portal Track

## Step-by-Step Instructions

### Step 1: Connect Application Insights to Foundry

1. Open [https://ai.azure.com](https://ai.azure.com) (ensure **New Foundry** toggle is **On**)
2. Select your **tire-factory-project**
3. In the left sidebar, click **Management center** (at the bottom)
4. Under your Foundry resource, look at **Connected resources**
5. Look for your Application Insights resource
   - If it's already connected, you'll see it listed with a status indicator
   - If not, click **+ New connection** → Select **Application Insights** → Choose your `foundry-hack-insights` resource → Click **Connect**

### Step 2: Enable Tracing in Foundry

1. Navigate back to your project
2. In the left sidebar, click **Tracing** (under the "Operate" section)
3. If prompted to select an Application Insights resource, choose `foundry-hack-insights`
4. You should see the tracing dashboard (may be empty initially)

### Step 3: Generate Some Traces

1. In the left sidebar, click **Agents** (under "Build")
2. Select your `anomaly-detection-agent`
3. Click **Test** to open the Agent playground
4. Send 3-4 messages to generate trace data:

   ```
   Check the mixer (MX-001) for anomalies
   ```
   ```
   What's the status of the curing press?
   ```
   ```
   Are any machines in critical condition?
   ```
   ```
   Check all 5 machines and summarize
   ```

5. Wait 1-2 minutes for traces to appear in Application Insights

### Step 4: Explore Traces in Foundry

1. In the left sidebar, click **Tracing** (under "Operate")
2. You should now see trace entries appearing
3. Click on any trace to see the full span:
   - **Root span**: The overall agent interaction
   - **Child spans**: Individual steps (model calls, tool calls)
   - **Attributes**: Token counts, latency, model name

### Step 5: Open Application Insights Directly

1. Go to the [Azure Portal](https://portal.azure.com)
2. Navigate to your **Application Insights** resource (`foundry-hack-insights`)
3. Click **Transaction search** in the left sidebar
4. Filter by:
   - Time range: Last 30 minutes
   - Event types: Dependency
5. You should see entries for your model calls

### Step 6: Write a KQL Query

1. In Application Insights, click **Logs** in the left sidebar
2. This opens the Log Analytics query editor
3. Try this query to see agent call latency:

   ```kql
   dependencies
   | where timestamp > ago(1h)
   | where type == "Azure.AI"
   | summarize 
       avg_duration_ms = avg(duration),
       p95_duration_ms = percentile(duration, 95),
       total_calls = count()
     by target
   | order by avg_duration_ms desc
   ```

4. Click **Run** to see results

### Step 7: Explore GenAI-Specific Traces

Try this KQL query to see token usage:

```kql
traces
| where timestamp > ago(1h)
| where message contains "gen_ai"
| extend prompt_tokens = toint(customDimensions["gen_ai.usage.prompt_tokens"])
| extend completion_tokens = toint(customDimensions["gen_ai.usage.completion_tokens"])
| where isnotnull(prompt_tokens)
| summarize 
    total_prompt_tokens = sum(prompt_tokens),
    total_completion_tokens = sum(completion_tokens),
    avg_prompt_tokens = avg(prompt_tokens),
    request_count = count()
| project 
    request_count,
    total_prompt_tokens,
    total_completion_tokens,
    total_tokens = total_prompt_tokens + total_completion_tokens,
    avg_prompt_tokens
```

### Step 8: Set Up a Basic Alert (Bonus)

1. In Application Insights, click **Alerts** in the left sidebar
2. Click **+ Create** → **Alert rule**
3. Condition: Custom log search
4. Query:
   ```kql
   dependencies
   | where type == "Azure.AI"
   | where duration > 10000
   ```
5. Threshold: Greater than 0
6. This will alert you if any agent call takes longer than 10 seconds

## ✅ Done!

You can now observe your agents in production. Move on to [Challenge 4: Workflow](../../challenge-4-deploy/).
