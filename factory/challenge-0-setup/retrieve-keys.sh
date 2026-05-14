#!/bin/bash
set -euo pipefail

# =============================================================================
# Foundry Hackathon — Retrieve Missing Keys from Existing Resources
# Retrieves PROJECT_CONNECTION_STRING without redeploying
# =============================================================================

# Get environment variables from existing .env file if it exists
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"
LEGACY_ENV_FILE="$SCRIPT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$LEGACY_ENV_FILE" ]; then
        echo "⚠️  Root .env not found. Using legacy file: $LEGACY_ENV_FILE"
        cp "$LEGACY_ENV_FILE" "$ENV_FILE"
        echo "✅ Migrated legacy .env to: $ENV_FILE"
    else
        echo "❌ Error: .env file not found at $ENV_FILE"
        echo "Please run deploy.sh first to create the infrastructure."
        exit 1
    fi
fi

# Source the existing .env to get resource names
set +u  # temporarily disable unset variable check for sourcing
source "$ENV_FILE"
set -u

echo "=============================================="
echo "  Retrieving Missing Keys"
echo "=============================================="
echo ""
echo "Resource Group:    $RESOURCE_GROUP"
echo "Foundry Endpoint:  $FOUNDRY_ENDPOINT"
echo ""

# --- Retrieve PROJECT_CONNECTION_STRING ----
echo ">>> Retrieving PROJECT_CONNECTION_STRING..."
PROJECT_CONNECTION_STRING=$(az cognitiveservices account project show \
    --name "$FOUNDRY_RESOURCE_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --project-name "$PROJECT_NAME" \
    --query "properties.endpoints.\"AI Foundry API\"" -o tsv 2>/dev/null || echo "")

if [ -n "$PROJECT_CONNECTION_STRING" ]; then
    echo "    ✓ Set to: $PROJECT_CONNECTION_STRING"
else
    echo "    ⚠️  Could not retrieve project endpoint. Falling back to FOUNDRY_ENDPOINT."
    PROJECT_CONNECTION_STRING="$FOUNDRY_ENDPOINT"
fi

# --- Update .env file -------
echo ""
echo ">>> Updating .env file..."

# Update PROJECT_CONNECTION_STRING
if grep -q "^PROJECT_CONNECTION_STRING=" "$ENV_FILE"; then
    sed -i "s|^PROJECT_CONNECTION_STRING=.*|PROJECT_CONNECTION_STRING=$PROJECT_CONNECTION_STRING|" "$ENV_FILE"
else
    echo "PROJECT_CONNECTION_STRING=$PROJECT_CONNECTION_STRING" >> "$ENV_FILE"
fi
echo "    ✓ Updated PROJECT_CONNECTION_STRING"

echo ""
echo "=============================================="
echo "  ✅ KEYS RETRIEVED"
echo "=============================================="
echo ""
echo "Updated .env file: $ENV_FILE"
echo ""
echo "Current values:"
echo "  PROJECT_CONNECTION_STRING=$PROJECT_CONNECTION_STRING"
echo ""
