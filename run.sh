#!/bin/bash

# IPA2024-Final - Quick Run Script

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: ./install_dependencies.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Load environment variables
if [ -f "set_env.sh" ]; then
    source set_env.sh
else
    echo "Warning: set_env.sh not found!"
    echo "Please configure your environment variables."
    exit 1
fi

# Run the main program
echo "Starting IPA2024-Final Bot..."
python3 ipa2024_final.py
