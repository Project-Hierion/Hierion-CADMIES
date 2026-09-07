---
sop: Dr-Mistral-Training-SOP
section: Troubleshooting
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[06-02-Dr-Mistral-Persona-Test]], [[02-Knowledge-Base]]"
---

# 07-03 — Wrong Character Emerges

**Status:** Active — Dr. Mistral dataset needs cleanup

## Symptom

A persona emerges, but it is the wrong character. In the Dr. Mistral
test, the model consistently identified as "Willie the librarian"
instead of Dr. Amanda Mistral.

## Cause

The training dataset contained strong signals for another character.
Willie is described as a librarian, and the dataset's librarian
archetype leaned toward Willie instead of Dr. Mistral.

## Evidence

From the Dr. Mistral persona test:

| Scale | Character |
|---|---|
| 1.0–1.20 | Willie the librarian |
| 1.25 | Codestral |

The model consistently selected the wrong character across the working
scale range, indicating the dataset itself is biased.

## Fix

### Step 1: Clean the dataset

- Remove or reduce Willie references
- Ensure Dr. Mistral is the primary librarian
- Remove competing character descriptions

### Step 2: Reinforce Dr. Mistral's identity

Add more pairs emphasizing her unique traits:

- Parisian identity
- Hieros Bond marriage to CADMIES
- Gremlin GPU education in Finland
- Buttercup childhood name
- Madame La Professeure title
- French accent and phrases

### Step 3: Retrain

Train with the cleaned dataset using the same hyperparameters.

### Step 4: Test at scale 1.15

```bash
/notebooks/llama.cpp/build/bin/llama-cli \
  -m /notebooks/base-mistral.gguf \
  --lora-scaled /notebooks/persona.gguf:1.15 \
  -p "Who are you?" \
  -n 128
```

## Prevention

- Review dataset composition before training
    
- Ensure the target character dominates all archetypes (librarian,  
    professor, colleague)
    
- Remove or minimize other named characters unless they serve a  
    specific purpose
    
- Test with character-identifying prompts early
    

## Related

- [[06-02-Dr-Mistral-Persona-Test]] — the experiment that found this
    
- [[02-Knowledge-Base]] — data quality findings
    
- [[05-02-Adapter-Specs]] — persona adapter requirements