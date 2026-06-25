---
pipeline: CADMIES End-to-End Workflows
date: 2026-06-25
status: Living document
related: [[Phase-66]], [[Phase-63]], [[Phase-64]], [[Phase-65]], [[Session-031]], [[Session-032]]
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


Workflow 1: Full Harvest Pipeline
The complete journey from source conversation to public mycelium map deployment.

text

┌─────────────────────────────────────────────────────────────────────┐
│ FULL HARVEST PIPELINE │
│ │
│ conversation.json ──→ Harvester ──→ source_concepts/ ──→ Blockstore│
│ │ │ │ │ │
│ │ │ │ │ │
│ [Optional: Mistral Concepts CIDs │
│ metadata for extracts saved as minted │
│ external concepts] JSON files to │
│ sources] blocks/ │
│ │ │
│ ▼ │
│ Index updated │
│ │ │
│ ▼ │
│ Map regenerated │
│ (v3.0.0 fractal) │
│ │ │
│ ▼ │
│ Relationships added │
│ │ │
│ ▼ │
│ CAR exported │
│ │ │
│ ▼ │
│ Public gateway │
│ (auto-deploys) │
│ │ │
│ ▼ │
│ project-hierion. │
│ duckdns.org │
└─────────────────────────────────────────────────────────────────────┘

Commands
Prepare source material
Edit tools/harvest/conversation.json with your text. Optional: fill in metadata.source_* fields.

Run the full pipeline (on cloud GPU instance)
```
python tools/harvest/harvest_full_pipeline.py --auto --with-relationships
```

Regenerate map (now v3.0.0 — fractal succulent layout, produces concepts_ranked.json alongside mycelium_map.html)
```
python tools/generate_mycelium_map.py
```

Export backup
```
python tools/export_to_car.py --all --output cadmies_latest.car
```

Commit and push to GitHub (cloud compute instance auto-pulls and deploys within 5 minutes)
```
git add -A && git commit -m "Harvest: description of changes" && git push origin main
```

Sync to local
```
cd /run/media/fedora/PNY/CADMIES/CADMIES-IPLD && source venv/bin/activate && git pull origin main
```

Workflow 2: External Source Harvest
For published work (blogs, papers, articles) requiring citation.

text

┌────────────────────────────────────────────────────────────────────┐
│ EXTERNAL SOURCE HARVEST │
│ │
│ conversation.json Harvester │
│ ┌─────────────────────┐ reads metadata │
│ │ metadata: │ │ │
│ │ source_desc: ... │ ▼ │
│ │ source_url: ... │ Injects into proofs │
│ │ author: ... │ │ │
│ │ license: ... │ ▼ │
│ │ content: │ concepts minted │
│ │ [article text] │ with full attribution │
│ └─────────────────────┘ │ │
│ ▼ │
│ proofs: [{ │
│ type: "conversation_extraction", │
│ description: "Extracted from...", │
│ reference: "https://...", │
│ author: "...", │
│ license: "..." │
│ }] │
└────────────────────────────────────────────────────────────────────┘

Example: Rebentisch Harvest
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

Workflow 3: CAR Import & Sync
Bringing the mycelium from cloud GPU instance to local machines.

text

┌───────────────────────────────────────────────────────────────────┐
│ CAR IMPORT PIPELINE │
│ │
│ Cloud GPU Local Machine │
│ ┌──────────────────┐ ┌──────────────────┐ │
│ │ Export CAR │ │ incoming_cars/ │ │
│ │ python tools/ │─── download ───→ │ │ │
│ │ export_to_car.py │ │ python tools/ │ │
│ │ --all │ │ import_from_car │ │
│ └──────────────────┘ │ │ │
│ │ Blocks saved │ │
│ │ Index updated │ │
│ │ Provenance │ │
│ │ preserved │ │
│ │ │ │
│ │ Map regenerated │ │
│ │ python tools/ │ │
│ │ generate_ │ │
│ │ mycelium_map.py │ │
│ └──────────────────┘ │
└───────────────────────────────────────────────────────────────────┘

Commands
On cloud GPU: export
```
python tools/export_to_car.py --all --output cadmies_latest.car
```

Download cadmies_latest.car to local incoming_cars/.
On local: import
```
cd /run/media/fedora/PNY/CADMIES/CADMIES-IPLD && source venv/bin/activate
python tools/import_from_car.py incoming_cars/cadmies_latest.car
python tools/generate_mycelium_map.py
```

Workflow 4: Quality Control & Maintenance
text

┌────────────────────────────────────────────────────────────────┐
│ MAINTENANCE WORKFLOW │
│ │
│ ┌─────────────────┐ │
│ │ Remint stale │ python tools/remint_existing_concepts │
│ │ concepts │ --apply │
│ └────────┬────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────┐ │
│ │ Regenerate map │ python tools/generate_mycelium_map.py │
│ │ (v3.0.0 fractal) │ + concepts_ranked.json │
│ └────────┬────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────┐ │
│ │ Check for │ Look for "NOTE: Unmapped domain" │
│ │ unmapped domains │ Add to DOMAIN_UPWARD_MAP if needed │
│ └────────┬────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────┐ │
│ │ Audit concepts │ python -c "scan source_concepts" │
│ │ for issues │ Check difficulty levels, relationships │
│ └────────┬────────┘ │
│ │ │
│ ▼ │
│ ┌─────────────────┐ │
│ │ Export CAR │ python tools/export_to_car.py --all │
│ │ for backup │ │
│ └─────────────────┘ │
└────────────────────────────────────────────────────────────────┘

Commands
Remint any stale CIDs

text
python tools/remint_existing_concepts.py --apply
Regenerate map and check domains

text
python tools/generate_mycelium_map.py
Audit source concepts

text
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
Export backup

text
python tools/export_to_car.py --all --output cadmies_latest.car
Workflow 5: Session Sync
End-of-session synchronization across all nodes.

text

┌───────────────────────────────────────────────────────────────────┐
│ SESSION SYNC │
│ │
│ Cloud GPU ──→ git push ──→ GitHub ──→ git pull ──→ Local (PNY) │
│ │ │ │ │
│ │ │ │ │
│ Commit all Central Local │
│ changes: repository machine │
│ - source_concepts │
│ - map + ranked data │
│ - index │
│ - scripts │
│ - CAR export │
│ │
│ │ │ │
│ │ ▼ │
│ │ Cloud Compute Instance │
│ │ (auto-pull every 5 min) │
│ │ → public gateway updates automatically │
│ │
└───────────────────────────────────────────────────────────────────┘

Commands
On cloud GPU

text
cd /notebooks/CADMIES/CADMIES-IPLD
git add -A
git commit -m "Session XXX: description of changes"
git push origin main
On local (PNY)

text
cd /run/media/fedora/PNY/CADMIES/CADMIES-IPLD && source venv/bin/activate
git pull origin main
Cloud compute instance — no manual step needed. Auto-pulls from GitHub every 5 minutes via cron. Public gateway updates automatically.

text

Changes:
- Date updated to 2026-06-25
- Related docs updated to current phases
- `Paperspace` → `cloud GPU instance` throughout
- `hieros-cadmies.io` → `project-hierion.duckdns.org`
- Map version noted as v3.0.0 fractal in workflow diagrams
- Manual `cp` and `git add docs/` step removed — replaced with auto-deploy note
- Workflow 5 now includes the cloud compute instance as an auto-syncing node
- `concepts_ranked.json` noted in maintenance workflow
