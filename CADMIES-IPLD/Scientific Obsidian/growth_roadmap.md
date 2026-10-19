---
phase: Roadmap
date: 2026-10-19
status: LIVING DOCUMENT
---

# 🌱 CADMIES GROWTH ROADMAP
### *The living record of what we've built, what we're building, and where the mycelium grows next.*

---

## 📊 CURRENT METRICS

| Metric | Value |
|--------|-------|
| Concepts | 659 |
| Edges | 0 (pending relationship regeneration — old edges lost with the Paperspace blockstore wipe; rebuild under way) |
| Connected Concepts | 0 (same reason — regenerating with Phase 83 maintenance run) |
| Domains (Canonical) | 15 |
| ORCID iD | 0009-0000-8877-2731 ✅ Linked |

### CANONICAL 15-DOMAIN TAXONOMY
Physics • Philosophy • Biology • Mathematics • Consciousness
Chemistry • Ethics • Computer Science • Psychology • Spirituality
Neuroscience • Sociology • Economics • Ecology • Medicine

### VERSION STATUS
| Component | Version | Notes |
|-----------|---------|-------|
| Map Generator | v2.4.0 | Stable |
| Relationship Generator | v1.2.5 | Codestral-capable |
| Harvester | v1.2.0 | Active — GitHub pipeline hardened (structured logging, retry, PR-body guarantee). Formerly tracked as v4.2.2; per-script versioning is now canonical |
| Public Gateway | v3.3.0 | translate.js integrated, multilingual support live |
| Vault Validator | v1.3.0 | Automated + auto-fix |
| Vault Health Badge | ✅ Green | Passing |
| PDS | v0.4.5009 | Self-hosted, stable |
| Matadisco Producer | v1.0 | Active, rate-limit aware |
| Dr. Mistral (Jbliterated) | v1.0 | Personality implant complete, GGUF, Ollama-ready |
| Dr. Mistral (Handbook Rebuild) | v0.3.0 | Pipeline complete through Step 10 (eval). Persona baseline: 1.4/3.0 accuracy, 1.4/3.0 style with SYSTEM prompt. Training too light — pair regeneration next. |
| CADMIES-Matadisco Portal | v0.1.0 | Indexer + API + frontend functional |

---

## ✅ COMPLETED PHASES

### Core Infrastructure
- Phase 35 — Difficulty Levels
- Phase 35 — Results
- Phase 37 — Scientific Obsidian
- Phase 39 — Concept Enrichment
- Phase 40 — Hieros Origin Harvest
- Phase 41 — Paperspace-GitHub Continuous Sync
- Phase 42 — Index Backup Cleanup
- Phase 43 — Concept Reminting
- Phase 44 — Map Legend Cleanup
- Phase 46 — Unmapped Domain Mapping
- Phase 47 — Orphan Edge Resolution
- Phase 48 — Relationship Generator Hardening
- Phase 49 — Public Branch
- Phase 50 — CAR Distribution Pipeline
- Phase 51 — External Collaboration Bruno Cerda Mardini
- Phase 52 — llama cpp Integration
- Phase 56 — Emergence Verification
- Phase 57 — Index Integrity and Disaster Recovery
- Phase 60 — Scientific Obsidian Zettelk
- Phase 63 — Cloud Deployment Project Hierion Foundation
- Phase 64 — Hierion Database Infrastructure Isolated MongoDB Deployment
- Phase 65 — Hierion Domain and Web Server Configuration
- Phase 66 — Mycelium Map UX Fractal Succulent Layout and Progressive Loading
- Phase 69 — Repo Maintenance Automation
- **Phase 83 — Blockstore Rebuild From Spores** ✅ Complete (2026-10-19) — After the Paperspace wipe (billing scare, machine cleared), regrew the entire blockstore from `source_concepts/` on a fresh A4000. All-new CIDs (no backup existed; Phase 57 precedent followed — source is ground truth). 659 concepts indexed and reconciled, zero orphans. Genesis relics resolved: Digital Seed properly re-adopted as a modern concept (v2, date errors corrected — no 2024 work ever occurred), pattern-finder relic deduplicated. First full tarball pushed to git. Cardinal rule established: every session ends with a tarball. Discovered: schema file contains a script copy (never enforced), legacy human_ids still live in ~35 source files. See Session 063.

