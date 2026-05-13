#!/bin/bash
set -euo pipefail

# =============================================================================
# Foundry Hackathon — Infrastructure Deployment Script
# Provisions: AI Foundry (hub + project + model), Log Analytics, App Insights, APIM
# Region: swedencentral
# =============================================================================

# --- Configuration -----------------------------------------------------------
RESOURCE_GROUP="${RESOURCE_GROUP:-foundry-hackathon-rg}"
LOCATION="${LOCATION:-swedencentral}"
FOUNDRY_RESOURCE_NAME="${FOUNDRY_RESOURCE_NAME:-foundry-hack-$(openssl rand -hex 4)}"
PROJECT_NAME="${PROJECT_NAME:-tire-factory-project}"
MODEL_DEPLOYMENT_NAME="${MODEL_DEPLOYMENT_NAME:-gpt-5.1}"
LOG_ANALYTICS_NAME="${LOG_ANALYTICS_NAME:-foundry-hack-logs}"
APP_INSIGHTS_NAME="${APP_INSIGHTS_NAME:-foundry-hack-insights}"
APIM_NAME="${APIM_NAME:-foundry-hack-apim-$(openssl rand -hex 4)}"
APIM_PUBLISHER_EMAIL="${APIM_PUBLISHER_EMAIL:-hackathon@contoso.com}"
APIM_PUBLISHER_NAME="${APIM_PUBLISHER_NAME:-Hackathon Team}"

echo "=============================================="
echo "  Foundry Hackathon — Infrastructure Deploy"
echo "=============================================="
echo ""
echo "Resource Group:    $RESOURCE_GROUP"
echo "Location:          $LOCATION"
echo "Foundry Resource:  $FOUNDRY_RESOURCE_NAME"
echo "Project:           $PROJECT_NAME"
echo "Model Deployment:  $MODEL_DEPLOYMENT_NAME"
echo "APIM:              $APIM_NAME"
echo ""

# --- Resource Group ----------------------------------------------------------
echo ">>> Creating resource group..."
az group create \
    --name "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --output none

# --- APIM (start early — takes ~30 min) -------------------------------------
echo ">>> Creating API Management instance (Developer SKU, ~30 min provision time)..."
echo "    This runs in the background. Check status with:"
echo "    az apim show --name $APIM_NAME --resource-group $RESOURCE_GROUP --query provisioningState"
az apim create \
    --name "$APIM_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --publisher-name "$APIM_PUBLISHER_NAME" \
    --publisher-email "$APIM_PUBLISHER_EMAIL" \
    --sku-name Developer \
    --no-wait \
    --output none

# --- AI Foundry Hub ----------------------------------------------------------
echo ">>> Creating AI Foundry resource (AIServices)..."
az cognitiveservices account create \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --kind AIServices \
    --sku S0 \
    --location "$LOCATION" \
    --custom-domain "$FOUNDRY_RESOURCE_NAME" \
    --output none

echo ">>> Creating AI Foundry project..."
az cognitiveservices account project create \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --project-name "$PROJECT_NAME" \
    --location "$LOCATION" \
    --output none

# --- Model Deployment --------------------------------------------------------
echo ">>> Deploying gpt-5.1 model..."
az cognitiveservices account deployment create \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --deployment-name "$MODEL_DEPLOYMENT_NAME" \
    --model-name "gpt-5.1" \
    --model-version "2026-02-04" \
    --model-format OpenAI \
    --sku-capacity 10 \
    --sku-name GlobalStandard \
    --output none

# --- Log Analytics Workspace -------------------------------------------------
echo ">>> Creating Log Analytics workspace..."
az monitor log-analytics workspace create \
    --resource-group "$RESOURCE_GROUP" \
    --workspace-name "$LOG_ANALYTICS_NAME" \
    --location "$LOCATION" \
    --output none

LOG_ANALYTICS_ID=$(az monitor log-analytics workspace show \
    --resource-group "$RESOURCE_GROUP" \
    --workspace-name "$LOG_ANALYTICS_NAME" \
    --query id -o tsv)

# --- Application Insights ----------------------------------------------------
echo ">>> Creating Application Insights (linked to Log Analytics)..."
az monitor app-insights component create \
    --app "$APP_INSIGHTS_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --location "$LOCATION" \
    --workspace "$LOG_ANALYTICS_ID" \
    --output none

APP_INSIGHTS_CONN_STRING=$(az monitor app-insights component show \
    --app "$APP_INSIGHTS_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query connectionString -o tsv)

APP_INSIGHTS_INSTRUMENTATION_KEY=$(az monitor app-insights component show \
    --app "$APP_INSIGHTS_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query instrumentationKey -o tsv)

# --- Retrieve Connection Info ------------------------------------------------
echo ">>> Retrieving Foundry endpoint and keys..."
FOUNDRY_ENDPOINT=$(az cognitiveservices account show \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "properties.endpoint" -o tsv)

PROJECT_CONNECTION_STRING=$(az cognitiveservices account project show \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --project-name "$PROJECT_NAME" \
    --query "properties.endpoint" -o tsv)

SUBSCRIPTION_ID=$(az account show --query id -o tsv)

# --- APIM Gateway URL --------------------------------------------------------
APIM_GATEWAY_URL="https://${APIM_NAME}.azure-api.net"

# --- Output ------------------------------------------------------------------
echo ""
echo "=============================================="
echo "  DEPLOYMENT COMPLETE"
echo "=============================================="
echo ""
echo "Copy these values into your .env file:"
echo ""
echo "AZURE_SUBSCRIPTION_ID=$SUBSCRIPTION_ID"
echo "RESOURCE_GROUP=$RESOURCE_GROUP"
echo "FOUNDRY_RESOURCE_NAME=$FOUNDRY_RESOURCE_NAME"
echo "PROJECT_NAME=$PROJECT_NAME"
echo "FOUNDRY_ENDPOINT=$FOUNDRY_ENDPOINT"
echo "PROJECT_CONNECTION_STRING=$PROJECT_CONNECTION_STRING"
echo "MODEL_DEPLOYMENT_NAME=$MODEL_DEPLOYMENT_NAME"
echo "APPLICATIONINSIGHTS_CONNECTION_STRING=$APP_INSIGHTS_CONN_STRING"
echo "APPINSIGHTS_INSTRUMENTATION_KEY=$APP_INSIGHTS_INSTRUMENTATION_KEY"
echo "APIM_GATEWAY_URL=$APIM_GATEWAY_URL"
echo "APIM_NAME=$APIM_NAME"
echo ""
echo "⚠️  APIM is still provisioning (~30 min). Check status:"
echo "    az apim show --name $APIM_NAME --resource-group $RESOURCE_GROUP --query provisioningState"
echo ""
echo "Once APIM is ready, get your subscription key:"
echo "    az apim subscription list --resource-group $RESOURCE_GROUP --service-name $APIM_NAME --query \"[0].primaryKey\" -o tsv"
echo ""
