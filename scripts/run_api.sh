#!/bin/bash
# run_api.sh - Start the Flask API server

set -e

echo "🚀 Starting SpamShieldAI API server..."

cd /workspaces/spamshieldai

# Ensure virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Set environment variables
export FLASK_APP=deployment/api/app.py
export FLASK_ENV=development
export PYTHONPATH=/workspaces/spamshieldai:$PYTHONPATH

# Run API
echo "🌐 API running on http://localhost:5000"
python deployment/api/app.py
