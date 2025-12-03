#!/bin/bash
# setup.sh - Initialize development environment

set -e

echo "🚀 Setting up SpamShieldAI development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -e .
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Create necessary data directories with gitkeep files
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/interim/.gitkeep
touch data/external/.gitkeep

echo "✅ Development environment setup complete!"
echo "📝 Next steps:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Train the model: python src/models/train.py"
echo "   3. Run the API: python deployment/api/app.py"
