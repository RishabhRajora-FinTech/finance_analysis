#!/bin/bash

set -e  # exit on any error

echo "🔄 Removing old venv..."
rm -rf venv_fin

echo "📦 Creating new virtual environment with Python 3.11..."
/opt/homebrew/bin/python3.11 -m venv venv_fin

echo "✅ Activating virtual environment..."
source venv_fin/bin/activate

echo "⬆️ Upgrading pip, setuptools, wheel..."
pip install --upgrade pip setuptools wheel

echo "📦 Installing required packages (compatible versions)..."
pip install numpy==1.24.4 plotly==5.20.0 streamlit pandas matplotlib yfinance

echo "✅ All packages installed."
echo "🚀 Launching Streamlit app..."

streamlit run app.py
