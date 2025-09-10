#!/bin/bash

# Self-Hosted Runner Setup Script for NickScherbakov-dashboard
# This script helps prepare a self-hosted runner environment

set -e

echo "🚀 Setting up self-hosted runner environment for NickScherbakov-dashboard"
echo "=================================================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "⚠️  This script should not be run as root for security reasons"
   echo "Please run as a regular user with sudo privileges"
   exit 1
fi

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "❌ Unsupported operating system: $OSTYPE"
    exit 1
fi

echo "🖥️  Detected OS: $OS"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python installation
echo "🐍 Checking Python installation..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | grep -oE '[0-9]+\.[0-9]+')
    echo "✅ Python 3 found: $(python3 --version)"
    
    # Check if version is 3.7+
    if python3 -c "import sys; exit(0 if sys.version_info >= (3,7) else 1)"; then
        echo "✅ Python version is compatible"
    else
        echo "❌ Python 3.7+ required, found: $PYTHON_VERSION"
        exit 1
    fi
else
    echo "❌ Python 3 not found"
    echo "Please install Python 3.7+ before running this script"
    exit 1
fi

# Check Git installation
echo "📋 Checking Git installation..."
if command_exists git; then
    echo "✅ Git found: $(git --version)"
else
    echo "❌ Git not found"
    echo "Please install Git before running this script"
    exit 1
fi

# Check pip installation
echo "📦 Checking pip installation..."
if command_exists pip3; then
    echo "✅ pip3 found"
elif command_exists pip; then
    echo "✅ pip found"
else
    echo "❌ pip not found"
    echo "Please install pip before running this script"
    exit 1
fi

# Install Python dependencies
echo "📚 Installing Python dependencies..."
PYTHON_CMD=$(command -v python3 || command -v python)
PIP_CMD=$(command -v pip3 || command -v pip)

echo "Using Python: $PYTHON_CMD"
echo "Using pip: $PIP_CMD"

# Create virtual environment (optional but recommended)
echo "🔧 Setting up virtual environment..."
if [[ ! -d "runner-env" ]]; then
    $PYTHON_CMD -m venv runner-env
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
source runner-env/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip

# Install required packages
echo "📦 Installing required Python packages..."
pip install requests>=2.25.0 matplotlib>=3.3.0 seaborn>=0.11.0 pandas>=1.2.0

echo "✅ All dependencies installed successfully"

# Check system resources
echo "💻 Checking system resources..."
echo "Memory:"
if [[ "$OS" == "linux" ]]; then
    free -h
elif [[ "$OS" == "macos" ]]; then
    echo "$(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024" GB"}')"
fi

echo "Disk space:"
df -h .

echo "CPU info:"
if [[ "$OS" == "linux" ]]; then
    nproc
    echo "cores"
elif [[ "$OS" == "macos" ]]; then
    sysctl -n hw.ncpu
    echo "cores"
fi

# Create runner directory
echo "📁 Creating runner directory..."
RUNNER_DIR="$HOME/actions-runner"
if [[ ! -d "$RUNNER_DIR" ]]; then
    mkdir -p "$RUNNER_DIR"
    echo "✅ Runner directory created: $RUNNER_DIR"
else
    echo "✅ Runner directory already exists: $RUNNER_DIR"
fi

echo ""
echo "🎉 Environment setup complete!"
echo "=================================================================="
echo ""
echo "Next steps:"
echo "1. Navigate to: https://github.com/NickScherbakov/NickScherbakov-dashboard/settings/actions/runners/new"
echo "2. Follow the instructions to download and configure the runner"
echo "3. Use the runner directory: $RUNNER_DIR"
echo "4. When configuring, consider adding these labels:"
echo "   - dashboard-runner"
echo "   - $OS"
echo ""
echo "📖 For detailed instructions, see: docs/SELF_HOSTED_RUNNERS.md"
echo ""
echo "🔧 To activate the virtual environment later:"
echo "   source $(pwd)/runner-env/bin/activate"
echo ""
echo "⚠️  Security reminder:"
echo "   - Keep your runner machine secure and updated"
echo "   - Only run trusted workflows"
echo "   - Monitor runner activity regularly"