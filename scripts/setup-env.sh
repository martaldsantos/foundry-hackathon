#!/bin/bash
# =============================================================================
# Foundry Hackathon — Setup Environment Variables
# Queries deployed Azure resources and populates the .env file
# Usage: bash scripts/setup-env.sh -g <resource-group>
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$REPO_ROOT/infra/.env"
ENV_TEMPLATE="$REPO_ROOT/infra/.env.template"

usage() {
    echo "Usage: $0 -g <resource-group> [-l <location>]"
    echo ""
    echo "Required parameters:"
    echo "  -g, --resource-group  Name of the resource group containing deployed resources"
    echo ""
    echo "Optional parameters:"
    echo "  -l, --location        Azure region (default: swedencentral)"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 -g foundry-hackathon-rg"
    exit 1
}

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Parse command line arguments
RESOURCE_GROUP=""
LOCATION="swedencentral"

while [[ $# -gt 0 ]]; do
    case $1 in
        -g|--resource-group)
            RESOURCE_GROUP="$2"
            shift 2
            ;;
        -l|--location)
            LOCATION="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate required parameters
if [ -z "$RESOURCE_GROUP" ]; then
    log_error "Missing required parameter: --resource-group"
    usage
fi

# Check if logged into Azure
log_info "Checking Azure CLI login status..."
if ! az account show &>/dev/null; then
    log_error "Not logged into Azure CLI. Please run 'az login' first."
    exit 1
fi

SUBSCRIPTION_ID=$(az account show --query id -o tsv)
SUBSCRIPTION_NAME=$(az account show --query name -o tsv)
log_success "Using subscription: $SUBSCRIPTION_NAME ($SUBSCRIPTION_ID)"

# Verify resource group exists
log_info "Checking resource group: $RESOURCE_GROUP"
if ! az group show --name "$RESOURCE_GROUP" &>/dev/null; then
    log_error "Resource group '$RESOURCE_GROUP' not found."
    echo "Run 'bash infra/deploy.sh' first to create resources."
    exit 1
fi
log_success "Resource group found"

# =============================================================================
# Query Azure resources
# =============================================================================

echo ""
log_info "Querying deployed resources..."

# --- AI Foundry / AI Services ---
log_info "Looking for AI Foundry resource..."
FOUNDRY_RESOURCE_NAME=$(az cognitiveservices account list \
    --resource-group "$RESOURCE_GROUP" \
    --query "[?kind=='AIServices' || kind=='OpenAI'].name | [0]" \
    -o tsv 2>/dev/null)

if [ -z "$FOUNDRY_RESOURCE_NAME" ] || [ "$FOUNDRY_RESOURCE_NAME" == "None" ]; then
    log_warning "No AI Foundry/AI Services resource found. Trying alternative query..."
    FOUNDRY_RESOURCE_NAME=$(az resource list \
        --resource-group "$RESOURCE_GROUP" \
        --resource-type "Microsoft.CognitiveServices/accounts" \
        --query "[0].name" -o tsv 2>/dev/null)
fi