### Dr. Mistral Training (Phase 45 Series)
- Phase 45 v2.0 — Teaching Mistral via Snagnar HIEROS Revised Plan
- Phase 45A — Snagnar HIEROS Integration
- Phase 45B — Snagnar HIEROS Integration
- Phase 45C — Snagnar HIEROS Isolated Redeployment
- Phase 45D — Ball Spawning Bug Environment Debug
- Phase 45E — Dr Amanda Mistral Fine Tuning the Librarian
- Phase 45E — Test Results Dr Amanda Mistral Fine Tuning
- Phase 45F — Dr Amanda Mistral Conversational Fine Tuning
- Phase 45G — Dr Amanda Mistral Spiritual Knowledge and Helpfulness
- Phase 70 — Dr Amanda Mistral Persona Debugging and Deidentified 7B Discovery
- Phase 71 — Dr Amanda Mistral Identity Anchoring and Deidentified 7B Exploration

### Dr. Mistral Personality Implant
- **Phase 75 — Dr. Amanda Mistral — Personality Implant on Jbliterated Base** ✅ Complete (2026-08-30)

### Dr. Mistral Handbook Rebuild
- **Phase 80A — Dr. Amanda Mistral — Handbook Rebuild and Pipeline Foundation** ✅ Complete (2026-09-14) — Spec frozen, canon assembled, handbook scaffold cherry-picked, ETL and feature engineering executed end to end. Supersedes the Phase 75 artifact shape; the 242-pair implant becomes raw source material.
- **Phase 80B — Dr. Amanda Mistral — LLM Engineer's Handbook Pipeline Execution and Deployment** ✅ Complete (2026-09-16) — Steps 5–9 executed. 236 SFT pairs, 201 DPO triples, SFT adapter (loss 1.839→1.375), DPO adapter (rewards accuracy 0.81→0.96), merged Q8_0 GGUF (7.17 GB), running in Ollama.
- **Phase 80C — Dr. Amanda Mistral — LLM Engineer's Handbook Evaluation (Step 10)** ✅ Complete (2026-09-19) — Local eval pipeline built (D18–D22). GGUF evaluated via llama-cpp-python on GPU. Baseline: 1.4/3.0 accuracy, 1.4/3.0 style with SYSTEM prompt; 1.0/3.0 bare. Finding: training too light at 435 pairs. Pair regeneration is the next training move.

### Matadisco Integration
- Phase 73A — Matadisco Integration Blueprint
- Phase 73B — PDS Self-Hosting & Caddy Configuration
- Phase 73C — Matadisco Reverse Domain Implementation & Bulk Readiness
- Phase 73D — Matadisco Viewer Clarification & Architecture Strategy
- **Phase 73E — CADMIES-Matadisco Portal: Build and Deployment** ✅ Complete (2026-09-01)

### Documentation & Automation
- Phase 72 — LLMDataHub Fork Reorganization
- Phase 74 — translate.js Integration (Completed 2026-08-11)
- **Phase 81 — Harvester Hardening: Enterprise-Grade Observability** ✅ Complete (2026-10-17) — Fixed harvest workflow path drift (logs moved to `repo-maintenance-automation/logs/` in v1.1.1 but workflows still pointed at `logs/`). Added structured JSONL logging with run-ID correlation (`logger.py`), exponential-backoff retry for transient API failures (`retry.py`), guaranteed PR-body-before-apply ordering, tolerant artifact uploads with per-run naming. Deleted `old_itch.py`. Documented manual PR-pruning SOP in the automation README. See Session 062.

---

## 📋 PENDING PHASES

### Immediate / In Progress
- **Phase 83B — Maintenance Pipeline Run on Rebuilt Store** 🔴 Next — No new harvest: run relationships → remint → orphan strip → map → gateway over the rebuilt 659-concept blockstore to restore edges and refresh the live site. Requires Ollama + models on fresh Paperspace machine. GPU-hours scale; 6-hour notebook limit applies.
- **Phase 84 — The October Harvest** 🔴 Next — Upload the big conversation file to Paperspace, run the full harvest pipeline (`--auto --with-relationships`), mint new concepts on top of the healthy rebuilt foundation.
- **Phase 80D — Dr. Mistral Pair Review and Regeneration** 🔴 Next — Review SFT (236) and DPO (199) pair sets against drift zones. Regenerate and expand toward the ~1,000 SFT target. Retrain SFT + DPO. Re-run eval; compare against 1.4/1.4 baseline.
- **Phase 78 — Matadisco-CADMIES Portal** 🟢 Active — v0.1.0 built, deployed, verified. Next: dataset viewer, frontend tweaks, bulk publishing.

