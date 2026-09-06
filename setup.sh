#!/bin/bash
set -e

# Check if uv is installed
if ! command -v uv &>/dev/null; then
    echo "uv is not installed. Please install it first."
    echo "Visit https://github.com/astral-sh/uv for installation instructions."
    exit 1
fi

# Check if src directory exists
if [ ! -d "src" ]; then
    echo "src directory not found. Please run ./reorganize.sh first."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
uv venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install the package in development mode
echo "Installing package and dependencies..."
uv pip install -e .

# Install development dependencies
echo "Installing development dependencies..."
uv pip install -e ".[dev]"

# Set up pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install

echo "Setup complete! You can now activate the environment with:"
echo "source .venv/bin/activate"