if [ -n "$FOUNDRY_RESOURCE_NAME" ] && [ "$FOUNDRY_RESOURCE_NAME" != "None" ]; then
    log_success "Found AI resource: $FOUNDRY_RESOURCE_NAME"
    
    FOUNDRY_ENDPOINT=$(az cognitiveservices account show \
        --name "$FOUNDRY_RESOURCE_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --query "properties.endpoint" -o tsv 2>/dev/null)
    log_success "Endpoint: $FOUNDRY_ENDPOINT"
else
    log_warning "No AI Services resource found — you'll need to fill FOUNDRY_RESOURCE_NAME manually"
    FOUNDRY_RESOURCE_NAME=""
    FOUNDRY_ENDPOINT=""
fi

# --- AI Foundry Project ---
log_info "Looking for AI Foundry project..."
PROJECT_NAME=$(az resource list \
    --resource-group "$RESOURCE_GROUP" \
    --resource-type "Microsoft.MachineLearningServices/workspaces" \
    --query "[0].name" -o tsv 2>/dev/null)

PROJECT_CONNECTION_STRING=""
if [ -n "$PROJECT_NAME" ] && [ "$PROJECT_NAME" != "None" ]; then
    log_success "Found project: $PROJECT_NAME"
    
    # Build connection string: <endpoint>/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.MachineLearningServices/workspaces/<project>
    PROJECT_RESOURCE_ID="/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.MachineLearningServices/workspaces/$PROJECT_NAME"
    
    # Get the discovery URL for the workspace
    DISCOVERY_URL=$(az resource show \
        --ids "$PROJECT_RESOURCE_ID" \
        --query "properties.discoveryUrl" -o tsv 2>/dev/null)
    
    if [ -n "$DISCOVERY_URL" ] && [ "$DISCOVERY_URL" != "None" ]; then
        # Extract the base endpoint from discovery URL
        PROJECT_ENDPOINT=$(echo "$DISCOVERY_URL" | sed 's|/discovery||')
        PROJECT_CONNECTION_STRING="$PROJECT_ENDPOINT;$SUBSCRIPTION_ID;$RESOURCE_GROUP;$PROJECT_NAME"
    fi
    
    log_success "Project connection string built"
else
    log_warning "No AI Foundry project found — you'll need to fill PROJECT_NAME manually"
    PROJECT_NAME="tire-factory-project"
fi

# --- Application Insights ---
log_info "Looking for Application Insights..."
APPINSIGHTS_NAME=$(az resource list \
    --resource-group "$RESOURCE_GROUP" \
    --resource-type "Microsoft.Insights/components" \
    --query "[0].name" -o tsv 2>/dev/null)

APPLICATIONINSIGHTS_CONNECTION_STRING=""
APPINSIGHTS_INSTRUMENTATION_KEY=""

if [ -n "$APPINSIGHTS_NAME" ] && [ "$APPINSIGHTS_NAME" != "None" ]; then
    log_success "Found App Insights: $APPINSIGHTS_NAME"
    
    APPLICATIONINSIGHTS_CONNECTION_STRING=$(az monitor app-insights component show \
        --app "$APPINSIGHTS_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --query "connectionString" -o tsv 2>/dev/null)
    
    APPINSIGHTS_INSTRUMENTATION_KEY=$(az monitor app-insights component show \
        --app "$APPINSIGHTS_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --query "instrumentationKey" -o tsv 2>/dev/null)
    
    log_success "App Insights connection string retrieved"
else
    log_warning "No Application Insights found — you'll need to fill this manually"
fi

# --- API Management ---
log_info "Looking for API Management..."
APIM_NAME=$(az resource list \
    --resource-group "$RESOURCE_GROUP" \
    --resource-type "Microsoft.ApiManagement/service" \
    --query "[0].name" -o tsv 2>/dev/null)

APIM_GATEWAY_URL=""
APIM_SUBSCRIPTION_KEY=""

if [ -n "$APIM_NAME" ] && [ "$APIM_NAME" != "None" ]; then
    log_success "Found APIM: $APIM_NAME"
    
    APIM_GATEWAY_URL=$(az apim show \
        --name "$APIM_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --query "gatewayUrl" -o tsv 2>/dev/null)
    
    # Get built-in subscription key
    APIM_SUBSCRIPTION_KEY=$(az apim subscription list \
        --resource-group "$RESOURCE_GROUP" \
        --service-name "$APIM_NAME" \
        --query "[?displayName=='Built-in all-access subscription'].primaryKey | [0]" \
        -o tsv 2>/dev/null)
    
    log_success "APIM gateway URL: $APIM_GATEWAY_URL"
else
    log_warning "No API Management found — you'll need to fill this manually"
fi

# =============================================================================
# Write .env file
# =============================================================================

echo ""
log_info "Writing .env file to: $ENV_FILE"

cat > "$ENV_FILE" << EOF
# =============================================================================
# Foundry Hackathon — Environment Variables
# Auto-generated by setup-env.sh on $(date)
# =============================================================================

# Azure Subscription
AZURE_SUBSCRIPTION_ID=$SUBSCRIPTION_ID
RESOURCE_GROUP=$RESOURCE_GROUP

# AI Foundry
FOUNDRY_RESOURCE_NAME=$FOUNDRY_RESOURCE_NAME
PROJECT_NAME=$PROJECT_NAME
FOUNDRY_ENDPOINT=$FOUNDRY_ENDPOINT
PROJECT_CONNECTION_STRING=$PROJECT_CONNECTION_STRING
MODEL_DEPLOYMENT_NAME=gpt-5.1

# Application Insights & Monitoring
APPLICATIONINSIGHTS_CONNECTION_STRING=$APPLICATIONINSIGHTS_CONNECTION_STRING
APPINSIGHTS_INSTRUMENTATION_KEY=$APPINSIGHTS_INSTRUMENTATION_KEY

# API Management
APIM_GATEWAY_URL=$APIM_GATEWAY_URL
APIM_NAME=$APIM_NAME
APIM_SUBSCRIPTION_KEY=$APIM_SUBSCRIPTION_KEY

# Tracing (set to true to enable GenAI tracing)
AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING=true
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
EOF

echo ""
echo "=========================================="
log_success ".env file created successfully!"
echo "=========================================="
echo ""
echo "File location: $ENV_FILE"
echo ""

# Check for empty values
EMPTY_VARS=()
while IFS='=' read -r key value; do
    # Skip comments and empty lines
    [[ "$key" =~ ^#.*$ ]] && continue
    [[ -z "$key" ]] && continue
    if [ -z "$value" ]; then
        EMPTY_VARS+=("$key")
    fi
done < "$ENV_FILE"

if [ ${#EMPTY_VARS[@]} -gt 0 ]; then
    log_warning "The following variables are empty (fill manually or deploy missing resources):"
    for var in "${EMPTY_VARS[@]}"; do
        echo "  - $var"
    done
    echo ""
fi

log_success "Setup complete! Run 'source $ENV_FILE' or use python-dotenv to load variables."
