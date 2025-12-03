#!/bin/bash
# train_model.sh - Train the spam classifier

set -e

echo "🤖 Training SpamShieldAI model..."

cd /workspaces/spamshieldai

# Ensure virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run training script
python src/models/train.py

echo "✅ Model training complete!"
echo "📍 Model saved to: models/spam_classifier.pkl"
echo "📍 Vectorizer saved to: models/vectorizer.pkl"
