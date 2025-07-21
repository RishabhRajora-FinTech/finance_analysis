#!/bin/bash

# Stop script on error
set -e

echo "📁 Creating virtual environment..."
python3 -m venv venv

echo "✅ Virtual environment created."

echo "📦 Activating virtual environment..."
source venv/bin/activate

echo "⬆️ Upgrading pip..."
pip install --upgrade pip

echo "📄 Installing required Python packages..."
pip install -r requirements.txt

echo "✅ All packages installed successfully!"
echo "🟢 You can now run your script with: source venv/bin/activate && python clip_creator.py"
python clip_creator.py