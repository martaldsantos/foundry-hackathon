#!/bin/bash
set -euo pipefail

# =============================================================================
# Foundry Hackathon — Infrastructure Deployment Script (Enhanced)
# Provisions: AI Foundry (hub + project + model), Log Analytics, App Insights
# Region: swedencentral
# =============================================================================

# --- Colors & Symbols --------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

CHECK="${GREEN}✔${NC}"
CROSS="${RED}✘${NC}"
WARN="${YELLOW}⚠${NC}"
ARROW="${CYAN}➜${NC}"

# --- Logging -----------------------------------------------------------------
SCRIPT_DIR_EARLY="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR_EARLY}/foundry-deploy-$(date +%Y%m%d-%H%M%S).log"
STEP_COUNT=0
STEP_RESULTS=()

# --- WSL / CRLF fix ---------------------------------------------------------
# Azure CLI on Windows outputs \r\n. $() strips \n but \r stays, silently
# breaking URLs, resource IDs, and string comparisons. This wrapper strips it.
az_q() { az "$@" | tr -d '\r'; }
log()       { echo -e "$1" | tee -a "$LOG_FILE"; }
log_raw()   { echo -e "$1" >> "$LOG_FILE"; }
header()    { log "\n${BOLD}${BLUE}$1${NC}"; }
success()   { log "  ${CHECK}  $1"; }
warn()      { log "  ${WARN}  ${YELLOW}$1${NC}"; }
fail()      { log "  ${CROSS}  ${RED}$1${NC}"; }
info()      { log "  ${ARROW}  $1"; }
divider()   { log "${DIM}$(printf '%.0s─' {1..60})${NC}"; }

# --- Timer helpers -----------------------------------------------------------
DEPLOY_START=$(date +%s)
STEP_START=0

step_start() {
    STEP_COUNT=$((STEP_COUNT + 1))
    STEP_START=$(date +%s)
    header "[Step $STEP_COUNT] $1"
}

step_end_ok() {
    local elapsed=$(( $(date +%s) - STEP_START ))
    success "$1 ${DIM}(${elapsed}s)${NC}"
    STEP_RESULTS+=("${CHECK}|Step $STEP_COUNT|$1|${elapsed}s")
}

step_end_fail() {
    local elapsed=$(( $(date +%s) - STEP_START ))
    fail "$1 ${DIM}(${elapsed}s)${NC}"
    STEP_RESULTS+=("${CROSS}|Step $STEP_COUNT|$1|${elapsed}s")
}

step_end_warn() {
    local elapsed=$(( $(date +%s) - STEP_START ))
    warn "$1 ${DIM}(${elapsed}s)${NC}"
    STEP_RESULTS+=("${WARN}|Step $STEP_COUNT|$1|${elapsed}s")
}

# --- Error handler -----------------------------------------------------------
on_error() {
    local exit_code=$?
    local line_no=$1
    fail "Command failed at line $line_no (exit code: $exit_code)"
    fail "Review the full log: $LOG_FILE"
    print_summary
    cleanup_tmp
    exit $exit_code
}
trap 'on_error $LINENO' ERR

# --- Cleanup on interrupt ----------------------------------------------------
cleanup_tmp() {
    rm -f "${SCRIPT_DIR_EARLY}"/.deploy-cmd-* 2>/dev/null || true
}

on_interrupt() {
    echo ""
    warn "Deployment interrupted by user (Ctrl+C)."
    warn "Partial resources may exist in: ${RESOURCE_GROUP:-unknown}"
    print_summary
    cleanup_tmp
    exit 130
}
trap 'on_interrupt' INT TERM

