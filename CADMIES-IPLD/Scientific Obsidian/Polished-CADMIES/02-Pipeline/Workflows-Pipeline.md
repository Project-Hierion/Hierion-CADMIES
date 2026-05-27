---
pipeline: CADMIES End-to-End Workflows
date: 2026-05-27
status: Living document
related: [[Phase-57-Harvester-Hardening]], [[Phase-58-Mega-Harvest]], [[Phase-56-Emergence-Verification]]
---
# CADMIES Pipeline Workflows
### Ground Zero: Capture the Conversation
Before anything else, save your conversation to **`tools/harvest/conversation.json`**.
This is the template for that file. This is a spore. Everything downstream flows from this file.
```json
{
  "metadata": {
    "_citation_guidance": "For scientific provenance and proper attribution, complete the fields below. They are optional but we highly advise they be filled in — omitted fields default to internal CADMIES system standards. All entries may be amended later as new source information becomes available.",
    "source_description": "YOUR TEXT HERE",
    "source_url": "YOUR TEXT HERE",
    "author": "YOUR TEXT HERE",
    "license": "YOUR TEXT HERE"
  },
  "content": "YOUR TEXT HERE"
}
```

---

## Workflow 1: Full Harvest Pipeline

The complete journey from source conversation to public mycelium map deployment.

text

┌─────────────────────────────────────────────────────────────────────┐
│                    FULL HARVEST PIPELINE                             │
│                                                                     │
│  conversation.json ──→ Harvester ──→ source_concepts/ ──→ Blockstore│
│         │                  │               │                  │     │
│         │                  │               │                  │     │
│    [Optional:          Mistral          Concepts            CIDs    │
│     metadata for       extracts         saved as            minted  │
│     external           concepts]        JSON files          to      │
│     sources]                                            blocks/     │
│                                                            │        │
│                                                            ▼        │
│                                                      Index updated  │
│                                                            │        │
│                                                            ▼        │
│                                                    Map regenerated  │
│                                                            │        │
│                                                            ▼        │
│                                              Relationships added    │
│                                                            │        │
│                                                            ▼        │
│                                                     CAR exported    │
│                                                            │        │
│                                                            ▼        │
│                                                  Public gateway     │
│                                                  (manual step)      │
│                                                            │        │
│                                                            ▼        │
│                                                   GitHub Pages      │
│                                               hieros-cadmies.io     │
└─────────────────────────────────────────────────────────────────────┘

### Commands

**Prepare source material**  
Edit `tools/harvest/conversation.json` with your text. Optional: fill in `metadata.source_*` fields.

**Run the full pipeline** (in the CADMIES notebook)

bash

python /notebooks/CADMIES/CADMIES-IPLD/tools/harvest/harvest_full_pipeline.py --auto --with-relationships

**Export backup**

bash

python /notebooks/CADMIES/CADMIES-IPLD/tools/export_to_car.py --all --output /notebooks/cadmies_latest.car

**Update public gateway** (manual map copy needed)

bash

python /notebooks/CADMIES/CADMIES-IPLD/tools/generate_public_gateway.py && cp /notebooks/CADMIES/CADMIES-IPLD/mycelium_map.html /notebooks/CADMIES/docs/

**Commit and deploy**

bash

cd /notebooks/CADMIES && git add docs/ && git commit -m "Update public gateway" && git push origin main

**Sync to local**

bash

cd /run/media/fedora/PNY/CADMIES/CADMIES-IPLD && source venv/bin/activate && git pull origin main

---

## Workflow 2: External Source Harvest

For published work (blogs, papers, articles) requiring citation.

text

┌────────────────────────────────────────────────────────────────────┐
│                 EXTERNAL SOURCE HARVEST                             │
│                                                                    │
│  conversation.json                  Harvester                      │
│  ┌─────────────────────┐           reads metadata                  │
│  │ metadata:           │                │                          │
│  │   source_desc: ...  │                ▼                          │
│  │   source_url: ...   │      Injects into proofs                  │
│  │   author: ...       │           │                               │
│  │   license: ...      │           ▼                               │
│  │ content:            │    concepts minted                        │
│  │   [article text]    │    with full attribution                  │
│  └─────────────────────┘           │                               │
│                                    ▼                               │
│                             proofs: [{                             │
│                               type: "conversation_extraction",      │
│                               description: "Extracted from...",     │
│                               reference: "https://...",             │
│                               author: "...",                        │
│                               license: "..."                        │
│                             }]                                     │
└────────────────────────────────────────────────────────────────────┘

### Example: Rebentisch Harvest

json