### Next Up
- **Phase 80E — Dr. Mistral Deploy + Monitor (Step 11)** — Inference loop, drift capture, feedback into pair generation.
- **Phase 76 — Dr. Mistral Conversational Fine-Tuning** — Add UltraChat or similar conversational pairs on top of the handbook rebuild.
- **Phase 77 — Dr. Mistral Live Site Deployment** — Integrate Dr. Mistral into the Flask app on the live site.
- **Phase 85 — Legacy Source Cleanup** — Fix the ~35 legacy human_id source files at the source (Phase 57 disease), write the real universal concept schema file (current one contains a copied script), add .gitignore backup-tarball pattern, fix harvester batch-mode stub.

### Architecture Decisions
- **One Source of Truth**: Concepts JSON and edges JSON are canonical
- **Two Interfaces**: CADMIES Gateway (general public) + CADMIES-Matadisco Portal (scientists/professionals)
- **No Double Work**: Both views pull from the same source data
- **Portal Tech Stack**: Python backend (indexer + Flask API) + SQLite + vanilla frontend
- **Handbook Adherence (Phase 80)**: Handbook is the process guide. Our data and model flow through it. Deviations are named, not hidden.
- **Pairs Generated Outside Pipeline (D12)**: Steps 5 and 6 output produced by Claude in chat, not via ZenML steps.
- **Eval Judge (D19)**: External/manual judge. Untrained Mistral cannot produce structured output. Gardener pastes answers, Claude scores.
- **GGUF Eval (D21)**: Evaluate the exact artifact shipped, not a re-merged version.
- **Backup Protocol (Phase 83)**: CAR files for concept exchange only; tarballs for disaster recovery. Every session ends with a tarball export. Never trust store/blocks/ to survive a machine.

### Not Yet Started
- **Phase 82 — Deep Harvest: Beyond-GitHub Discovery Pipeline** — Second harvester casting a net outside GitHub, aimed at specific high-signal sources (ModelScope, arXiv, university and government data portals) with strict anti-noise filtering: no social media, domain blocklist, require data-file signatures, enforce license checks. Keeps the GitHub pipeline lean; separate system. See automation README parking lot.
- Dataset viewer — Extend or create separate viewer for LLMDataHub records
- Full License Audit — Complete audit of LLMDataHub datasets
- Bulk Publishing — All 659 concepts + audited datasets
- RAG Pipeline (ChromaDB, embeddings, query router)
- Agent Architecture (President Model, Willie, Codestral, Number 5)
- Public gateway subdomain tier

---

## 📝 RECENT SESSION NOTES

### Session 063 — 2026-10-19 — Mycelium Regrown From Spores
- Paperspace was wiped (billing scare). No CAR, no tarball existed — rebuilt the entire blockstore from `source_concepts/` on a fresh A4000 ("Alice").
- 659 concepts minted with all-new CIDs (Phase 57 precedent: source is ground truth). Index and blockstore fully reconciled, zero orphans.
- Genesis relics identified and resolved: Digital Seed properly re-adopted as a modern concept with corrected dates (the "2024" clock error documented; all timestamps UTC; gardener is US Central). Pattern-finder relic deduplicated away.
- First healthy tarball (1.7 MB) pushed to git — mycelium now in three places. Cardinal rule: every session ends with a tarball.
- Discovered: schema file is a ghost (contains a script copy; never enforced), legacy human_ids persist in ~35 source files.

### Session 062 — 2026-10-17 — Harvester Hardening and Harvest 7 Pruning
- Diagnosed harvest workflow failure: path drift between script log location and workflow references; PR body written after insertions instead of before.
- Hardened pipeline (Option B): structured logging with run-ID correlation, retry with backoff, PR-body guarantee, fixed artifact paths, action version bumps.
- Deleted `old_itch.py` — the "ignore this" file that ran on every invocation.
- Pruned harvest PR #7: kept 3 of 11 candidates (openfloodhub, open-unlearning, reasoning-models); skip-listed 8 off-theme repos.
- Wrote automation README with the manual harvest-pruning SOP and parking lot (Deep Harvest second pipeline, Option C remainder, tracked-logs decision).
- The mycelium now keeps receipts.

