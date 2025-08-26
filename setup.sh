#!/bin/bash
# Setup script for the number generation analysis project.
# This script runs when the Pixi environment is activated.

echo "🔧 Setting up number generation analysis environment..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    if [ -f env_example.txt ]; then
        cp env_example.txt .env
        echo "✅ Created .env file from env_example.txt"
    else
        echo "⚠️  env_example.txt not found. Please create .env file manually."
    fi
else
    echo "✅ .env file already exists"
fi

echo "🚀 Environment setup complete!"
echo ""
echo "📋 Available commands:"
echo "  pixi run test    - Test the setup"
echo "  pixi run quick   - Run quick analysis"
echo "  pixi run full    - Run full analysis"
echo "  pixi run example - Run example analyses" 