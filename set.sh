#!/bin/bash

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed. Please install Python3 and try again."
    exit 1
fi

# Check if venv already exists
if [ -d "venv" ]; then
    echo "Virtual environment already exists."
    echo "To recreate it, delete the 'venv' folder and rerun this script."
else
    # Create a virtual environment
    echo "Creating virtual environment..."
    python3 -m venv venv

    if [ ! -d "venv" ]; then
        echo "Error: Failed to create a virtual environment."
        exit 1
    fi
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # macOS/Linux
    source venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found. No dependencies were installed."
fi

# Final message
echo "Setup complete. To activate the virtual environment manually, run:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "source venv/Scripts/activate"
else
    echo "source venv/bin/activate"
fi
