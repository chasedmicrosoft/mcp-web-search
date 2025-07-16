#!/bin/bash

# Setup script for AI Web Search MCP Server
# This script creates a Python virtual environment and installs dependencies

set -e

echo "Setting up AI Web Search MCP Server..."

# Check for Python 3.12 (via Homebrew) first, then fall back to system Python
if command -v /opt/homebrew/bin/python3.12 &> /dev/null; then
    PYTHON_CMD="/opt/homebrew/bin/python3.12"
    echo "Using Python 3.12 from Homebrew"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    # Check Python version
    python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    required_version="3.10"
    
    if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
        echo "Error: Python $required_version or higher is required. Found Python $python_version"
        echo "Please install Python 3.10+ or use: brew install python@3.12"
        exit 1
    fi
else
    echo "Error: Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment with $PYTHON_CMD..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete! 🎉"
echo ""
echo "To use the MCP server:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the server: python ai-web-search.py"
echo ""
echo "To deactivate the virtual environment: deactivate"