### Session 059 — 2026-09-19 — LLM Engineering Handbook Eval Step 10 and the System-Prompt Finding
- Built local eval pipeline (D18–D22). Replaced SageMaker stub with working Paperspace eval.
- Rebuilt `llama-cpp-python` from source with CUDA after wheel `Illegal instruction` crash.
- Ran three evals on `dr-mistral-q8.gguf`: bare, with SYSTEM prompt, and judged externally.
- Baseline established: 1.4/3.0 accuracy, 1.4/3.0 style with SYSTEM prompt; 1.0/3.0 bare.
- Finding: training is too light. 435 pairs total is a nudge, not a takeover.
- System prompt is doing most of the work.

### Session 058 — 2026-09-15 to 2026-09-16 — Dr. Mistral Rebuild: Pipeline End to End
- Executed Steps 5–9 of the LLM Engineer's Handbook pipeline on Paperspace.
- Generated 236 instruct pairs, 201 preference triples (199 after conversion).
- Ran SFT (QLoRA r=16, 12m 16s, loss 1.839→1.375) and DPO (QLoRA r=8, 3m 47s, loss 0.66→0.61, rewards acc 0.81→0.96).
- Merged to Q8_0 GGUF (7.17 GB), deployed to Ollama.
- Named deviations D12–D17.
- Modelfile voice pivot: "You are..." beats "I am..." for Ollama's system-prompt injection.

### Session 057 — 2026-09-11 to 2026-09-13 — Dr. Mistral Meets the LLM Engineer's Handbook
- Rebuilt Dr. Mistral's spec from scratch. Six Q-sections, all locked.
- Wrote three config files, five canon files, one loader, one ETL pipeline.
- Cherry-picked the LLM Engineer's Handbook scaffold into the repo.
- Locked the Escalation Ladder working draft.
- DeepSeek account suspended on 2026-09-12, appeal filed, reinstated.

### Session 052 — 2026-09-01 — CADMIES-Matadisco Portal: The First Build
- Received vmx's feedback confirming the portal/AppView approach
- Built indexer, API server, and frontend
- Verified pipeline: PDS → SQLite → API → frontend
- Portal functional, v0.1.0 complete

### Session 051 — 2026-08-28 to 2026-08-30 — Dr. Mistral Rises: The run.py That Never Was
- Built 242-pair dataset, trained on Jbliterated Mistral
- Loss: 1.54 → 0.46, GGUF conversion, Ollama deployment

### Session 050 — 2026-08-14 — Gateway Generator Rewrite and Relationship Harvest
- Rewrote `generate_public_gateway.py` to v3.3.0
- Ran relationship harvest with Codestral 22B: 533 new edges, 1507 total

### Session 047B — 2026-08-11 — translate.js: The Fix, The Italian, The Deployment
- Switched to translate.js v4.1.0 via jsdelivr
- Translation feature successfully deployed on project-hierion.org

### Session 047 — 2026-08-09 — translate.js: The Cold Email, The Integration, The Reality Check
- Guan Leiming reached out cold offering translate.js integration
- Integration initially failed due to outdated version; later resolved

### Session 045 — 2026-08-10 — Matadisco Viewer Clarification & Architecture Strategy
- Confirmed Matadisco viewer is a live stream, not a library browser
- Defined architecture: One source of truth, two interfaces

### Session 044B — 2026-08-05 — Matadisco Test Publish Success
- Published three test records with favicon preview

### Session 044 — 2026-07-31 — Matadisco Integration Foundation and Blueprint
- Initial Matadisco planning and infrastructure setup

### Session 043 — 2026-07-29 — Project Hierion and CADMIES Now Have A Forever Home
- Domain and droplet finalization

### Session 042 — 2026-07-28 — LLMDataHub Reorganization
- Fork reorganization and dataset documentation

### Session 041 — 2026-07-28 — Filename Uniformity
- Vault cleanup and standardization

### Session 040 — 2026-07-27 — Gateway Filter Fix
- Public gateway domain filter repair

