---
sop: Dr-Mistral-Training-SOP
section: Troubleshooting
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[02-Knowledge-Base]], [[04-04-Deploy-Model]]"
---

# 07-01 — GGUF Merge Fails

**Status:** Critical — this failure mode changed the entire deployment
approach

## Symptom

After merging adapters with `llama-export-lora`, the model responds
like generic Mistral AI. The persona and knowledge are gone, regardless
of how well the adapters performed in solo testing.

## Cause

The `llama-export-lora` merge pipeline does not work correctly for
Mistral 7B. The merge produces a model that has lost the adapter
influence, even though the adapters themselves are valid.

## Evidence

From both the Zara Steele and Dr. Mistral experiments:

| Method | Result |
|---|---|
| PEFT (Python) | Full persona at 100+ pairs — adapter works |
| llama-cli dynamic LoRA | Works with correct scale |
| llama-export-lora merge | Generic Mistral AI — merge fails |

The adapter is confirmed valid via PEFT and dynamic loading. The
problem is specifically the GGUF conversion/merge pipeline.

## Fix

Use dynamic LoRA loading instead of merging:

```bash
/notebooks/llama.cpp/build/bin/llama-cli \
  -m /notebooks/base-mistral.gguf \
  --lora-scaled /notebooks/persona.gguf:1.15 \
  -p "Who are you?" \
  -n 128
```


For the full deployment procedure, see [[04-04-Deploy-Model]].

## What NOT to Do

**Do not use:**
```text
/notebooks/llama.cpp/build/bin/llama-export-lora \
  -m /notebooks/base-mistral.gguf \
  -o /notebooks/merged.gguf \
  --lora-scaled /notebooks/persona.gguf:1.15
```

This produces the generic model. The merge approach is deprecated for  
Mistral 7B.

## Related

- [[02-Knowledge-Base]] — the finding that changed everything
    
- [[04-04-Deploy-Model]] — correct deployment procedure
    
- [[06-03-Findings]] — experimental evidence