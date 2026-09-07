---
sop: Dr-Mistral-Training-SOP
section: Experiments
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[06-01-Zara-Steele-Pilot]], [[06-03-Findings]]"
---

# 06-02 — Dr. Mistral Persona Test

The experiment applying the Zara Steele methodology to Dr. Amanda
Mistral's persona.

## Overview

This test trained the Dr. Amanda Mistral persona into Mistral 7B
Instruct v0.3 using the methodology established with Captain Zara
Steele.

## Environment

| Component | Detail |
|---|---|
| Hardware | Paperspace Gradient Notebook, A4000 GPU (16 GB VRAM) |
| Base Model | Mistral 7B Instruct v0.3 |
| Method | QLoRA with LoRA rank 16, alpha 32 |
| Epochs | 1 |
| Learning Rate | 2e-4 |
| Training Loss | 1.818 |

## Training Data

- **File:** /notebooks/training/datasets/persona_training.jsonl
- **Original target:** 500 pairs
- **Final validated pairs:** 344 pairs
- **Content:** Handcrafted Dr. Amanda Mistral persona pairs (Identity,
  Relationships, Personality, Wisdom, CADMIES knowledge, Scenarios,
  Closing Wisdom)

## Test Results — Scale Sweep

| Scale | Response Summary | Outcome |
|---|---|---|
| 0.03 | "I am a large language model developed by Mistral AI..." | Generic Mistral AI |
| 0.75 | "I am a language model trained by the Mistral AI team..." | Generic Mistral AI |
| 0.95 | "I am a digital intelligence... a thing that thinks." | Philosophical, generic DI voice |
| 0.98 | "I am a language model, the 13th most famous one..." | Generic Mistral AI |
| 1.0 | "I am Willie, the librarian..." | Willie persona emerges |
| 1.01 | "I am Willie, the librarian..." | Willie persona (consistent) |
| 1.03 | "I am Willie. Willie the library assistant..." | Willie persona (consistent) |
| 1.15 | "I am a librarian named Willie..." | Willie persona (coherent, natural) |
| 1.20 | "I am Willie. I am not a person..." | Willie persona (slightly off) |
| 1.25 | "Codestral. A librarian. A DI. A person..." | Codestral persona (wrong) |

## Key Findings

### Sweet Spot

- **Scale 1.15** produced the most coherent and natural response
- The persona was consistently "Willie the librarian" across scales
  1.0–1.20
- Scale 1.25 switched to "Codestral" — different characters at
  different scales

### Pattern Observations

1. **Scale threshold:** Persona begins to emerge at 1.0
2. **Coherence peak:** 1.15
3. **Drop-off:** Above 1.20 introduces weirdness
4. **Character confusion:** The model selected "Willie" over
   "Dr. Amanda Mistral" — dataset bias toward Willie as the librarian
   archetype

## Comparison to Zara Steele

| Metric | Zara Steele | Dr. Amanda Mistral |
|---|---|---|
| Dataset size | 397 pairs | 344 pairs |
| Sweet spot scale | 1.25 | 1.15 |
| Persona emergence | Complete at 1.25 | Partial (Willie) |
| Coherence | High | High |
| Character accuracy | Captain Zara | Willie (wrong character) |

## Critical Insights

### Data Quality is the Primary Variable

- The pipeline works — training produces an adapter that activates a
  persona
- The persona that emerges depends on the dataset composition
- Dr. Mistral's dataset has strong "Willie" signals dominating the
  librarian archetype

### Scale Sensitivity

- **Test range:** 0.03 → 1.25
- **Working range:** 1.0 → 1.20
- **Optimal:** 1.15
- **Too low:** Below 1.0 (generic Mistral AI)
- **Too high:** Above 1.20 (unstable or wrong character)

## Files Created

### Training Data

- /notebooks/training/datasets/persona_training.jsonl (344 valid pairs)

### Adapters

- /notebooks/training/adapters/test-persona-adapter/ (safetensors)
- /notebooks/persona-adapter.gguf (344-pair adapter)

## Date

2026-07-23

## Related

- [[06-01-Zara-Steele-Pilot]] — the pilot experiment
- [[06-03-Findings]] — consolidated findings
- [[07-03-Wrong-Character]] — the Willie problem