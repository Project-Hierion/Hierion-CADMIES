---
sop: Concept-Harvesting-SOP
section: Troubleshooting
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[04-02-Run-Harvester]]"
---

# 07-01 — Harvester Fails

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
maintained in the CADMIES repository. This troubleshooting entry
documents failure modes observed during active development.

## Symptom

The harvester fails to run — script errors, no concepts extracted, or
Mistral returns empty responses.

## Possible Causes

1. Ollama not running
2. Model not pulled
3. Conversation JSON malformed
4. Wrong working directory
5. Python environment not activated

## Diagnostic Steps

### Step 1: Check Ollama is running

```bash
pgrep -x ollama
```

### Step 2: Check the model is available

```bash
ollama list | grep mistral
```

If missing:

```bash
ollama pull mistral:7b
```

### Step 3: Validate the conversation JSON

```bash
python3 -c "import json; json.load(open('tools/harvest/conversation.json'))"
```

### Step 4: Verify working directory

Run from the repo root:

```bash
cd /notebooks/CADMIES/CADMIES-IPLD
```

### Step 5: Check the error output

Run the harvester and capture errors:

```bash
python tools/harvest/harvest_full_pipeline.py --auto 2>&1 | head -50
```

## Manual Import Fallback

When no LLM is available, the harvester switches to manual minting
mode. Concepts in source_concepts/ can be reviewed and minted
without an LLM.

## Related
- [[04-02-Run-Harvester]] — the run procedure
- [[07-02-Validation-Errors]] — validation failures
