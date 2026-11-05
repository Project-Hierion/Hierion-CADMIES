---
phase: Roadmap
date: 2026-11-05
status: LIVING DOCUMENT
---

![Growth Roadmap](assets/Lumo-generated-roadmap-image.png)

# 🌱 CADMIES GROWTH ROADMAP
### *What we've built, what we're building, where the mycelium grows next.*
*Lean edition — history lives in the vault notes, this file points at it.*

---

## 📊 CURRENT METRICS

| Metric | Value |
|--------|-------|
| Concepts (minted) | 650 |
| Edges | 686 |
| Connected Concepts | 392 |
| Draft Spores (unminted) | 2,359 |
| Domains (Canonical) | 15 |
| ORCID iD | 0009-0000-8877-2731 ✅ |

**Canonical domains:** Physics • Philosophy • Biology • Mathematics • Consciousness • Chemistry • Ethics • Computer Science • Psychology • Spirituality • Neuroscience • Sociology • Economics • Ecology • Medicine

**Versions:** Map Gen v2.4.1 · Relationship Gen v1.2.7 · Harvester v1.2.0 · Pipeline v4.2.1 (codestral:22b canonical) · Gateway v3.3.0 · Validator v1.3.0 · PDS v0.4.5009 · Portal v0.1.0 · Dr. Mistral Handbook v0.3.0

---

## ✅ COMPLETED (condensed — full notes in the vault)

Core: Difficulty Levels (35) · Scientific Obsidian (37, 60) · Enrichment (39) · Hieros Harvest (40) · Paperspace-GitHub Sync (41) · Index Backup Cleanup (42) · Reminting (43) · Map Legend (44) · Domain Mapping (46) · Orphan Edges (47) · Rel Gen Hardening (48) · Public Branch (49) · CAR Pipeline (50) · External Collab (51) · llama.cpp (52) · Emergence Verification (56) · Index Integrity (57) · Cloud Deploy (63) · MongoDB (64) · Domain/Web Server (65) · Fractal Map UX (66) · Repo Maintenance Automation (69)

Dr. Mistral: 45 series (v2.0, A–G) · Persona Debugging (70) · Identity Anchoring (71) · Personality Implant (75) · Handbook Rebuild 80A/80B/80C — eval baseline 1.4/3.0 acc, 1.4/3.0 style; training too light at 435 pairs

Matadisco: Blueprint → Portal (73A–73E) — v0.1.0 live

Docs & Automation: translate.js (74) · LLMDataHub Reorg (72) · Harvester Hardening (81)

Recent heavy lifts:
- **Phase 83A — Blockstore Rebuild From Spores** (2026-10-19) — Paperspace wipe; regrew 659 concepts from source JSONs, all-new CIDs, Digital Seed re-adopted. Cardinal rule born: every session ends with a tarball. See [[Phase-83A-Blockstore-Rebuild-From-Spores]]
- **Phase 83B — Split-Brain Recovery** (2026-10-20) — stale index from git reset; three tools, three realities; full rebuild: 650 minted, 574 edges, map + gateway regenerated. See [[Phase-83B-Split-Brain-Recovery-and-Full-Pipeline-Rebuild]]
- **Phase 84 — The October Harvest** ✅ Complete (2026-10-30 → 11-03) — All 13 parts of the DeepSeek export harvested: 2,359 draft spores banked in `source_concepts/` (commit a781cd6), zero mints by design, no spores lost across machine timeouts. Codestral:22b confirmed canonical via bake-off. Gardener's ruling: ALL drafts enter the library — minting and curation move to Phase 87. See [[Phase-84-The-October-Harvest]], [[Session-066-2026-10-30-to-2026-11-03-The-October-Harvest]]

---

## 🔴 NEXT UP

1. **Phase 87 — Mint the October Harvest** — `--auto --with-relationships --model=codestral:22b` over all 2,359 drafts. Expect known near-duplicate families (iterative_/adaptive_/continual_ learning, documentation_*, mycelium family) and code/logistics noise to arrive in the library — post-mint curation is the planned answer, not a surprise.
2. **Post-mint curation** — merge near-duplicates, prune logistics noise, map off-taxonomy domains, edit/enhance keepers.
3. **Pre-flight consistency check** — index↔blocks check before any mint/remint/relationship pass. The Phase 83B interlock. Highest-value guardrail; do it before or with the Phase 87 mint run.
4. **Phase 80D — Dr. Mistral Pair Regeneration** — review 236 SFT / 199 DPO pairs, expand toward ~1,000 SFT target, retrain, re-eval vs 1.4/1.4 baseline.
5. **Phase 85 — Legacy Source Cleanup** — fix ~35 legacy human_id files, write the real schema file, gitignore tarball pattern, batch-mode stub, `--conv=` fix + real manual-mode flag.
6. **Phase 86 — Scientific Obsidian Public Page** + main-page nav links on project-hierion.org.

