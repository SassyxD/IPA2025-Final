#!/bin/bash

# IPA2024-Final - Ubuntu Dependencies Installation Script
# This script will install all required dependencies for the project

# Note: We don't use 'set -e' because apt update might have warnings from other repos

echo "=========================================="
echo "IPA2024-Final Dependencies Installation"
echo "=========================================="
echo ""

# Update package list
echo "[1/5] Updating package list..."
sudo apt update || echo "Warning: Some repositories had errors, but continuing..."

# Install pip3 if not installed
echo ""
echo "[2/5] Installing pip3..."
sudo apt install -y python3-pip python3-venv

# Create virtual environment
echo ""
echo "[3/5] Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created successfully!"
else
    echo "Virtual environment already exists. Skipping..."
fi

# Activate virtual environment and install Python packages
echo ""
echo "[4/5] Installing Python packages from requirements.txt..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Install Ansible via apt (recommended for Ubuntu)
echo ""
echo "[5/5] Installing Ansible via apt..."
sudo apt install -y ansible

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Set environment variables: source set_env.sh"
echo "3. Run the main program: python3 ipa2024_final.py"
echo ""
echo "Note: Make sure to configure set_env.sh with your credentials first!"
