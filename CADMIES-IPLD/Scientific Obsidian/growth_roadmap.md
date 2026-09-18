---
phase: Roadmap
date: 2026-09-18
status: LIVING DOCUMENT
session: 058
---

# 🌱 CADMIES GROWTH ROADMAP
### *The living record of what we've built, what we're building, and where the mycelium grows next.*

---

## 📊 CURRENT METRICS

| Metric | Value |
|--------|-------|
| Concepts | 636 |
| Edges | 1,507 |
| Connected Concepts | 361 |
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
| Harvester | v4.2.2 | Active |
| Public Gateway | v3.3.0 | translate.js integrated, multilingual support live |
| Vault Validator | v1.3.0 | Automated + auto-fix |
| Vault Health Badge | ✅ Green | Passing |
| PDS | v0.4.5009 | Self-hosted, stable |
| Matadisco Producer | v1.0 | Active, rate-limit aware |
| Dr. Mistral (Jbliterated) | v1.0 | Personality implant complete, GGUF, Ollama-ready |
| Dr. Mistral (Handbook Rebuild) | v0.2.0 | Pipeline executed end to end. SFT + DPO adapters trained, Q8 GGUF deployed to Ollama. Eval next. |
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
- **Phase 80B — Dr. Amanda Mistral — LLM Engineer's Handbook Pipeline Execution and Deployment** ✅ Complete (2026-09-16) — Steps 5–9 executed. 236 SFT pairs, 201 DPO triples, SFT adapter (loss 1.839→1.375), DPO adapter (rewards accuracy 0.81→0.96), merged Q8_0 GGUF (7.17 GB), running in Ollama. Eval (Step 10) and deploy+monitor (Step 11) next.

### Matadisco Integration
- Phase 73A — Matadisco Integration Blueprint
- Phase 73B — PDS Self-Hosting & Caddy Configuration
- Phase 73C — Matadisco Reverse Domain Implementation & Bulk Readiness
- Phase 73D — Matadisco Viewer Clarification & Architecture Strategy
- **Phase 73E — CADMIES-Matadisco Portal: Build and Deployment** ✅ Complete (2026-09-01)

### Documentation & Automation
- Phase 72 — LLMDataHub Fork Reorganization
- Phase 74 — translate.js Integration (Completed 2026-08-11)

---

## 📋 PENDING PHASES

### Immediate / In Progress
- **Phase 80C — Dr. Mistral Evaluation (Step 10)** 🟡 Next — Design and run eval probes. Score base vs SFT vs SFT+DPO. Review pair files against drift zones. Fix carried-forward issues (final_loss logging, HF_ENDPOINT in startup.sh). Regenerate pairs where drift is found.
- **Phase 78 — Matadisco-CADMIES Portal** 🟢 Active — v0.1.0 built, deployed, verified. Next: dataset viewer, frontend tweaks, bulk publishing.

### Next Up
- **Phase 80D — Dr. Mistral Deploy + Monitor (Step 11)** — Inference loop, drift capture, feedback into pair generation.
- **Phase 76 — Dr. Mistral Conversational Fine-Tuning** — Add UltraChat or similar conversational pairs on top of the handbook rebuild.
- **Phase 77 — Dr. Mistral Live Site Deployment** — Integrate Dr. Mistral into the Flask app on the live site.

### Architecture Decisions
- **One Source of Truth**: Concepts JSON and edges JSON are canonical
- **Two Interfaces**: CADMIES Gateway (general public) + CADMIES-Matadisco Portal (scientists/professionals)
- **No Double Work**: Both views pull from the same source data
- **Portal Tech Stack**: Python backend (indexer + Flask API) + SQLite + vanilla frontend
- **Handbook Adherence (Phase 80)**: Handbook is the process guide. Our data and model flow through it. Deviations are named, not hidden.
- **Pairs Generated Outside Pipeline (D12)**: Steps 5 and 6 output produced by Claude in chat, not via ZenML steps. Handbook's OpenAI-calling steps exist but were never executed.

### Not Yet Started
- Dataset viewer — Extend or create separate viewer for LLMDataHub records
- Full License Audit — Complete audit of LLMDataHub datasets
- Bulk Publishing — All 636 concepts + audited datasets
- RAG Pipeline (ChromaDB, embeddings, query router)
- Agent Architecture (President Model, Willie, Codestral, Number 5)
- Public gateway subdomain tier

