---
sop: Dr-Mistral-Training-SOP
section: Experiments
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[02-Knowledge-Base]], [[06-03-Findings]]"
---

# 06-01 — Zara Steele Pilot

The pilot experiment that established the persona training
methodology for Mistral 7B Instruct v0.3.

## Overview

Captain Zara Steele was the test case for the end-to-end persona
training pipeline. The experiment tested dataset size and LoRA scale
to find what makes a persona emerge.

## Environment

| Component | Detail |
|---|---|
| Hardware | Paperspace Gradient Notebook, A4000 GPU (16 GB VRAM) |
| Base Model | Mistral 7B Instruct v0.3 |
| Method | QLoRA with LoRA rank 16, alpha 32 |
| Epochs | 1 |
| Learning Rate | 2e-4 |

## Test Results

| Dataset Size | Scale | Outcome |
|---|---|---|
| 4 pairs | 0.3, 1.0, 2.0 | Generic Mistral AI |
| 25 pairs | 0.3, 0.5, 1.0 | Generic Mistral AI |
| 100 pairs | 0.3, 1.0 | Generic Mistral AI |
| 250 pairs | 1.0 | Partial persona (Belt, Ceres, tough talk) |
| 397 pairs | 0.05 | Generic Mistral AI |
| 397 pairs | 0.3 | Generic Mistral AI |
| 397 pairs | 0.75 | Generic Mistral AI |
| 397 pairs | 1.0 | Partial persona (space, Jupiter mention, but weak) |
| **397 pairs** | **1.25** | **Full persona (Stardust Runner, pilot, smuggler, Belt, code)** |

## Key Finding

**~400 pairs at scale 1.25** is the sweet spot for persona training on
Mistral 7B Instruct v0.3 using dynamic LoRA.

## Pattern Observed

- **Scale sensitivity:** Persona appears at higher scales only after
  enough data
- **Data threshold:** ~400 pairs seems to be the minimum for a coherent
  persona
- **Scale threshold:** 1.25 worked; lower scales failed to activate the
  persona

## Critical Debugging Insights

### GGUF Merge Does Not Work for Mistral

- `llama-export-lora` merge produces generic Mistral AI responses
  regardless of adapter quality
- Adapter works in Python (PEFT) but fails in GGUF merge
- **Solution:** Use `llama-cli --lora-scaled` dynamic loading instead
  of merging

### Method Comparison

| Method | Works? | Notes |
|---|---|---|
| PEFT (Python) | Yes | Full persona at 100 pairs |
| llama-cli dynamic LoRA | Yes | Works with correct scale |
| llama-export-lora merge | No | Produces generic Mistral AI |

## Files Created

### Training Data

- test_persona_training.jsonl (4 pairs)
- test_persona_25.jsonl (25 pairs)
- test_persona_100.jsonl (100 pairs)
- test_persona_250.jsonl (250 pairs)
- test_persona_500.jsonl (397 pairs)

### Adapters

- test-persona-adapter/ (safetensors)
- test-persona.gguf (100-pair adapter)
- test-persona-250.gguf (250-pair adapter)
- test-persona-500.gguf (397-pair adapter)

## Date

2026-07-23

## Related

- [[06-02-Dr-Mistral-Persona-Test]] — the follow-up experiment
- [[06-03-Findings]] — consolidated findings
- [[02-Knowledge-Base]] — what we learned