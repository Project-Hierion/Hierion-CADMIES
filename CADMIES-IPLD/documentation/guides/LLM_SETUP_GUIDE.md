# LLM Setup Guide for CADMIES

**How to install and configure a local LLM for Willie the Librarian on CPU-only systems (no GPU required).**

---

## Overview

CADMIES uses [Ollama](https://ollama.com) to run large language models locally on your machine. No API keys, no cloud services, no data leaving your computer. Willie the Librarian reads your mycelium and uses the LLM to synthesize answers, cross-reference concepts, and explain complex ideas in natural language.

This guide is written for **CPU-only systems** (no dedicated graphics card). The setup has been tested on a 13-year-old PC with 24GB RAM, an Intel integrated GPU, and a Sandisk SSD running Fedora Silverblue 44. If this works on that hardware, it'll work on yours.

**If you have a GPU (NVIDIA CUDA or AMD ROCm):** Ollama will automatically detect and use it. Your inference will be much faster. The NiceGUI web-based GUI (retired for CPU) may work well on your system since your response times will be under 5 seconds.

Willie v1.2.1 uses **hybrid search**: keyword matching combined with Mistral-powered semantic query expansion. This allows the mycelium to find concepts even when your vocabulary differs from the concept's technical terminology — the Mycelial Rosetta Effect in action.

---

## System Requirements

### Minimum (CPU-only, tested working)

| Component | Spec |
|-----------|------|
| RAM | 8GB (Mistral 7B uses ~5GB when loaded) |
| Storage | 10GB free (models are 4-5GB each) |
| CPU | Any x86_64 with AVX support |
| OS | Linux (Fedora Silverblue, Ubuntu, Debian), macOS, Windows |

### Tested Configuration (CADMIES Development Machine)

| Component | Spec |
|-----------|------|
| RAM | 24GB |
| Storage | Sandisk Extreme SSD (USB 3) |
| CPU | Intel integrated graphics, 4 cores |
| OS | Fedora Silverblue 44 |
| Models | Mistral 7B (4.4GB) + TinyLlama 1.1B (637MB) |
| Inference time | 30-120 seconds for Mistral, 10-30 seconds for TinyLlama |

---

## Step 1: Install Ollama

### Linux

backtickbash
curl -fsSL https://ollama.com/install.sh | sh
backtick

### macOS

Download from [ollama.com/download](https://ollama.com/download) or use Homebrew:

backtickbash
brew install ollama
backtick

### Windows

Download the installer from [ollama.com/download](https://ollama.com/download).

### Fedora Silverblue / Immutable Systems (Our Setup)

Use a toolbox container to keep the OS clean:

backtickbash
toolbox create ollama-mistral
toolbox enter ollama-mistral
sudo dnf install ollama -y
backtick

Run `ollama serve` inside the toolbox. The CADMIES Python client on the host connects via `localhost:11434`.

---

## Step 2: Pull Models

### Mistral 7B (Recommended — Deep Reasoning)

backtickbash
ollama pull mistral:7b
backtick

- **Size:** 4.4 GB
- **RAM usage:** ~5GB when loaded
- **Best for:** Complex reasoning, cross-domain synthesis, philosophical analysis
- **Speed on CPU:** 30-120 seconds per query (depends on query complexity and concept count)

### TinyLlama 1.1B (Fast Queries)

backtickbash
ollama pull tinyllama:1.1b
backtick

- **Size:** 637 MB
- **RAM usage:** ~1GB when loaded
- **Best for:** Quick lookups, simple questions, testing
- **Speed on CPU:** 10-30 seconds per query

### CPU-Friendly Model Strategy

| Model | Size | RAM | Use Case |
| Codestral 22B | 12 GB | ~14GB | Maximum depth, library audits (GPU recommended) |
|-------|------|-----|----------|
| TinyLlama 1.1B | 637 MB | ~1GB | Quick answers, simple retrieval |
| Mistral 7B | 4.4 GB | ~5GB | Deep reasoning, cross-domain synthesis |

On CPU-only systems, **keep Mistral warm** to avoid cold-start delays:

backtickbash
# Start Ollama with 24-hour keep-alive (model stays in RAM)
OLLAMA_KEEP_ALIVE=24h ollama serve &
backtick

Without keep-alive, the model unloads after 5 minutes of inactivity and must reload on the next query (20-30 second delay on our test system).

### GPU Acceleration (Paperspace)

CADMIES supports cloud GPU acceleration via Paperspace Gradient. A free A4000 GPU (16GB VRAM) handles inference in seconds. See the main README for setup instructions.

---

## Step 3: Start Ollama

Open a **dedicated terminal** (keep it running forever):

### Standard Linux/macOS:

backtickbash
OLLAMA_KEEP_ALIVE=24h ollama serve &
backtick

### Fedora Silverblue (our setup):

backtickbash
toolbox enter ollama-mistral
OLLAMA_KEEP_ALIVE=24h ollama serve &
backtick

Ollama listens on `http://localhost:11434`. Verify it's working:

backtickbash
curl http://localhost:11434/api/tags
backtick

---

## Step 4: Install Python Client

In your CADMIES virtual environment:

backtickbash
pip install ollama
backtick

---

## Step 5: Test Willie

backtickbash
python agents/code/llm_mycelium_reader.py --test
backtick

All tests should pass:
1. ✅ Ollama connectivity
2. ✅ Mycelium access (concept count)
3. ✅ Keyword search
4. ✅ Hybrid search (keyword + semantic)
5. ✅ Live LLM query

---

## Step 6: Ask Your First Question

### Terminal:

backtickbash
# Deep reasoning
python agents/code/llm_mycelium_reader.py --query "What is the Mycelial Rosetta Effect?" --model mistral:7b

# Quick query
python agents/code/llm_mycelium_reader.py --query "List concepts about biology" --model tinyllama:1.1b
backtick

### GUI:

backtickbash
cd cadmies-gui
python tkinter_main.py
backtick

Then navigate to "👓 Willie Chat" in the sidebar. Select your model, tone, and max concepts, then type your question.

---

## CPU Performance Expectations

**Mistral 7B on CPU (our tested timings):**

| Query Type | Concepts | Approx Time |
|------------|----------|-------------|
| Simple: "hi" | 3 | 30-60 seconds |
| Moderate: "What is natural selection?" | 5 | 60-120 seconds |
| Deep: "Explain the Rosetta Effect" | 10 | 2-5 minutes |
| Very Deep: Complex philosophy | 20+ | 5-20 minutes |

**TinyLlama 1.1B on CPU:**

| Query Type | Concepts | Approx Time |
|------------|----------|-------------|
| Any | Any | 10-30 seconds |

The GUI uses a **20-minute timeout** to accommodate deep philosophical queries. The terminal uses a default 300-second (5-minute) timeout. Adjust in the script if needed.

**Why so slow?** Mistral 7B has 7.25 billion parameters. On CPU, every token requires sequential processing through all layers. A GPU parallelizes this. Our development machine has no dedicated GPU — everything runs on the Intel integrated chip. If your system has an NVIDIA GPU, Ollama will detect it automatically, and these times drop to 2-10 seconds.

---

## Troubleshooting

### "ollama: command not found"
Ollama not installed or not in PATH. Re-run the install or restart terminal.

### "Connection refused" on localhost:11434
Ollama server not running. Run `ollama serve` in a dedicated terminal.

### "model not found"
Pull the model first: `ollama pull mistral:7b`

### Slow responses (5+ minutes)
This is normal on CPU. Options:
- Use TinyLlama for faster responses
- Reduce max concepts (5 instead of All)
- Keep model warm with `OLLAMA_KEEP_ALIVE=24h`
- Consider upgrading to a system with a GPU

### "CUDA/ROCm error" or GPU warnings
Expected on CPU-only systems. Ollama will run on CPU automatically. The warning is informational, not an error.

### GUI connection drops
The Tkinter GUI uses a threaded architecture and should not drop connections. If the GUI freezes, the Ollama query is still running in the background — wait for it. The mockingbird chirp will notify you when it's done.

### Toolbox / Silverblue: Ollama stops when terminal closes
Keep the toolbox terminal open, or run Ollama as a background process:

backtickbash
toolbox enter ollama-mistral
nohup ollama serve > /tmp/ollama.log 2>&1 &
backtick

---

## Model Storage

Models are stored in `~/.ollama/models/`. Mistral 7B uses ~4.4 GB, TinyLlama ~637 MB. To change storage location:

backtickbash
export OLLAMA_MODELS=/path/to/your/storage
backtick

Add to `~/.bashrc` for permanent change.

---

> *"The LLM is not the mycelium. It is the voice that reads the mycelium to those who cannot yet see. On CPU, it speaks slowly. But it speaks true."* — CADMIES Development Team, 2026
