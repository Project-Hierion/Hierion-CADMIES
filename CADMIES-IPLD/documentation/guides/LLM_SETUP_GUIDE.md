# LLM Setup Guide for CADMIES

**How to install and configure a local LLM for Willie the Librarian and the CADMIES mycelium.**

---

## Overview

CADMIES uses [Ollama](https://ollama.com) to run large language models locally on your machine. No API keys, no cloud services, no data leaving your computer. Willie the Librarian reads your mycelium and uses the LLM to synthesize answers, cross-reference concepts, and explain complex ideas in natural language.

---

## Step 1: Install Ollama

### Linux

```
curl -fsSL https://ollama.com/install.sh | sh
```

### macOS

Download from [ollama.com/download](https://ollama.com/download) or use Homebrew:

```
brew install ollama
```

### Windows

Download the installer from [ollama.com/download](https://ollama.com/download).

### Fedora Silverblue / Immutable Systems

Use a toolbox container:

```
toolbox create ollama-mistral
toolbox enter ollama-mistral
sudo dnf install ollama -y
```

Run `ollama serve` inside the toolbox. The CADMIES Python client on the host will connect via `localhost:11434`.

---

## Step 2: Pull a Model

CADMIES supports any Ollama-compatible model. Two are recommended:

### Mistral 7B (Recommended — Deep Reasoning)

```
ollama pull mistral:7b
```

- **Size:** 4.4 GB
- **Best for:** Complex reasoning, cross-domain synthesis, fact-checking, multi-concept analysis
- **Speed:** ~2.5s to load, responses in 30-90s on CPU

### TinyLlama 1.1B (Fast Queries)

```
ollama pull tinyllama:1.1b
```

- **Size:** 637 MB
- **Best for:** Quick concept lookups, simple retrieval, low-resource environments
- **Speed:** ~2s to load, responses in 10-30s on CPU

### Other Compatible Models

Any model on [ollama.com/library](https://ollama.com/library) will work:

| Model | Size | Notes |
|-------|------|-------|
| `llama3.2:1b` | 1.3 GB | Good balance of speed and quality |
| `phi:latest` | 1.6 GB | Microsoft's compact reasoning model |
| `llama3.2:3b` | 2.0 GB | Stronger reasoning, still compact |
| `llama3.1:8b` | 4.9 GB | Full-sized general purpose model |

---

## Step 3: Start Ollama

Open a **separate terminal** and run:

```
ollama serve
```

Leave this terminal running. Ollama listens on `http://localhost:11434`.

To verify it's working, open another terminal and run:

```
curl http://localhost:11434/api/tags
```

You should see a JSON response listing your downloaded models.

---

## Step 4: Install the Python Client

In your CADMIES virtual environment:

```
pip install ollama
```

---

## Step 5: Test Willie

```
python agents/code/llm_mycelium_reader_v1.1.0.py --test
```

All four tests should pass:
1. Ollama connectivity
2. Mycelium access
3. Concept search
4. Live LLM query

---

## Step 6: Ask Your First Question

```
python agents/code/llm_mycelium_reader_v1.1.0.py --query "What is natural selection?" --model mistral:7b
```

For faster responses on simple queries:

```
python agents/code/llm_mycelium_reader_v1.1.0.py --query "What concepts relate to physics?" --model tinyllama:1.1b
```

---

## Troubleshooting

### "ollama: command not found"

Ollama is not installed or not in your PATH. Run the install script again or restart your terminal.

### "Connection refused" on localhost:11434

Ollama server is not running. Run `ollama serve` in a separate terminal.

### "model not found"

You haven't pulled the model yet. Run `ollama pull mistral:7b` (or your preferred model).

### "CUDA/ROCm error" or GPU warnings

Expected on CPU-only systems. Ollama will run on CPU automatically. Performance will be slower but fully functional.

### Slow responses (5+ minutes)

Running on CPU is expected to be slower. Use TinyLlama for faster responses, or keep Mistral loaded persistently:

```
OLLAMA_KEEP_ALIVE=24h ollama serve
```

This keeps the model in RAM between queries, reducing load times to near-instant after the first query.

### Toolbox / Silverblue users

If Ollama stops when you close the toolbox terminal, keep it running in a dedicated terminal tab:

```
toolbox enter ollama-mistral
ollama serve
```

Leave this tab open. Run CADMIES commands from your host terminal.

---

## Model Storage

Models are stored in `~/.ollama/models/` by default. Mistral 7B uses ~4.4 GB, TinyLlama ~637 MB. To change the storage location:

```
export OLLAMA_MODELS=/path/to/your/storage
```

Add this to your `~/.bashrc` or `~/.zshrc` to make it permanent.

---

## Next Steps

- Read the [CADMIES Agents README](../agents/README.md) to understand the agent framework
- Try different `--tone` options: `helpful`, `scholarly`, `casual`, `scottish`
- Increase `--max-concepts` to 5 for broader context
- Experiment with accuracy tags in responses

---

> *"The LLM is not the mycelium. It is the voice that reads the mycelium to those who cannot yet see."* — CADMIES Vision
