#!/usr/bin/env bash
set -euo pipefail

# A helpful script to initialize a Railway project and set common environment variables for the API.
# Note: You must have the Railway CLI installed and be logged in.

if ! command -v railway >/dev/null 2>&1; then
  echo "Please install the Railway CLI and run 'railway login' first: https://docs.railway.app/cli"
  exit 1
fi

echo "Initializing Railway project for SpamShield API..."
railway init --yes || true

echo "Add environment variables. Set the FRONTEND_URL to your frontend's deployed url."
read -p "Frontend URL (example: https://spamshield-frontend-production.up.railway.app): " FRONTEND_URL

railway variables set CORS_ORIGINS="$FRONTEND_URL" || true
railway variables set MODELS_DIR="/app/models" || true
read -p "Add optional MODEL_BASE_URL if you use remote models (leave blank to skip): " MODEL_BASE_URL
if [ -n "$MODEL_BASE_URL" ]; then
  railway variables set MODEL_BASE_URL="$MODEL_BASE_URL" || true
fi

echo "Variables configured. You can now run 'railway up' or use the dashboard to configure more settings."
