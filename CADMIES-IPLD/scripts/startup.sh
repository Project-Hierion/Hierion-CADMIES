#!/bin/bash
echo "🚀 CADMIES Paperspace Startup"
apt-get update -qq && apt-get install -y -qq zstd 2>/dev/null
curl -fsSL https://ollama.com/install.sh | sh 2>/dev/null
pkill ollama 2>/dev/null; ollama serve &
sleep 3
pip install -q dag-cbor ollama 2>/dev/null
echo "✅ Ready!"