# --- run_cmd: execute a command with error capture ---------------------------
# Uses temp-file redirection (not $()) so complex args (JSON bodies) stay intact.
# Usage: run_cmd "description" command arg1 arg2 ...
run_cmd() {
    local description="$1"; shift
    local cmd_exit_code=0
    local tmp_out
    tmp_out=$(mktemp "${SCRIPT_DIR_EARLY}/.deploy-cmd-XXXXXX")

    info "${DIM}Running: $*${NC}"
    log_raw ">>> $(date '+%H:%M:%S') | $description"
    log_raw ">>> CMD: $*"

    "$@" > "$tmp_out" 2>&1 || cmd_exit_code=$?

    # Append command output to the main log
    if [ -s "$tmp_out" ]; then
        cat "$tmp_out" >> "$LOG_FILE"
    fi

    if [ $cmd_exit_code -ne 0 ]; then
        fail "$description"
        fail "Exit code: $cmd_exit_code"
        if [ -s "$tmp_out" ]; then
            echo ""
            log "  ${RED}── Error details ──${NC}"
            tail -20 "$tmp_out" | while IFS= read -r line; do
                log "  ${DIM}  ${line}${NC}"
            done
            log "  ${RED}───────────────────${NC}"
            echo ""
        fi
        rm -f "$tmp_out"
        return $cmd_exit_code
    fi

    rm -f "$tmp_out"
    return 0
}

# --- Prerequisite checks -----------------------------------------------------
preflight_check() {
    header "Preflight Checks"

    # az CLI installed?
    if ! command -v az &> /dev/null; then
        fail "Azure CLI (az) is not installed. Install it from https://aka.ms/install-azure-cli"
        exit 1
    fi
    local az_version
    az_version=$(az_q version --query '"azure-cli"' -o tsv 2>/dev/null || echo "unknown")
    success "Azure CLI found (v${az_version})"

    # Logged in?
    if ! az account show &> /dev/null; then
        fail "Not logged in to Azure. Run 'az login' first."
        exit 1
    fi

    local account_name
    account_name=$(az_q account show --query name -o tsv 2>/dev/null)
    local account_id
    account_id=$(az_q account show --query id -o tsv 2>/dev/null)
    success "Authenticated — subscription: ${BOLD}$account_name${NC}"
    info "Subscription ID: ${DIM}$account_id${NC}"

    # jq (optional but nice)
    if command -v jq &> /dev/null; then
        success "jq found"
    else
        warn "jq not found — non-critical, but useful for debugging"
    fi
}

# --- Summary printer ---------------------------------------------------------
print_summary() {
    local total_elapsed=$(( $(date +%s) - DEPLOY_START ))
    local minutes=$((total_elapsed / 60))
    local seconds=$((total_elapsed % 60))

    echo ""
    divider
    log "${BOLD}  Deployment Summary${NC}"
    divider

    for result in "${STEP_RESULTS[@]}"; do
        IFS='|' read -r icon step desc duration <<< "$result"
        printf "  %b  %-8s %-38s %s\n" "$icon" "$step" "$desc" "$duration" | tee -a "$LOG_FILE"
    done

    divider
    log "  ${BOLD}Total time: ${minutes}m ${seconds}s${NC}"
    log "  ${DIM}Full log:   $LOG_FILE${NC}"
    divider
    echo ""
}

# =============================================================================
#  MAIN
# =============================================================================

# --- Configuration -----------------------------------------------------------
SUFFIX="${SUFFIX:-$(openssl rand -hex 4)}"
RESOURCE_GROUP="${RESOURCE_GROUP:-foundry-hackathon-rg-$SUFFIX}"
LOCATION="${LOCATION:-swedencentral}"
FOUNDRY_RESOURCE_NAME="${FOUNDRY_RESOURCE_NAME:-foundry-hack-$SUFFIX}"
PROJECT_NAME="${PROJECT_NAME:-factory-project}"
MODEL_DEPLOYMENT_NAME="${MODEL_DEPLOYMENT_NAME:-gpt-5.4}"
MODEL_NAME="${MODEL_NAME:-gpt-5.4}"
MODEL_VERSION="${MODEL_VERSION:-2026-03-05}"
LOG_ANALYTICS_NAME="${LOG_ANALYTICS_NAME:-foundry-hack-logs-$SUFFIX}"
APP_INSIGHTS_NAME="${APP_INSIGHTS_NAME:-foundry-hack-insights-$SUFFIX}"
ARM_API_VERSION="${ARM_API_VERSION:-2026-03-01}"

