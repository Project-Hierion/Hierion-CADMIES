#!/usr/bin/env bash
# ============================================================================
# CADMIES Paperspace Startup
# ============================================================================
# Installs everything needed for a fresh Paperspace machine:
# system deps, Ollama, Python packages, models.
# Run once per session: bash scripts/startup.sh
# ============================================================================

echo "🚀 CADMIES Paperspace Startup"
echo "=============================="

# ----------------------------------------
# Step 1: Install system dependencies
# ----------------------------------------
echo "[1/5] Installing system packages..."
apt-get update -qq && apt-get install -y -qq zstd curl > /dev/null 2>&1
echo "   ✅ zstd, curl"

# ----------------------------------------
# Step 2: Install Ollama
# ----------------------------------------
echo "[2/5] Installing Ollama..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh > /dev/null 2>&1
    echo "   ✅ Ollama installed"
else
    echo "   ✅ Ollama already installed"
fi

# ----------------------------------------
# Step 3: Install Python packages
# ----------------------------------------
echo "[3/5] Installing Python packages..."
pip install ollama dag_cbor multiformats -q 2>&1 | tail -1
echo "   ✅ ollama, dag_cbor, multiformats"

# ----------------------------------------
# Step 4: Launch Ollama
# ----------------------------------------
echo "[4/5] Starting Ollama..."
ollama serve &
sleep 3
echo "   ✅ Ollama running"

# ----------------------------------------
# Step 5: Pull models
# ----------------------------------------
echo "[5/5] Pulling models..."
ollama pull mistral:7b
echo "   ✅ mistral:7b"
echo ""
echo "✅ Ready!"
echo ""
echo "To pull additional models:"
echo "  ollama pull codestral:22b"
echo "  ollama pull tinyllama:1.1b"
echo ""
echo "To start harvesting:"
echo "  python tools/harvest/harvest_full_pipeline.py --auto --with-relationships"