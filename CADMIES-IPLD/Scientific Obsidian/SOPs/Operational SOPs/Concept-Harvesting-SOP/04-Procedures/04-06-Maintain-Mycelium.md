---
sop: Concept-Harvesting-SOP
section: Procedures
date: 2026-09-07
status: ACTIVE
related: "[[SOP Landing]], [[07-03-Orphan-Edges]], [[05-02-Workflow-Commands]]"
---

# 04-06 — Maintain Mycelium

## Compilation Note

This SOP was compiled on 2026-09-07 from the pipeline documentation
and script inventory maintained in the CADMIES repository. The
procedure documented here reflects the pipeline as of the August 2026
script audit.

## When to Use

- After relationship generation
- Periodically to verify system health
- When unmapped domains appear
- When concepts need enrichment

## Procedure

### Step 1: Remint stale concepts

```bash
python tools/remint_existing_concepts.py --apply
```

Remints concepts whose block content changed since original minting.

### Step 2: Regenerate map and check domains

```bash
python tools/generate_mycelium_map.py
```

Look for "NOTE: Unmapped domain" in the output. Add missing mappings
to DOMAIN_UPWARD_MAP if needed.

### Step 3: Audit source concepts

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

Checks for empty difficulty level entries.

### Step 4: Run scientific audit

```bash
python audits/scientific_audit.py
```

Four-part audit: structure, metadata, functionality, standards.

### Step 5: Strip orphan edges

```bash
python tools/strip_all_orphans.py --apply
```

Strips edges pointing to non-existent targets. See
[[07-03-Orphan-Edges]].

### Step 6: Enrich concepts

```bash
python tools/enrich_concepts.py
```

Fills gaps in existing concepts via LLM. For a single concept:

```bash
python tools/enrich_concepts.py --concept=entropy
```

Dry run preview:

```bash
python tools/enrich_concepts.py --dry-run
```

### Step 7: Export backup

```bash
python tools/export_to_car.py --all --output cadmies_latest.car
```

## Maintenance Checklist

| Task | Command | Frequency |
|---|---|---|
| Remint stale | remint_existing_concepts.py --apply | After relationship changes |
| Check domains | generate_mycelium_map.py | After each harvest |
| Audit concepts | scientific_audit.py | Periodically |
| Strip orphans | strip_all_orphans.py --apply | After relationship generation |
| Enrich concepts | enrich_concepts.py | When gaps detected |
| Export backup | export_to_car.py --all | After each session |

## Related
- [[07-03-Orphan-Edges]] — orphan edge troubleshooting
- [[05-02-Workflow-Commands]] — full workflow reference
- [[05-04-Script-Inventory]] — maintenance script details
