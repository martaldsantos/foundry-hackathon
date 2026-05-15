#!/bin/bash
set -euo pipefail

# =============================================================================
# Foundry Hackathon — Infrastructure Deployment Script
# Provisions: AI Foundry (hub + project + model), Log Analytics, App Insights
# Region: swedencentral
# =============================================================================

# --- Configuration -----------------------------------------------------------
RESOURCE_GROUP="${RESOURCE_GROUP:-foundry-hackathon-rg}"
LOCATION="${LOCATION:-swedencentral}"
FOUNDRY_RESOURCE_NAME="${FOUNDRY_RESOURCE_NAME:-foundry-hack-$(openssl rand -hex 4)}"
PROJECT_NAME="${PROJECT_NAME:-tire-factory-project}"
MODEL_DEPLOYMENT_NAME="${MODEL_DEPLOYMENT_NAME:-gpt-5.4}"
MODEL_NAME="${MODEL_NAME:-gpt-5.4}"
MODEL_VERSION="${MODEL_VERSION:-2026-03-05}"
LOG_ANALYTICS_NAME="${LOG_ANALYTICS_NAME:-foundry-hack-logs}"
APP_INSIGHTS_NAME="${APP_INSIGHTS_NAME:-foundry-hack-insights}"

echo "=============================================="
echo "  Foundry Hackathon — Infrastructure Deploy"
echo "=============================================="
echo ""
echo "Resource Group:    $RESOURCE_GROUP"
echo "Location:          $LOCATION"
echo "Foundry Resource:  $FOUNDRY_RESOURCE_NAME"
echo "Project:           $PROJECT_NAME"
echo "Model Deployment:  $MODEL_DEPLOYMENT_NAME"
echo "Model Name:        $MODEL_NAME"
echo "Model Version:     $MODEL_VERSION"
echo ""

# --- Resource Group ----------------------------------------------------------
echo ">>> Creating resource group..."
az group create \
    --name "$RESOURCE_GROUP" \
    --location "$LOCATION" \
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
    --disable-local-auth false \
    --output none

# Some tenants enforce this with Azure Policy. Try to force-enable key auth and verify.
FOUNDRY_RESOURCE_ID=$(az cognitiveservices account show \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query id -o tsv)

az resource update \
    --ids "$FOUNDRY_RESOURCE_ID" \
    --set properties.disableLocalAuth=false \
    --output none || true

DISABLE_LOCAL_AUTH=$(az cognitiveservices account show \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query properties.disableLocalAuth -o tsv)

if [ "$DISABLE_LOCAL_AUTH" = "true" ]; then
    echo "❌ API key authentication is still disabled on the Foundry resource."
    echo "   This is usually enforced by Azure Policy in your tenant/subscription."
    echo "   Ask an Azure admin to allow local auth or use Entra ID-only evaluation flow."
    exit 1
fi

echo ">>> Creating AI Foundry project..."
az cognitiveservices account project create \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --project-name "$PROJECT_NAME" \
    --location "$LOCATION" \
    --output none

# --- Model Deployment --------------------------------------------------------
echo ">>> Deploying model: $MODEL_NAME ($MODEL_VERSION)..."
az cognitiveservices account deployment create \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --deployment-name "$MODEL_DEPLOYMENT_NAME" \
    --model-name "$MODEL_NAME" \
    --model-version "$MODEL_VERSION" \
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
    --query "properties.endpoints.\"AI Foundry API\"" -o tsv)

SUBSCRIPTION_ID=$(az account show --query id -o tsv)

# --- Write .env file ----------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"

echo ">>> Writing .env file to: $ENV_FILE"

cat > "$ENV_FILE" << EOF
# =============================================================================
# Foundry Hackathon — Environment Variables
# Auto-generated by deploy.sh on $(date)
# =============================================================================

# Azure Subscription
AZURE_SUBSCRIPTION_ID=$SUBSCRIPTION_ID
RESOURCE_GROUP=$RESOURCE_GROUP

# AI Foundry
FOUNDRY_RESOURCE_NAME=$FOUNDRY_RESOURCE_NAME
PROJECT_NAME=$PROJECT_NAME
FOUNDRY_ENDPOINT=$FOUNDRY_ENDPOINT
PROJECT_CONNECTION_STRING=$PROJECT_CONNECTION_STRING
MODEL_DEPLOYMENT_NAME=$MODEL_DEPLOYMENT_NAME

# Application Insights & Monitoring
APPLICATIONINSIGHTS_CONNECTION_STRING=$APP_INSIGHTS_CONN_STRING
APPINSIGHTS_INSTRUMENTATION_KEY=$APP_INSIGHTS_INSTRUMENTATION_KEY

# Tracing (set to true to enable GenAI tracing)
AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
EOF

echo ""
echo "=============================================="
echo "  ✅ DEPLOYMENT COMPLETE"
echo "=============================================="
echo ""
echo "  .env file written to: $ENV_FILE"
echo ""
