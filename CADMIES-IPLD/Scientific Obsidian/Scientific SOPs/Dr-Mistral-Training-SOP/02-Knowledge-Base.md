---
sop: Dr-Mistral-Training-SOP
section: Knowledge Base
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[01-Overview]], [[06-Experiments]]"
---

# 02 — Knowledge Base

The critical findings from experimental work. This is the knowledge
that makes the procedures valid. Read this before training anything.

## Finding 1: GGUF Merge Does Not Work for Mistral 7B

**The discovery:** `llama-export-lora` merge produces generic Mistral
AI responses regardless of adapter quality.

**The evidence:**

- Adapter works in Python via PEFT — confirms training is valid
- Adapter works via `llama-cli --lora-scaled` dynamic loading
- Adapter fails when merged into the base model via `llama-export-lora`

**The conclusion:** The issue is with the GGUF conversion/merge
pipeline, not the training data or adapter.

**The solution:** Use dynamic LoRA loading, not merging.

See [[07-01-GGUF-Merge-Fails]] for full technical details.

## Finding 2: Scale Sweet Spot for Persona Training

Persona emergence depends on both dataset size and LoRA scale. The
relationship is non-linear and specific to each persona.

### Zara Steele Pilot

| Dataset Size | Scale | Outcome |
|---|---|---|
| 4 pairs | 0.3, 1.0, 2.0 | Generic Mistral AI |
| 25 pairs | 0.3, 0.5, 1.0 | Generic Mistral AI |
| 100 pairs | 0.3, 1.0 | Generic Mistral AI |
| 250 pairs | 1.0 | Partial persona |
| 397 pairs | 0.05–0.75 | Generic Mistral AI |
| 397 pairs | 1.0 | Partial persona |
| **397 pairs** | **1.25** | **Full persona** |

**Sweet spot:** ~400 pairs at scale 1.25

### Dr. Mistral Persona

| Scale | Outcome |
|---|---|
| 0.03–0.98 | Generic Mistral AI |
| 1.0–1.20 | Willie persona (wrong character) |
| **1.15** | **Most coherent — but still Willie** |
| 1.25 | Codestral persona (wrong character) |

**Sweet spot:** 344 pairs at scale 1.15 — but character confusion
(Wille instead of Dr. Mistral) indicates dataset bias.

## Finding 3: Data Quality Controls Character Emergence

The training pipeline works. The persona that emerges depends on the
dataset composition.

- Zara's dataset produced Zara — correct character
- Dr. Mistral's dataset produced Willie — wrong character

**The cause:** Dr. Mistral's dataset had strong "Willie" signals that
dominated the librarian archetype.

**The fix:** Clean the dataset to emphasize Dr. Mistral's unique
traits. Reduce Willie references. Add more pairs reinforcing Parisian
identity, Hieros Bond, CADMIES, Gremlin, Buttercup.

See [[07-03-Wrong-Character]] for details.

## Finding 4: Scale Tuning Strategy

When the default scales fail, tune systematically:

1. Start with all adapters at 0.2 (neutral baseline)
2. If personality is weak: increase persona to 0.3–0.4
3. If CADMIES knowledge is weak: increase concepts to 0.3–0.35
4. If helpfulness is too strong: decrease to 0.05–0.08
5. If output is incoherent: decrease all scales by 0.05–0.1
6. Test each change with sanity check and evaluation
7. Log every attempted configuration to merge_log.csv

## Finding 5: Scale Thresholds

- **Below 1.0:** Generic Mistral AI — persona does not emerge
- **1.0–1.20:** Working range for persona emergence
- **Optimal:** 1.15 (Dr. Mistral), 1.25 (Zara)
- **Above 1.20:** Unstable — wrong character or incoherence

## The Bottom Line

1. Train adapters from scratch on v0.3
2. Use ~400 pairs for persona, more for knowledge adapters
3. Test with dynamic LoRA at scales 1.0–1.25
4. Never merge — dynamic loading only
5. Dataset quality matters more than quantity
6. If the wrong character emerges, fix the dataset, not the scale

## Related

- [[06-Experiments]] — the full test results
- [[07-Troubleshooting]] — failure modes and fixes
- [[04-Procedures]] — how to apply this knowledge