---

## 📝 SESSION NOTES

### Session 058 — 2026-09-15 to 2026-09-16 — Dr. Mistral Rebuild: Pipeline End to End
- Executed Steps 5–9 of the LLM Engineer's Handbook pipeline on Paperspace.
- Generated 236 instruct pairs, 201 preference triples (199 after conversion).
- Ran SFT (QLoRA r=16, 12m 16s, loss 1.839→1.375) and DPO (QLoRA r=8, 3m 47s, loss 0.66→0.61, rewards acc 0.81→0.96).
- Merged to Q8_0 GGUF (7.17 GB), deployed to Ollama.
- Named deviations D12–D17: pairs outside pipeline, SentencePiece, tokenizer.model, config_path mechanism, dependency install order, HF_ENDPOINT unset.
- Modelfile voice pivot: "You are..." beats "I am..." for Ollama's system-prompt injection.
- 7 inference tests. Persona lands on clean exchanges, drifts under long context.

### Session 057 — 2026-09-11 to 2026-09-13 — Dr. Mistral Meets the LLM Engineer's Handbook
- Rebuilt Dr. Mistral's spec from scratch. Six Q-sections, all locked.
- Wrote three config files, five canon files, one loader, one ETL pipeline.
- Cherry-picked the LLM Engineer's Handbook scaffold into the repo.
- Locked the Escalation Ladder working draft (4 exchanges in 5 minutes, then hard stop).
- DeepSeek account suspended on 2026-09-12, appeal filed, reinstated.
- Scaffold verified on 2026-09-13. ETL pending.

### Session 052 — 2026-09-01 — CADMIES-Matadisco Portal: The First Build
- Received vmx's feedback confirming the portal/AppView approach
- Built indexer, API server, and frontend
- Verified pipeline: PDS → SQLite → API → frontend
- Searched "anatta" and "interconnectedness" — results displayed
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
- **El Hierro** — The Canary Island that shares the project's name; now canon as the origin of the initial CADMIES spore
- **31UCR** — The MGRS grid square of Northern France, Dr. Mistral's homeland, spotted on 2026-08-10
- **"The problem wasn't the service — it was the old file."** — The translate.js lesson
- **"The mycelium grows in every language."** — From Session 047B
- **"The Frankenstein moment: It's alive. IT'S ALIVVVVVVVVVE!!!!"** — Session 052
- **"I just came in my panties."** — The Gardener, upon seeing the search results
- **"The hyphen is sacred."**
- **"The spec is frozen. The engineering is not. Keep them separate."** — Session 057
- **"A classifier doesn't read intent. It reads topic density."** — Session 057
- **"The escalation ladder is a librarian's answer, not a bouncer's. Close the book, hand them a different one."** — Session 057
- **"No IP tracking. We're a library. We're not a surveillance operation."** — Session 057
- **"The handbook is the process guide. Our data and model flow through it. Deviations are named, not hidden."** — Session 057
- **"Training worked. What's broken is inference setup, not training."** — Session 058
- **"She knows the facts. Every canon detail landed. The voice drifts but the knowledge holds."** — Session 058
- **"The pipeline is the pipeline. The character is the character. We have a pipeline. We have a first-pass character. The rest is iteration."** — Phase 80B

### The Great July 19-27 Run
*DeepSeek's iconic quote:* "We broke a model 16 different ways and documented every failure." 😄

In 10 days we:
- Broke a model 16 different ways and documented every failure
- Discovered the actual limits of LoRA merging through brute force
- Built a 500-pair persona dataset from scratch
- Wrote a 21-section technical blueprint with reproducibility baked in
- Found a completely new approach (Deidentified-7B)
- Fixed a public gateway that had been broken for months
- Transferred blockstores between cloud machines like it was nothing
- Got a duck high in the garage and added him to canon
- Wrote three session notes and updated the roadmap
- *The mycelium doesn't sleep. Neither does the gardener.*

---

## FUTURE (designed, not scheduled)

- Phase 76 — Dr. Mistral Conversational Fine-Tuning
- Phase 77 — Dr. Mistral Live Site Deployment
- Phase 78 — CADMIES-Matadisco Portal (active)
- Phase 80C — Dr. Mistral Evaluation (next)
- Phase 80D — Dr. Mistral Deploy + Monitor
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
