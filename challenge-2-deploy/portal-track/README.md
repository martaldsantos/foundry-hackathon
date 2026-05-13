# Challenge 2: Deploy & Expose — Portal Track

## Step-by-Step Instructions

### Step 1: Verify APIM is Ready

1. Open the [Azure Portal](https://portal.azure.com)
2. Navigate to your resource group: **foundry-hackathon-rg**
3. Click on your **API Management** resource
4. Verify the **Status** shows **Online** (top of the overview page)

> ⏳ If status shows "Activating", APIM is still provisioning. Ask your facilitator for the shared instance.

### Step 2: Import Foundry API into APIM

1. In your APIM resource, click **APIs** in the left sidebar
2. Click **+ Add API**
3. Under "Create from Azure resource", select **Azure AI Service** (or **Microsoft Foundry**)
4. In the dialog:
   - **Azure AI Service**: Select your Foundry resource (e.g., `foundry-hack-xxxx`)
   - **Display name**: `Foundry Tire Factory`
   - **Name**: `foundry-tire-factory`
   - **API URL suffix**: `ai`
   - **Client compatibility**: Select **Azure AI** (Model Inference API)
5. Click **Create**

### Step 3: Configure Managed Identity

APIM needs permission to call your Foundry endpoint:

1. In your APIM resource, go to **Managed identities** (left sidebar, under Security)
2. Under **System assigned**, set Status to **On**
3. Click **Save**
4. Copy the **Object ID**

Now assign the role:

5. Navigate to your **Foundry resource** (AI Services account)
6. Click **Access control (IAM)**
7. Click **+ Add** → **Add role assignment**
8. Role: **Cognitive Services User**
9. Members: Select **Managed identity** → **API Management** → Select your APIM instance
10. Click **Review + assign**

### Step 4: Add Rate Limiting Policy

1. Go back to your APIM resource → **APIs** → **Foundry Tire Factory**
2. Click on **All operations**
3. Click the **</>** icon in the **Inbound processing** section
4. Add this policy inside the `<inbound>` block (after `<base />`):

   ```xml
   <rate-limit calls="10" renewal-period="60" />
   ```

5. Click **Save**

This limits each subscription to 10 calls per minute.

### Step 5: Get Your Subscription Key

1. In APIM, go to **Subscriptions** (left sidebar)
2. Find the **Built-in all-access subscription** (or create a new one)
3. Click the **...** menu → **Show/hide keys**
4. Copy the **Primary key**
5. Add it to your `.env` file as `APIM_SUBSCRIPTION_KEY`

### Step 6: Test the Gateway

1. In APIM, go to **APIs** → **Foundry Tire Factory**
2. Click on a POST operation (e.g., chat completions)
3. Click the **Test** tab
4. The subscription key is auto-filled
5. Set the request body:

   ```json
   {
     "messages": [
       {"role": "user", "content": "What causes high vibration in industrial machinery?"}
     ],
     "model": "gpt-5.1"
   }
   ```

6. Click **Send**
7. Verify you get a 200 response with a valid completion

### Step 7: Test Rate Limiting

1. Click **Send** rapidly 11+ times within a minute
2. After 10 calls, you should get a **429 Too Many Requests** response
3. This confirms your rate limiting policy is working

## ✅ Done!

Your Foundry model is now accessible through a managed API gateway. Move on to [Challenge 3: Monitor](../../challenge-3-monitor/).
