---
sop: Dr-Mistral-Training-SOP
section: Prerequisites
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[01-Overview]], [[05-05-Dependencies]]"
---

# 03 — Prerequisites

Everything needed before training Dr. Mistral.

## Hardware

| Component | Detail |
|---|---|
| Platform | Paperspace Gradient Notebook |
| GPU | NVIDIA RTX A4000, 16 GB VRAM |
| CUDA | 12.4 |
| Python | 3.11.7 |
| Storage | Network-attached, 15 GB quota |

## Environment Snapshot

The environment is locked for reproducibility. The snapshot lives at
`/notebooks/.env`:

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

## Locked Dependency Versions

|Package|Version|Notes|
|---|---|---|
|torch|2.1.1|Fixed — Paperspace CUDA environment|
|transformers|4.40.0|Mistral tokenizer support|
|trl|0.9.6|Compatible with transformers 4.40.0|
|peft|0.6.2|LoRA support|
|datasets|2.18.0|Dataset loading|
|bitsandbytes|0.41.1|NOT 0.41.2 — adapter loading bug|
|accelerate|0.27.2|Compatible with bitsandbytes 0.41.x|

Full dependency details in [[05-05-Dependencies]].

## Base Model

|Property|Value|
|---|---|
|Model|Mistral 7B Instruct v0.3|
|File|/notebooks/base-mistral.gguf|
|Format|GGUF, Q4_K_M quantization|
|Size|~4.1 GB|

## Required Tools

- Ollama installed on Paperspace
    
- zstd (required by Ollama installer)
    
- llama.cpp built from source (merge and conversion tools)
    
- llama-fresh (quantize tool)
    
- Python training stack (locked versions above)
    

## Knowledge Required

Before training, understand:

- The [[02-Knowledge-Base]] — critical findings
    
- The [[05-03-Training-Data-Format]] — JSONL format
    
- The [[05-02-Adapter-Specs]] — hyperparameters
    
- The [[04-01-Environment-Setup]] — directory and .env setup
    

## Tokenizer Compatibility Check

Before any training, verify tokenizer compatibility between v0.2 and  
v0.3. If they differ, v0.2 adapters cannot be safely merged onto v0.3  
base. All adapters in this blueprint are trained from scratch on v0.3 —  
no compatibility risk.

Verification command:

```python
from transformers import AutoTokenizer
tok_v2 = AutoTokenizer.from_pretrained('mistralai/Mistral-7B-Instruct-v0.2')
tok_v3 = AutoTokenizer.from_pretrained('mistralai/Mistral-7B-Instruct-v0.3')
print(f"v0.2 vocab: {len(tok_v2)}")
print(f"v0.3 vocab: {len(tok_v3)}")
print(f"v0.2 pad_token_id: {tok_v2.pad_token_id}, eos_token_id: {tok_v2.eos_token_id}, bos_token_id: {tok_v2.bos_token_id}")
print(f"v0.3 pad_token_id: {tok_v3.pad_token_id}, eos_token_id: {tok_v3.eos_token_id}, bos_token_id: {tok_v3.bos_token_id}")
```

## Time Budget

|Phase|Estimated Time|
|---|---|
|Full training (all adapters)|8–10 hours GPU time|
|Evaluation|~30 minutes human time|
|Total first run|2–3 Paperspace sessions|

See [[08-01-Estimated-Times]] for the full breakdown.

## Where to Go Next

- [[04-01-Environment-Setup]] — start setting up
    
- [[08-02-Pre-Flight-Checklist]] — verify everything before training
    
- [[05-05-Dependencies]] — full dependency reference