echo ""
log "${BOLD}${BLUE}══════════════════════════════════════════════${NC}"
log "${BOLD}${BLUE}  Foundry Hackathon — Infrastructure Deploy${NC}"
log "${BOLD}${BLUE}══════════════════════════════════════════════${NC}"
echo ""
info "Suffix:             ${BOLD}$SUFFIX${NC}"
info "Resource Group:     ${BOLD}$RESOURCE_GROUP${NC}"
info "Location:           ${BOLD}$LOCATION${NC}"
info "Foundry Resource:   ${BOLD}$FOUNDRY_RESOURCE_NAME${NC}"
info "Project:            ${BOLD}$PROJECT_NAME${NC}"
info "Model:              ${BOLD}$MODEL_NAME${NC} (v${MODEL_VERSION})"
info "Log file:           ${DIM}$LOG_FILE${NC}"
echo ""

# --- Preflight ---------------------------------------------------------------
preflight_check
SUBSCRIPTION_ID=$(az_q account show --query id -o tsv)

# --- Step 1: Resource Group --------------------------------------------------
step_start "Resource Group"
run_cmd "Create resource group" \
    az group create \
        --name "$RESOURCE_GROUP" \
        --location "$LOCATION" \
        --output none
step_end_ok "Resource group created"

# --- Step 2: AI Foundry Hub (AIServices) ------------------------------------
step_start "AI Foundry Resource (AIServices)"
run_cmd "Create AIServices account" \
    az rest \
        --method PUT \
        --url "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.CognitiveServices/accounts/$FOUNDRY_RESOURCE_NAME?api-version=$ARM_API_VERSION" \
        --body "{\"kind\": \"AIServices\", \"sku\": {\"name\": \"S0\"}, \"location\": \"$LOCATION\", \"properties\": {\"customSubDomainName\": \"$FOUNDRY_RESOURCE_NAME\", \"publicNetworkAccess\": \"Enabled\", \"allowProjectManagement\": true}}" \
        --output none

