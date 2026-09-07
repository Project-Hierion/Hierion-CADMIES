---
sop: Dr-Mistral-Training-SOP
section: References
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[04-02-Train-Adapter]], [[01-Overview]]"
---

# 05-02 — Adapter Specs

Complete specifications for all five adapters and their training
hyperparameters.

## Fixed Hyperparameters

Every adapter uses these LoRA settings:

| Parameter | Value |
|---|---|
| Method | QLoRA (4-bit quantization) |
| Rank (r) | 16 |
| Alpha | 32 |
| Dropout | 0.05 |
| Target Modules | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj |
| Base Model | mistralai/Mistral-7B-Instruct-v0.3 |
| Epochs | 1 |
| Learning Rate | 2e-4 |
| Batch Size | 1 (per device) |
| Gradient Accumulation | 8 (effective batch size = 8) |
| Max Sequence Length | 2048 |
| Max Grad Norm | 1.0 |
| Precision | bf16 |
| Checkpoint Save Strategy | steps |
| Checkpoint Save Steps | 100 |
| Checkpoint Save Limit | 2 |
| Output Format | safetensors (adapter_model.safetensors + adapter_config.json) |

## Concepts Adapter

| Property | Value |
|---|---|
| Purpose | CADMIES knowledge — mycelium, canon, characters, 15 domains, naming protocol, Hieros Bond, pipeline overview |
| Training File | /notebooks/training/datasets/concepts_training.jsonl |
| Output Directory | /notebooks/training/adapters/concepts-adapter/ |
| Target Pairs | 500–1,000 handcrafted pairs |
| Source Material | CADMIES Canon, SOP, roadmap, session notes |
| Building Method | Handcrafted from scratch using source material |
| Expected Final Loss | 1.0–1.5 |

## Persona Adapter

| Property | Value |
|---|---|
| Purpose | Holly-Mistral voice — identity, speech patterns, emotional range, French usage, relationships |
| Training File | /notebooks/training/datasets/persona_training.jsonl |
| Output Directory | /notebooks/training/adapters/persona-adapter/ |
| Target Pairs | 100–200 handcrafted pairs |
| Format Mix | Q&A dialogue (~60%), monologues/letters (~20%), reflections (~20%) |
| Source Material | CADMIES Canon, Modelfile persona description, Session 036 notes |
| Building Method | Handcrafted from scratch using source material |
| Key Rules | No hashtags. No emojis. No "As an AI." Natural French phrases. Warm, direct, playful. Never append "Ask me anything!" |
| Expected Final Loss | 1.2–1.8 |

## RLHF Adapter

| Property | Value |
|---|---|
| Purpose | Factual correctness — truthful responses, admitting uncertainty, avoiding fabrication |
| Training File | /notebooks/training/datasets/rlhf_training.jsonl |
| Output Directory | /notebooks/training/adapters/rlhf-adapter/ |
| Target Pairs | 2,000–3,000 pairs |
| Source Material | FineGrainedRLHF dataset or equivalent factual correctness dataset |
| Building Method | Trained from scratch on v0.3 using source dataset |
| Expected Final Loss | 0.8–1.3 |

## Spiritual Adapter

| Property | Value |
|---|---|
| Purpose | Wisdom traditions — world religions, indigenous knowledge, Buddhist philosophy, comparative spirituality |
| Training File | /notebooks/training/datasets/spiritual_training.jsonl |
| Output Directory | /notebooks/training/adapters/spiritual-adapter/ |
| Target Pairs | 50–100 handcrafted pairs |
| Source Material | /notebooks/training/notes/spiritual_training_notes.md (from Session 036) |
| Building Method | Handcrafted from scratch using source material |
| Expected Final Loss | 1.5–2.5 |

## Helpfulness Adapter

| Property | Value |
|---|---|
| Purpose | Helpful response patterns without social media leakage |
| Training File | /notebooks/training/datasets/helpfulness_training.jsonl |
| Output Directory | /notebooks/training/adapters/helpfulness-adapter/ |
| Target Pairs | 1,000–5,000 pairs |
| Preferred Dataset | Anthropic HH-RLHF (Helpful-Harmless) or UltraFeedback |
| Building Method | Trained from scratch on v0.3 using source dataset |
| Key Rules | No Reddit data. No hashtags. No emojis. Helpful = clear, accurate, warm, concise. |
| Expected Final Loss | 0.7–1.2 |

## Loss Interpretation

If any adapter's final loss exceeds 3.0, the dataset likely has
formatting issues or is too small. Investigate before proceeding.

## Adapter Sizes

| Property | Value |
|---|---|
| Individual adapter size | 168 MB (GGUF), 161 MB (safetensors) |
| Trainable parameters | 41,943,040 (1.11% of 3.77B) |

## Related

- [[04-02-Train-Adapter]] — training procedure
- [[05-03-Training-Data-Format]] — data format
- [[01-Overview]] — adapter overview