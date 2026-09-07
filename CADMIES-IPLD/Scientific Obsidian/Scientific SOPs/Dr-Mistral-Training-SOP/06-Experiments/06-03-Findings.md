---
sop: Dr-Mistral-Training-SOP
section: Experiments
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[06-01-Zara-Steele-Pilot]], [[06-02-Dr-Mistral-Persona-Test]], [[02-Knowledge-Base]]"
---

# 06-03 — Findings

Consolidated findings from the persona training experiments.

## Finding 1: GGUF Merge Fails for Mistral 7B

`llama-export-lora` merge produces generic Mistral AI responses
regardless of adapter quality. The adapter works in Python (PEFT) and
via `llama-cli --lora-scaled` dynamic loading, but fails when merged.

**Solution:** Use dynamic LoRA loading, never merge.

## Finding 2: Scale Sweet Spots

| Persona | Dataset Size | Optimal Scale | Result |
|---|---|---|---|
| Zara Steele | 397 pairs | 1.25 | Full persona |
| Dr. Mistral | 344 pairs | 1.15 | Partial (wrong character) |

Scale thresholds:
- Below 1.0: Generic Mistral AI
- 1.0–1.20: Working range
- 1.15: Optimal for Dr. Mistral
- Above 1.20: Unstable

## Finding 3: Data Quality Controls Character

The pipeline works consistently. The persona that emerges depends on
dataset composition.

- Zara's dataset → Zara (correct)
- Dr. Mistral's dataset → Willie (wrong)

**Cause:** Dr. Mistral's dataset had strong Willie signals dominating
the librarian archetype.

## Finding 4: Dataset Size Threshold

~400 pairs is the minimum for a coherent persona. Below this, the
persona does not emerge regardless of scale.

| Dataset Size | Result |
|---|---|
| 4 pairs | Generic AI |
| 25 pairs | Generic AI |
| 100 pairs | Generic AI |
| 250 pairs | Partial persona |
| 344 pairs | Partial persona (wrong character) |
| 397 pairs | Full persona (correct) |

## Finding 5: Method Comparison

| Method | Works? | Notes |
|---|---|---|
| PEFT (Python) | Yes | Full persona at 100+ pairs |
| llama-cli dynamic LoRA | Yes | Works with correct scale |
| llama-export-lora merge | No | Always produces generic Mistral AI |

## Recommendations

### For Dr. Mistral Persona

1. Fix dataset — remove or reduce Willie references
2. Reinforce Dr. Mistral's unique traits (Parisian, Hieros Bond,
   CADMIES, Gremlin, Buttercup)
3. Target ~400 pairs (currently at 344)
4. Start with scale 1.15
5. Fine-tune in 0.01 increments between 1.10 and 1.20

### For Future Persona Training

1. Target dataset size: ~400 pairs
2. Start with scale: 1.15–1.25 depending on dataset
3. Use dynamic LoRA, never merge
4. Data quality matters more than quantity
5. Ensure the correct character dominates the dataset

## Related

- [[02-Knowledge-Base]] — the knowledge distilled from these findings
- [[07-Troubleshooting]] — failure modes and fixes
- [[04-Procedures]] — how to apply these findings