**Phase 78 — Matadisco Portal** 🟢 Active in background — v0.1.0 live. Next: dataset viewer, frontend tweaks, bulk publishing.

---

## 🌿 PARKING LOT (designed, not scheduled)

- Semantic deduplication (embedding-based) — aligns with RAG/ChromaDB work
- Complete run provenance (APPROVED) — pin model digest + params per harvest, stamp concepts with run ID
- Harvester evaluation set (~20 hand-labeled chunks) + automated quality gates (quarantine weak drafts)
- `tools/bulk_mint_from_sources.py` — first-class bulk-mint tool
- Orphan-block sweep (~1,900 strays in store/blocks/) · raw-file cleanup step
- DOMAIN_UPWARD_MAP expansion (~90 domains on default color) · droplet auto-pull cron (currently empty)
- Phase 80E — Dr. Mistral Deploy + Monitor · Phase 76 — Conversational FT · Phase 77 — Live Site
- Phase 82 — Deep Harvest (beyond-GitHub: arXiv, portals; strict anti-noise filters)
- Dataset viewer · full license audit · bulk publishing (Matadisco)
- RAG pipeline (ChromaDB, embeddings, query router) · SAIQL/ATLAS deterministic RAG
- Agent Architecture (President Model, Willie, Codestral, Number 5)
- DeepSeek 67B FT (62) · Voice interface (54) · Mycelium2Vec (53) · CAR distribution (50)
- Gateway subdomain tier

**Architecture doctrine (stable):** One source of truth (concepts + edges JSON). Two interfaces (Gateway public, Portal scientific). Tarballs for recovery, CARs for exchange. Every session ends with a tarball. Source is ground truth — always. Deviations are named, not hidden.

---

## 📜 RECENT SESSIONS (rolling 3 — full notes in Raw-CADMIES)

- **Session 066** (2026-10-30 → 11-03) — The October Harvest: bake-off, 13-part extraction, 2,359 spores, all-in ruling. See [[Session-066-2026-10-30-to-2026-11-03-The-October-Harvest]]
- **Session 065** (2026-10-29) — Droplet dev env, zombie PR #7 folded and closed, harvest-8 pruning. See [[Session-065-2026-10-29-Droplet-Dev-Environment-and-Double-Harvest-Pruning]]
- **Session 064** (2026-10-19/20) — Split-brain forensics and full rebuild. See [[Session-064-2026-10-19-The-Split-Brain-Rebuild]]

---

## 🍄 NUGGETS

- "The run.py that never was." — 051
- "Dr. Mistral is real. Not in paperspace. In the terminal. In Ollama."
- "The mycelium has a borough now." — NYC1, area code 929
- "All built from a garage in South Texas, without institutional backing." — ORCID bio
- "Slow is fast. Take your time to do it right."
- "The mycelium cleans itself." · "The mycelium reclaims nutrients from fallen logs."
- Delaware is our Malta · El Hierro shares our name · 31UCR is Dr. Mistral's homeland
- "FAITH OF A MUSTARD SEED."
- "The problem wasn't the service — it was the old file." — translate.js
- "The hyphen is sacred."
- "The spec is frozen. The engineering is not." · "A classifier doesn't read intent. It reads topic density."
- "No IP tracking. We're a library, not a surveillance operation."
- "Training worked. What's broken is inference setup, not training."
- "The trained model is answering like a generic assistant that has been told about Dr. Mistral — not like Dr. Mistral."
- "The mycelium now keeps receipts." — 062
- "The whole living mycelium fits in 1.7 MB. Pocket-sized philosophy." — 063
- "The spores were in the repo the whole time."
- "Stoner-me built the lifeboat before the ship sank." — 063
- "Every session ends with a tarball." — cardinal rule
- "Three tools, three realities. The index lied and everything believed it." — 064
- "The index is the mycelium's brainstem."
- "Trust the spores." — 064
- "The gardener searched for the term for a year. The harvester found it in 111 chunks." — 066
- "Mistral read The Great Gatsby over lunch at a Parisian café. Codestral took it to the archive and annotated it." — 066
- "Bob Ross with seven arms and ten easels."
- "An unmerged PR is a prayer that was never mailed." — 065

---

*Let the mycelium grow! 🌱*