info "Waiting for provisioning (polling every 10s, timeout 6min)..."
PROVISIONED=false
for i in $(seq 1 36); do
    PROV_STATE=$(az_q cognitiveservices account show \
        --name "$FOUNDRY_RESOURCE_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --query "properties.provisioningState" -o tsv 2>/dev/null || echo "Pending")

    if [ "$PROV_STATE" = "Succeeded" ]; then
        PROVISIONED=true
        break
    elif [ "$PROV_STATE" = "Failed" ]; then
        fail "AIServices provisioning returned 'Failed'. Check the Azure portal."
        step_end_fail "AIServices provisioning failed"
        exit 1
    fi
    printf "  ${DIM}  [%2d/36] State: %-12s${NC}\r" "$i" "$PROV_STATE"
    sleep 10
done
echo "" # clear the \r line

if [ "$PROVISIONED" = false ]; then
    fail "Timed out waiting for AIServices to provision (360s)."
    step_end_fail "AIServices timed out"
    exit 1
fi

# Enable local auth + project management
FOUNDRY_RESOURCE_ID=$(az_q cognitiveservices account show \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query id -o tsv)

az resource update --ids "$FOUNDRY_RESOURCE_ID" --set properties.disableLocalAuth=false --output none 2>/dev/null || true
az resource update --ids "$FOUNDRY_RESOURCE_ID" --set properties.allowProjectManagement=true --output none 2>/dev/null || true

DISABLE_LOCAL_AUTH=$(az_q cognitiveservices account show \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query properties.disableLocalAuth -o tsv 2>/dev/null || echo "unknown")

if [ "$DISABLE_LOCAL_AUTH" = "true" ]; then
    warn "API key auth disabled by Azure Policy — use DefaultAzureCredential (Entra ID)."
fi

step_end_ok "AIServices provisioned"

# --- Step 3: AI Foundry Project ---------------------------------------------
step_start "AI Foundry Project"
run_cmd "Create project" \
    az cognitiveservices account project create \
        --name "$FOUNDRY_RESOURCE_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --project-name "$PROJECT_NAME" \
        --location "$LOCATION" \
        --output none
step_end_ok "Project '$PROJECT_NAME' created"

# --- Step 4: Model Deployment -----------------------------------------------
step_start "Model Deployment ($MODEL_NAME)"
run_cmd "Deploy model" \
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
step_end_ok "Model '$MODEL_NAME' deployed"

# --- Step 5: Log Analytics ---------------------------------------------------
step_start "Log Analytics Workspace"
run_cmd "Create Log Analytics workspace" \
    az monitor log-analytics workspace create \
        --resource-group "$RESOURCE_GROUP" \
        --workspace-name "$LOG_ANALYTICS_NAME" \
        --location "$LOCATION" \
        --output none

LOG_ANALYTICS_ID=$(az_q monitor log-analytics workspace show \
    --resource-group "$RESOURCE_GROUP" \
    --workspace-name "$LOG_ANALYTICS_NAME" \
    --query id -o tsv)
step_end_ok "Log Analytics created"

# --- Step 6: Application Insights -------------------------------------------
step_start "Application Insights"
run_cmd "Create Application Insights" \
    az monitor app-insights component create \
        --app "$APP_INSIGHTS_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --location "$LOCATION" \
        --workspace "$LOG_ANALYTICS_ID" \
        --output none

APP_INSIGHTS_CONN_STRING=$(az_q monitor app-insights component show \
    --app "$APP_INSIGHTS_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query connectionString -o tsv)

APP_INSIGHTS_INSTRUMENTATION_KEY=$(az_q monitor app-insights component show \
    --app "$APP_INSIGHTS_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query instrumentationKey -o tsv)

APP_INSIGHTS_RESOURCE_ID=$(az_q monitor app-insights component show \
    --app "$APP_INSIGHTS_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query id -o tsv)
step_end_ok "Application Insights created"

# --- Step 7: Connect App Insights to Foundry --------------------------------
step_start "Link App Insights → Foundry Project"
run_cmd "Patch project with App Insights" \
    az rest \
        --method PATCH \
        --url "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.CognitiveServices/accounts/$FOUNDRY_RESOURCE_NAME/projects/$PROJECT_NAME?api-version=$ARM_API_VERSION" \
        --body "{\"properties\": {\"applicationInsights\": \"$APP_INSIGHTS_RESOURCE_ID\"}}" \
        --output none
step_end_ok "App Insights linked to project"

# --- Step 8: Retrieve endpoints & write .env --------------------------------
step_start "Retrieve Endpoints & Write .env"

FOUNDRY_ENDPOINT=$(az_q cognitiveservices account show \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --query "properties.endpoint" -o tsv)

PROJECT_CONNECTION_STRING=$(az_q cognitiveservices account project show \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --project-name "$PROJECT_NAME" \
    --query "properties.endpoints.\"AI Foundry API\"" -o tsv 2>/dev/null || echo "")

ROOT_DIR="$(cd "$SCRIPT_DIR_EARLY/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"

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

success ".env written to: ${BOLD}$ENV_FILE${NC}"
step_end_ok ".env file generated"

# --- Final Summary -----------------------------------------------------------
print_summary

log "${BOLD}${GREEN}══════════════════════════════════════════════${NC}"
log "${BOLD}${GREEN}  ✅ DEPLOYMENT COMPLETE${NC}"
log "${BOLD}${GREEN}══════════════════════════════════════════════${NC}"
echo ""
info "Foundry endpoint:   ${BOLD}$FOUNDRY_ENDPOINT${NC}"
info "Project:            ${BOLD}$PROJECT_NAME${NC}"
info "Model deployment:   ${BOLD}$MODEL_DEPLOYMENT_NAME${NC}"
info ".env file:          ${BOLD}$ENV_FILE${NC}"
info "Full log:           ${DIM}$LOG_FILE${NC}"
cleanup_tmp
echo ""