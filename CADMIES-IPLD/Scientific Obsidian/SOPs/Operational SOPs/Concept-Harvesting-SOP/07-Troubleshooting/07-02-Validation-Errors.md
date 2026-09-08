---
sop: Concept-Harvesting-SOP
section: Troubleshooting
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[04-03-Review-and-Mint]]"
---

# 07-02 — Validation Errors

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
maintained in the CADMIES repository. This troubleshooting entry
documents validation failure modes observed during active development.

## Symptom

The scientific validator rejects concepts before minting. Concepts
fail schema compliance.

## Possible Causes

1. Missing required fields
2. Invalid references in builds_upon
3. Empty difficulty levels
4. Malformed concept structure

## Diagnostic Steps

### Step 1: Check the validation output

The validator reports specific errors per concept. Each error
identifies the field or structure that failed.

### Step 2: Check difficulty levels

```bash
python3 -c "
import json
from pathlib import Path
source_dir = Path('source_concepts')
for jf in source_dir.glob('*.json'):
    with open(jf) as f:
        c = json.load(f)
    dl = c.get('difficulty_levels', {})
    for level in ['beginner', 'intermediate', 'expert']:
        if level not in dl or not dl[level]:
            print(f'{c[\"human_id\"]}: EMPTY {level}')
"
```

### Step 3: Check builds_upon references

The transform step filters invalid references to unminted concepts.
If builds_upon points to a concept that doesn't exist, the reference
must be corrected.

## Validation Levels

| Level | Description |
|---|---|
| BASIC | Minimal schema checks |
| STANDARD | Standard concept requirements |
| RIGOROUS | Strict scientific requirements |
| STRICT | Full compliance |

## Resolution
- Fix missing fields in the concept JSON
- Correct invalid references
- Fill empty difficulty levels
- Re-run validation before minting

## Related
- [[04-03-Review-and-Mint]] — the validation step
- [[07-01-Harvester-Fails]] — harvester failures
