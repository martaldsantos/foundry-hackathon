# Challenge 0: Setup — Portal Track

## Step-by-Step Instructions

### Step 1: Navigate to Microsoft Foundry Portal

1. Open [https://ai.azure.com](https://ai.azure.com) in your browser
2. Sign in with your Azure credentials
3. Ensure the **New Foundry** toggle in the top banner is set to **On** (you should see the new experience, not Foundry classic)
4. You should see the **Microsoft Foundry** home page

### Step 2: Verify Your Project

1. From the home page, click **All projects** in the left navigation
2. Look for the project named **tire-factory-project**
3. Click on it to open the project overview
4. Confirm you see:
   - Project name: `tire-factory-project`
   - Region: `swedencentral`
   - Status: Active
   - Resource type: Foundry project (not hub-based)

### Step 3: Check Model Deployment

1. In the left sidebar, click **Models + endpoints** (under the "Build" section)
2. You should see a deployment named **gpt-5.1**
3. Verify:
   - Status: **Succeeded** (green checkmark)
   - Model: `gpt-5.1`
   - Type: `GlobalStandard`
   - Capacity: `10K TPM`

> 💡 If the deployment shows "Creating" or "Failed", wait a few minutes or check with your facilitator.

### Step 4: Test in the Playground

1. Click on the **gpt-5.1** deployment name
2. Click **Open in playground**
3. You'll land in the **Chat playground** — make sure your deployment is selected in the model dropdown
4. In the message box, type:

   ```
   What are common causes of overheating in industrial curing presses?
   ```

5. Click the **Send** arrow (or press Enter)
6. Verify you get a reasonable response about industrial equipment

### Step 5: Explore Connected Resources

1. Go back to your project by clicking the project name in the breadcrumb
2. In the left sidebar, click **Management center** (at the bottom)
3. Under your Foundry resource, look at **Connected resources**
4. Verify you can see:
   - Your Foundry resource (AI Services)
   - Application Insights connection (may still be connecting)

> 💡 In the new Foundry portal, connected resources are managed at the Foundry resource level, not per-project.

## ✅ Done!

You've confirmed your Foundry project is live and the model responds. Move on to [Challenge 1: Build Agents](../../challenge-1-build/).
