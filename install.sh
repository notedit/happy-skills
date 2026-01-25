#!/bin/bash
set -e

# Happy Skills CLI Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/notedit/happy-skills/main/install.sh | bash

HCA_VERSION="1.0.0"
HCA_REPO="https://github.com/notedit/happy-skills"
INSTALL_DIR="${HOME}/.local/bin"

echo "========================================"
echo " Happy Skills CLI Installer"
echo " Version: ${HCA_VERSION}"
echo "========================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Found Python ${PYTHON_VERSION}"

# Check if version is 3.8+
MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
    echo "Error: Python 3.8+ is required (found ${PYTHON_VERSION})"
    exit 1
fi

# Method 1: Try pipx (recommended)
if command -v pipx &> /dev/null; then
    echo ""
    echo "Installing via pipx..."
    pipx install "git+${HCA_REPO}.git" || {
        echo "pipx install failed, trying pip..."
    }

    if command -v hca &> /dev/null; then
        echo ""
        echo "Installation complete!"
        echo "Run 'hca --help' to get started."
        exit 0
    fi
fi

# Method 2: Try pip with --user
echo ""
echo "Installing via pip..."
pip3 install --user "git+${HCA_REPO}.git"

# Check if installation was successful
if python3 -c "import cli" 2>/dev/null; then
    echo ""
    echo "========================================"
    echo " Installation Complete!"
    echo "========================================"
    echo ""

    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo "NOTE: Add the following to your shell profile:"
        echo ""
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo ""
        echo "Then restart your shell or run:"
        echo ""
        echo "  source ~/.bashrc  # or ~/.zshrc"
        echo ""
    fi

    echo "To get started, run:"
    echo ""
    echo "  hca --help"
    echo ""
    echo "To initialize a project:"
    echo ""
    echo "  cd your-project"
    echo "  hca init"
    echo ""
else
    echo ""
    echo "Installation may have failed. Please try:"
    echo ""
    echo "  pip3 install git+${HCA_REPO}.git"
    echo ""
    exit 1
fi
