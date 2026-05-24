#!/usr/bin/env bash
# ============================================================================
# CADMIES Public Setup — Linux/macOS
# ============================================================================
# Installs everything needed to run CADMIES. One command, no confusion.
# Usage: bash setup.sh
# ============================================================================

set -e

echo "============================================"
echo "  CADMIES Setup"
echo "  The mycelium welcomes you. 🌱🍄"
echo "============================================"
echo ""

# Detect OS
OS="$(uname -s)"
echo "👋 Hey! Detected: $OS"
echo "   This'll take about 30 seconds. Grab a sip of coffee. ☕"
echo ""

# ----------------------------------------
# Step 1: Check Python
# ----------------------------------------
echo "[1/4] Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "❌ Python not found. Please install Python 3.10+ first:"
    echo "   https://www.python.org/downloads/"
    exit 1
fi
echo "   ✅ $($PYTHON --version)"
echo ""

# ----------------------------------------
# Step 2: Create virtual environment
# ----------------------------------------
echo "[2/4] Setting up virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON -m venv venv
    echo "   ✅ Created venv/"
else
    echo "   ⏭️  venv/ already exists — skipping"
fi

# Activate
source venv/bin/activate
echo "   ✅ Activated"
echo ""

# ----------------------------------------
# Step 3: Install Python dependencies
# ----------------------------------------
echo "[3/4] Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet dag_cbor
echo "   ✅ dag_cbor installed"
echo ""

# ----------------------------------------
# Step 4: Optional — Ollama for AI features
# ----------------------------------------
echo "[4/4] AI features (optional)..."
if command -v ollama &> /dev/null; then
    echo "   ✅ Ollama already installed"
else
    echo "   💡 Want the AI features? Install Ollama:"
    echo "      curl -fsSL https://ollama.com/install.sh | sh"
    echo "      Then: ollama pull mistral:7b"
    echo "   Or skip this — the map and library work without it."
fi
echo ""

# ----------------------------------------
# Done
# ----------------------------------------
echo "============================================"
echo "  ✅ All done!"
echo "============================================"
echo ""
echo "  Next steps:"
echo "  1. Download cadmies_latest.car from:"
echo "     https://github.com/Hieros-CADMIES/CADMIES/releases"
echo "  2. Drop it in the incoming_cars/ folder"
echo "  3. Run: python tools/import_from_car.py incoming_cars/cadmies_latest.car"
echo "  4. Run: python tools/generate_mycelium_map.py"
echo "  5. Open mycelium_map.html in your browser"
echo ""
echo "  The garden is alive. 🌱🍄"
echo ""