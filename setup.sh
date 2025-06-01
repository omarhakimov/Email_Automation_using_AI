#!/bin/bash

# AI Email Automation Setup Script
echo "🚀 Setting up AI Email Automation System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Set up your API keys:"
echo "   export OPENAI_API_KEY='your-openai-api-key'"
echo "   export DEEPSEEK_API_KEY='your-deepseek-api-key'"
echo ""
echo "2. Configure Gmail API:"
echo "   - Download credentials.json from Google Cloud Console"
echo "   - Place it in the project root directory"
echo ""
echo "3. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "4. Run the models:"
echo "   python naive_bayes.py"
echo "   jupyter notebook  # for bert.ipynb and RoBERTa_Project.ipynb"
echo ""
echo "📚 See README.md for detailed usage instructions"
