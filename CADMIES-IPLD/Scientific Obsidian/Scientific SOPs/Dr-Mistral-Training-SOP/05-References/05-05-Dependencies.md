---
sop: Dr-Mistral-Training-SOP
section: References
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[03-Prerequisites]], [[04-01-Environment-Setup]]"
---

# 05-05 — Dependencies

Complete dependency reference for Dr. Mistral training.

## requirements.txt

File: `/notebooks/requirements.txt`

```text
datasets
accelerate==0.27.2
transformers==4.40.0
trl==0.9.6
rich
bitsandbytes==0.41.1
torch
peft
```

## Locked Versions

|Package|Version|Notes|
|---|---|---|
|torch|2.1.1|Fixed — Paperspace CUDA environment|
|transformers|4.40.0|Mistral tokenizer support|
|trl|0.9.6|Compatible with transformers 4.40.0|
|peft|0.6.2|LoRA support|
|datasets|2.18.0|Dataset loading|
|bitsandbytes|0.41.1|NOT 0.41.2 — adapter loading bug|
|accelerate|0.27.2|Compatible with bitsandbytes 0.41.x|
|rich|latest|Required by TRL|

## Critical Version Notes

### bitsandbytes — DO NOT use 0.41.2

Version 0.41.2 intercepts `load_state_dict` and crashes on LoRA  
weights. Always use 0.41.1.

### torch — Fixed to 2.1.1

The Paperspace environment uses CUDA 12.4. Torch 2.1.1 is the matching  
build.

### transformers — 4.40.0

Mistral tokenizer support, PyTorch 2.1.1 compatible.

## System Dependencies

|Package|Purpose|
|---|---|
|zstd|Required by Ollama installer|
|Ollama|Model serving|

## Installation

### System packages

```bash
# Install zstd if missing
if ! command -v zstd &> /dev/null; then
    apt-get update -qq && apt-get install -y -qq zstd
fi
# Install Ollama if missing
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
fi
```

### Python dependencies

```bash
pip install -r /notebooks/requirements.txt -q
```

## Environment Snapshot

File: `/notebooks/.env`

```bash
# Environment snapshot for reproducibility
# Generated: 2026-07-22
CUDA_VERSION=12.4
TORCH_VERSION=2.1.1
TRANSFORMERS_VERSION=4.40.0
TRL_VERSION=0.9.6
PEFT_VERSION=0.6.2
DATASETS_VERSION=2.18.0
BITSANDBYTES_VERSION=0.41.1
ACCELERATE_VERSION=0.27.2
```

Source this in startup.sh:

```bash
source /notebooks/.env
```

## Related

- [[03-Prerequisites]] — what's needed before training
    
- [[04-01-Environment-Setup]] — setup procedure
    
- [[07-04-Training-Crash]] — if dependencies cause crashes