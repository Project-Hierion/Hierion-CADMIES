---
sop: Dr-Mistral-Training-SOP
section: Overview
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[02-Knowledge-Base]]"
---

# 01 — Overview

## Training Philosophy

Dr. Amanda Mistral is trained using a **lite by design** approach.

- **Personality and core knowledge** live in LoRA adapter weights
- **Factual domain knowledge** lives in external agent systems
- **Training is minimal, precise, and reproducible**

### Key Principle

All adapters are trained from scratch on Mistral 7B Instruct v0.3.
No existing adapters are reused. No v0.2 training data is reused.

This ensures a clean foundation. The v0.2 work taught us what works —
the v0.3 work applies those lessons to a fresh base model.

## Why Mistral 7B Instruct v0.3

| Property | Value |
|---|---|
| Model | Mistral 7B Instruct v0.3 |
| Hugging Face ID | mistralai/Mistral-7B-Instruct-v0.3 |
| Format | GGUF, Q4_K_M quantization |
| Chat Template | [INST] / [/INST] |
| Context Length | 4,096 tokens (runtime) |

**Why v0.3 over v0.2:**

- Already instruction-tuned — can follow directions without additional training
- Less ingrained refusal behavior — personality training is easier
- Instruction-tuning can be skipped entirely

## The Five Adapters

Dr. Mistral's capabilities come from five LoRA adapters:

| Adapter | Purpose | Target Pairs |
|---|---|---|
| concepts | CADMIES knowledge — mycelium, canon, characters, 15 domains | 500–1,000 |
| persona | Holly-Mistral voice — identity, speech, emotion, French | 100–200 |
| rlhf | Factual correctness — truthful, admits uncertainty | 2,000–3,000 |
| spiritual | Wisdom traditions — religions, philosophy, indigenous | 50–100 |
| helpfulness | Helpful responses without social media leakage | 1,000–5,000 |

Each adapter is trained independently, validated solo, then combined.

## The Critical Finding

The experimental work revealed something crucial: **GGUF merging does
not work for Mistral 7B v0.3.** The `llama-export-lora` merge produces
generic responses regardless of adapter quality.

The working method is **dynamic LoRA loading** via `llama-cli
--lora-scaled` at a scale sweet spot of **1.15** for Dr. Mistral.

This finding changed everything. See [[02-Knowledge-Base]] for the full
story and [[07-01-GGUF-Merge-Fails]] for the technical details.

## Training Order

Adapters are trained in this sequence:

```text
concepts → rlhf → spiritual → persona → helpfulness
```

Knowledge first, voice later, behavior last.

## Workflow Summary

### Phase 1: Setup
Environment, base model, directory structure, tokenizer verification,
baseline evaluation.

### Phase 2: Train Adapters
One at a time. Each adapter: build pairs → validate → dry run → full
training → log → convert → solo validate.

### Phase 3: Deploy
Dynamic LoRA loading (not merge). Modelfile configuration. Ollama model
creation.

### Phase 4: Evaluate
Sanity check, persona coherence, canonical accuracy, safety, leakage.

### Phase 5: Iterate
If scores miss targets, adjust scales, retrain, re-evaluate.

## Where to Go Next

- [[02-Knowledge-Base]] — the critical findings
- [[03-Prerequisites]] — what you need before training
- [[04-01-Environment-Setup]] — start the setup procedure