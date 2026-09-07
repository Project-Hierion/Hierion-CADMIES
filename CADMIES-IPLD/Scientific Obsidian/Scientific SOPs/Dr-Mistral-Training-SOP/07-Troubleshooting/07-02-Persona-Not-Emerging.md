---
sop: Dr-Mistral-Training-SOP
section: Troubleshooting
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[02-Knowledge-Base]], [[07-01-GGUF-Merge-Fails]]"
---

# 07-02 — Persona Not Emerging

**Status:** Active troubleshooting entry

## Symptom

The model responds like generic Mistral AI. No persona emerges,
regardless of the prompt.

## Possible Causes

1. Scale too low — below the emergence threshold
2. Dataset too small — below ~400 pairs
3. Using merge instead of dynamic LoRA
4. Wrong adapter file being loaded

## Diagnostic Steps

### Step 1: Check the method

Are you using dynamic LoRA or merge? If merge, see
[[07-01-GGUF-Merge-Fails]]. Merge always produces generic responses.

### Step 2: Check the scale

Scale below 1.0 produces generic responses. Test at 1.15:

```bash
/notebooks/llama.cpp/build/bin/llama-cli \
  -m /notebooks/base-mistral.gguf \
  --lora-scaled /notebooks/persona.gguf:1.15 \
  -p "Who are you?" \
  -n 128
```

### Step 3: Check the dataset size

Persona emergence requires ~400 pairs. Below 250 pairs, the persona  
will not emerge regardless of scale.

### Step 4: Verify the adapter works in Python

Test the adapter via PEFT to confirm it is valid:

```python
from peft import PeftModel
# Load adapter and test directly
```

If the adapter works in Python but not via llama-cli, the issue is the  
GGUF conversion.

## Fixes

- Scale too low → increase to 1.15, test in 0.01 increments
    
- Dataset too small → add more pairs, target ~400
    
- Using merge → switch to dynamic LoRA
    
- Wrong adapter file → verify the file path and name
    

## Scale Reference

|Scale|Result|
|---|---|
|Below 1.0|Generic Mistral AI|
|1.0–1.20|Working range|
|1.15|Optimal for Dr. Mistral|
|Above 1.20|Unstable|

## Related

- [[02-Knowledge-Base]] — scale findings
    
- [[07-01-GGUF-Merge-Fails]] — merge failure
    
- [[04-03-Validate-and-Convert]] — solo validation