{
  "metadata": {
    "_citation_guidance": "For scientific provenance and proper attribution, complete the fields below. Optional — defaults to internal CADMIES standards. May be amended later.",
    "source_description": "Dr. Rupert Rebentisch's blog 'Mycelium of Knowledge' — article: 'When AI Becomes Your Zettelkasten's Co-Pilot'",
    "source_url": "https://www.mycelium-of-knowledge.org/when-ai-becomes-your-zettelkastens-co-pilot/",
    "author": "Dr. Rupert Rebentisch",
    "license": "MIT"
  },
  "content": "[Full article text here]"
}

---

## Workflow 3: CAR Import & Sync

Bringing the mycelium from Paperspace to local machines.

text

┌───────────────────────────────────────────────────────────────────┐
│                    CAR IMPORT PIPELINE                             │
│                                                                   │
│  Paperspace                              Local Machine            │
│  ┌──────────────────┐                   ┌──────────────────┐      │
│  │ Export CAR       │                   │ incoming_cars/   │      │
│  │ python tools/    │─── download ───→   │                  │      │
│  │ export_to_car.py │                   │ python tools/    │      │
│  │ --all            │                   │ import_from_car  │      │
│  └──────────────────┘                   │                  │      │
│                                         │ Blocks saved     │      │
│                                         │ Index updated    │      │
│                                         │ Provenance       │      │
│                                         │ preserved        │      │
│                                         │                  │      │
│                                         │ Map regenerated  │      │
│                                         │ python tools/    │      │
│                                         │ generate_        │      │
│                                         │ mycelium_map.py  │      │
│                                         └──────────────────┘      │
└───────────────────────────────────────────────────────────────────┘

### Commands

**On Paperspace: export**

bash

python tools/export_to_car.py --all --output /notebooks/cadmies_latest.car

Download `cadmies_latest.car` to local `incoming_cars/`.

**On local: import**

bash

cd /run/media/fedora/PNY/CADMIES/CADMIES-IPLD && source venv/bin/activate
python tools/import_from_car.py incoming_cars/cadmies_latest.car
python tools/generate_mycelium_map.py

---

## Workflow 4: Quality Control & Maintenance

text

┌────────────────────────────────────────────────────────────────┐
│                   MAINTENANCE WORKFLOW                          │
│                                                                │
│  ┌─────────────────┐                                           │
│  │ Remint stale     │  python tools/remint_existing_concepts   │
│  │ concepts         │  --apply                                 │
│  └────────┬────────┘                                           │
│           │                                                    │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │ Regenerate map   │  python tools/generate_mycelium_map.py   │
│  └────────┬────────┘                                           │
│           │                                                    │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │ Check for        │  Look for "NOTE: Unmapped domain"        │
│  │ unmapped domains │  Add to DOMAIN_UPWARD_MAP if needed      │
│  └────────┬────────┘                                           │
│           │                                                    │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │ Audit concepts   │  python -c "scan source_concepts"        │
│  │ for issues       │  Check difficulty levels, relationships  │
│  └────────┬────────┘                                           │
│           │                                                    │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │ Export CAR       │  python tools/export_to_car.py --all     │
│  │ for backup       │                                          │
│  └─────────────────┘                                           │
└────────────────────────────────────────────────────────────────┘

### Commands

**Remint any stale CIDs**

bash

python tools/remint_existing_concepts.py --apply

**Regenerate map and check domains**

bash

python tools/generate_mycelium_map.py

**Audit source concepts**

bash

python3 -c "
import json; from pathlib import Path
source_dir = Path('source_concepts')
for jf in source_dir.glob('*.json'):
    with open(jf) as f: c = json.load(f)
    dl = c.get('difficulty_levels', {})
    for level in ['beginner', 'intermediate', 'expert']:
        if level not in dl or not dl[level]:
            print(f'{c[\"human_id\"]}: EMPTY {level}')
"

**Export backup**

bash

python tools/export_to_car.py --all --output /notebooks/cadmies_latest.car

---

## Workflow 5: Session Sync

End-of-session synchronization across all nodes.

text

┌───────────────────────────────────────────────────────────────────┐
│                      SESSION SYNC                                  │
│                                                                   │
│  Paperspace ──→ git push ──→ GitHub ──→ git pull ──→ PNY          │
│      │                            │                    │          │
│      │                            │                    │          │
│  Commit all                   Central                 Local       │
│  changes:                     repository             machine      │
│  - source_concepts                                               │
│  - map                                                           │
│  - index                                                         │
│  - scripts                                                       │
│  - CAR export                                                    │
│                                                                  │
│  PNY ──→ SanDisk (daily driver, manual copy or git pull)          │
└───────────────────────────────────────────────────────────────────┘

### Commands

**On Paperspace**

bash

cd /notebooks/CADMIES/CADMIES-IPLD
git add -A
git commit -m "Session XXX: description of changes"
git push origin main

**On PNY**

bash

cd /run/media/fedora/PNY/CADMIES/CADMIES-IPLD && source venv/bin/activate
git pull origin main