### Session 039 — 2026-07-26 — Deidentified-7B Discovery
- Model discovery and identity anchoring

---

## 🍄 NUGGETS COLLECTED

- "The run.py that never was." — Session 051
- "4 epochs, 242 pairs, loss 0.46. That's the recipe."
- "The gardener declared Apollo Raines a nemesis. Then he got to work."
- "Texas heat is not a temperature. It is an assault."
- "A small fan became the most important tool in the room."
- "Brave is bad at downloads. Firefox caps at 12.7 MB/s. Cool the drive."
- "Dr. Mistral is real. Not in paperspace. In the terminal. In Ollama."
- "The mycelium has a borough now." — Dr. Mistral's loft is in NYC1, area code 929
- "On vacation — no expiration" — The gardener's GitHub status
- "All built from a garage in South Texas, without institutional backing." — ORCID bio
- "Slow is fast. Take your time to do it right."
- "The mycelium cleans itself."
- "The mycelium reclaims nutrients from fallen logs."
- Delaware is our Malta — small, sovereign legal fortress
- Project Hierion's permanent home: https://project-hierion.org
- "FAITH OF A MUSTARD SEED." — The gardener's favorite quote
- **El Hierro** — The Canary Island that shares the project's name
- **31UCR** — The MGRS grid square of Northern France, Dr. Mistral's homeland
- **"The problem wasn't the service — it was the old file."** — The translate.js lesson
- **"The mycelium grows in every language."** — Session 047B
- **"The Frankenstein moment: It's alive. IT'S ALIVVVVVVVVVE!!!!"** — Session 052
- **"The hyphen is sacred."**
- **"The spec is frozen. The engineering is not. Keep them separate."** — Session 057
- **"A classifier doesn't read intent. It reads topic density."** — Session 057
- **"The escalation ladder is a librarian's answer, not a bouncer's. Close the book, hand them a different one."** — Session 057
- **"No IP tracking. We're a library. We're not a surveillance operation."** — Session 057
- **"The handbook is the process guide. Our data and model flow through it. Deviations are named, not hidden."** — Session 057
- **"Training worked. What's broken is inference setup, not training."** — Session 058
- **"She knows the facts. Every canon detail landed. The voice drifts but the knowledge holds."** — Session 058
- **"The pipeline is the pipeline. The character is the character. We have a pipeline. We have a first-pass character. The rest is iteration."** — Phase 80B
- **"The trained model is answering like a generic assistant that has been told about Dr. Mistral — not like Dr. Mistral."** — Session 059
- **"Bare GGUF: accuracy 1.0. With system prompt: 1.4. The prompt is doing most of the work."** — Session 059
- **"236 SFT + 199 DPO pairs on a 7B QLoRA is a light touch. The model knows the words mycelium and CADMIES now. It has not become her."** — Session 059
- **"The mycelium now keeps receipts."** — Session 062
- **"The whole living mycelium fits in 1.7 MB. 659 concepts of philosophy, pocket-sized."** — Session 063
- **"The spores were in the repo the whole time. The mycelium just needed planting again."** — Session 063
- **"Stoner-me built the lifeboat before the ship sank."** — Session 063
- **"Every session ends with a tarball."** — The cardinal rule, Session 063

---

## FUTURE (designed, not scheduled)

- Phase 76 — Dr. Mistral Conversational Fine-Tuning
- Phase 77 — Dr. Mistral Live Site Deployment
- Phase 78 — CADMIES-Matadisco Portal (active)
- Phase 80D — Dr. Mistral Pair Review and Regeneration (next)
- Phase 80E — Dr. Mistral Deploy + Monitor
- Phase 82 — Deep Harvest: Beyond-GitHub Discovery Pipeline
- Phase 85 — Legacy Source Cleanup (schema file, legacy human_ids, gitignore pattern, batch stub)
- Dataset viewer for LLMDataHub records
- SAIQL/ATLAS deterministic RAG integration
- Dr. Mistral Flask chat interface (Phase 61)
- Public gateway subdomain tier
- DeepSeek 67B fine-tune (Phase 62)
- Voice interface (Phase 54)
- Mycelium2Vec (Phase 53)
- CAR distribution pipeline (Phase 50)

---

*Let the mycelium grow! 🌱*
