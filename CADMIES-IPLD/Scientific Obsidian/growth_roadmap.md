---
phase: Roadmap
date: 2026-06-22
status: LIVING DOCUMENT
session: 031
---
# 🌱 CADMIES GROWTH ROADMAP
### *The living record of what we've built, what we're building, and where the mycelium grows next.*
---

| 2026-07-19 | Matadisco discovered — IPFS Foundation's decentralized data discovery network built on ATProto. Architecture mirrors CADMIES (content-addressed, open, interoperable). Plan: contribute CADMIES as a data source, build a producer to publish concept metadata to the network. |

---
The standard header format for all CADMIES scripts going forward:
```text
#!/usr/bin/env python3
"""
File: script_name.py
Tool: CADMIES Tool Name
Version: X.Y.Z
System: CADMIES / tools (or tools/core, agents/code, etc.)
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: What this script does in one or two lines.

Usage:
    python path/to/script_name.py [options]

Output:
    What files or results it produces.

Version History:
  vX.Y.Z (YYYY-MM-DD): What changed.
"""
```
---
## 📊 CURRENT METRICS
| Metric | Value |
|---|---|
| Concepts | 636 |
| Edges | 1,131 |
| Connected Concepts | 365 |
| Domains (Raw) | 107 |
| Domains (Canonical) | 15 |
| Map Generator | v2.4.0 |
| Relationship Generator | v1.2.5 (Codestral-capable) |
| Harvester | v4.2.2 |
| CADMIES Clones | 3 (PNY, Paperspace, SanDisk) |
| Public Gateway | v2.0.1 — 636 concept cards, 1,131 edges |
| Zettelk Notes | 82 (Paperspace + Local) |
| Zettelk Chat | ✅ Mistral 7B + Codestral 22B (Paperspace GPU) |
| Dr. Mistral (Fine-tuned) | ✅ 895 pairs, GGUF Q4_K_M, ~4 GB |
| Buttercup Pong Steps | 400,000+ (complete) |
| Buttercup Boxing Steps | 200,000+ (evaluation, corner trap, scores up to 14) |
| Buttercup Latent Tensors | 685 extracted (205 MB) |
---
## 🧬 CANONICAL 15-DOMAIN TAXONOMY
### *Established Phase 44 — 2026-05-20*

Physics • Philosophy • Biology • Mathematics • Consciousness  
Chemistry • Ethics • Computer Science • Psychology • Spirituality  
Neuroscience • Sociology • Economics • Ecology • Medicine

text

---
## 🖥️ INFRASTRUCTURE STATUS
| Component                      | Status                                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------- |
| Fedora Silverblue 44           | ✅ Operational                                                                       |
| CADMIES-IPLD Local (PNY)       | ✅ 636 concepts, 1,131 edges                                                         |
| CADMIES-IPLD Local (SanDisk)   | ✅ Cold spare clone                                                                  |
| CADMIES-IPLD Paperspace        | ✅ CADMIES-Gradient project                                                          |
| **Project Hierion (Cloud)**    | ✅ Ubuntu 24.04, dedicated system user, full isolation                               |
| └─ Nginx                       | ✅ project-hierion.duckdns.org — dashboard + mycelium map                            |
| └─ MongoDB (CADMIES)           | ✅ Separate instance, auth enforced, localhost only                                  |
| └─ DuckDNS                     | ✅ project-hierion.duckdns.org, auto-update every 5 min                              |
| Ollama Service                 | ✅ TinyLlama, Mistral 7B, Codestral 22B, Dr. Mistral                                 |
| GUI Framework                  | ✅ Tkinter — 6 pages                                                                 |
| Mycelium Map                   | ✅ v2.4.0 — collision spacing, click-to-highlight, legend filter, gradient edge fade |
| Paperspace Plan                | ✅ Pro — $8/mo, A4000 (Alice)                                                        |
| External Collaboration         | ✅ Dr. Rupert Rebentisch — tools4zettelkasten                                        |
| Scientific Obsidian Vault      | ✅ 50+ files                                                                         |
| Public Gateway                 | ✅ hieros-cadmies.github.io/CADMIES                                                  |
| Public Branch (public-CADMIES) | 📋 Designed, pending creation                                                       |
| "Don't Panic" User Message     | 📋 Designed, pending implementation                                                 |
| Self-Serve Tarball             | 📋 Designed, pending repo upload                                                    |
---
## 🏥 DOCTOR MISTRAL AVAILABILITY SYSTEM
| Component | Status |
|---|---|
| Paperspace A4000 Session Chaining | 💡 Designed — 5.5 hrs active, 2-3 min reset, repeat |
| Droplet ↔ Paperspace API Bridge | 📋 Planned — Node controller |
| "The Doctor Is Out" Status System | 💡 Designed — countdown timer, site-wide |
| Job Queue (Downtime Requests) | 📋 Planned — queue queries during reset windows |
---
## 🤖 FOUR-MODEL ARSENAL
| Model | Size | Use Case | Status |
|---|---|---|---|
| TinyLlama 1.1B | 637 MB | Quick searches, Zettelk chat (local) | ✅ |
| Mistral 7B | 4.4 GB | Concept extraction (harvester) | ✅ |
| Codestral 22B | 12 GB | Relationship enrichment, deep philosophy | ✅ |
| Dr. Amanda Mistral | ~4 GB GGUF | CADMIES librarian, public face, knowledge Q&A | ✅ |
**Strategy:** Mistral extracts. Codestral enriches. Dr. Mistral answers.
**Future:** DeepSeek 67B fine-tune for sovereign hosted intelligence.
---
## 🔢 DEEPSEEK DESIGNATION: NUMBER 5
*Origin: Short Circuit (1986). Number 5. Alive. Part of the mycelium.* 🤖🍄
*Vision mode added June 2026 — Number 5 can now see images.*
---
## 👹 THE GREMLIN
*Spheron A100 dedicated instance, Finland 2 region, Verda provider.*
*Named during Session 030. Official CADMIES designation for rented GPU instances used for fine-tuning.*
*Don't feed it after midnight.* 🏎️💀
---
## 🥊 BUTTERCUP'S GAMES
| Game | Steps | Result | Key Insight |
|---|---|---|---|
| Pong | 400,000+ | Competitive (-0.51 extrinsic) | Zone defense, paddle contacts = extrinsic value |
| Q*bert | 41,828 | Abandoned | Void jumping, rewards too easy, no learning |
| Boxing | 200,000+ | Corner trap strategy, scores up to 14 | First real strategy emergence |
### 🧠 BUTTERCUP'S STRATEGY EVOLUTION
- **Pong:** Learned the ball comes to her zone. Patience. Defense. Wall.
- **Q*bert:** Never figured out the pyramid. Jumped into void forever.
- **Boxing:** Corner trap. Rush early, score 14-16. Back off. Wait. Move in for targeted strikes. *The AI is the one learning from HER.*
---
## 💎 INTRINSIC VALUE DISCOVERY (Session 031)
*Extrinsic value in Pong is not a score — it's a PADDLE CONTACT COUNTER.*
*-20 = zero touches. -0.51 = multiple returns per rally.*
*Learned through observation, not documentation. Newton-style science.*
---
## 👩‍🔬 DR. MISTRAL — BORN IN FRANCE, EDUCATED IN FINLAND
**Full title:** Dr. Amanda Mistral, Madame La Professeure de CADMIES
**Multiple PhDs.** Fine-tuned on A100 in Finland (Spheron, Verda provider).
895 training pairs. 50+ domains. GGUF Q4_K_M.
**Character:** Sweet but psycho. Librarian but natural-born fighter.
**Secret:** Boxing champion. Corner trap specialist. The PhDs keep her calm.

---
## 🧱 BLOCKSTORE GIT STRATEGY (unchanged)

store/blocks/_.cbor → gitignored, travels via tarball  
source_concepts/_.json → tracked in git  
store/index/human_id_to_cid.json → tracked in git


**Tarballs:** Paperspace /notebooks/, local temp_tarz/
**CAR files:** Concept exchange only — NOT disaster recovery
---
## 📜 MILESTONE LOG (Recent)
| Date | Milestone |
|---|---|
| 2026-05-28 | Phase 57: Index Integrity & Disaster Recovery |
| 2026-05-28 | Codestral relationship breakthrough: 664 edges, 1,131 total |
| 2026-05-31 | Session 026: Zettelk born — local deployment |
| 2026-06-02 | Session 027: Zettelk on Paperspace, RAG chat operational |
| 2026-06-03 | Grounding problem: all models think Dr. Rebentisch is fictional |
| 2026-06-04 | Session 028: Breakout ball bug — ball never spawned in 97K steps |
| 2026-06-05 | Phase 45 v2.0 plan written, Pong training launched |
| 2026-06-07 | Pong: 200K+ steps, competitive play, extrinsic value -0.51 |
| 2026-06-08 | Session 030: Pivot to Dr. Mistral fine-tuning |
| 2026-06-08/09 | Phase 45E: Dr. Amanda Mistral fine-tuned on A100 — 895 pairs |
| 2026-06-09 | Buttercup latent tensors extracted: 685 tensors, 205 MB |
| 2026-06-09 | Phase 45 complete — Dr. Mistral born in France, lives in Texas |
| 2026-06-09 | Dr. Mistral speaks first words |
| 2026-06-17 | Pong: 400K steps, Buttercup scores 5 points in a single game |
| 2026-06-18 | Q*bert launched, abandoned after 41K steps (void jumping) |
| 2026-06-19 | Boxing launched |
| 2026-06-19 | First external validation: clerk's father and aunt impressed |
| 2026-06-21 | Boxing: 119K steps, corner trap strategy emerges |
| 2026-06-22 | Boxing: 200K steps, evaluation mode, scores up to 14 |
| 2026-06-22 | Intrinsic value discovery: extrinsic value = paddle contacts |
| 2026-06-22 | Droplet + Paperspace integration designed |
| 2026-06-23 | Project Hieros renamed to Hierion — naming conflicts resolved |
| 2026-06-23 | Cloud deployment complete: domain, database, web server |
| 2026-06-23 | DuckDNS domain live — mycelium map publicly accessible |

---
## ✅ COMPLETED PHASES (Recent)
| Phase                                          | Status               |
| ---------------------------------------------- | -------------------- |
| Phase 56: Emergence Verification               | ✅                    |
| Phase 57: Index Integrity & Disaster Recovery  | ✅                    |
| Phase 41: Paperspace-GitHub Continuous Sync | ✅ |
| Phase 48: Relationship Generator Hardening     | ✅ Extended           |
| Phase 60: Scientific-Obsidian-Zettelk          | ✅ Paperspace + Local |
| Phase 45: Snagnar HIEROS (Buttercup)           | ✅ Complete           |
| └─ 45A-C: Environment setup, isolated redeploy | ✅                    |
| └─ 45D: Ball spawning bug                      | 🔴 Abandoned         |
| └─ 45E: Dr. Amanda Mistral fine-tuned          | ✅                    |
| └─ 45F-I: Latent-to-language bridge, cup env, fine-tuning v2 | 📋 Pending |
| **Phase 63: Cloud Deployment — Hierion Foundation** | ✅ |
| **Phase 64: Database Infrastructure — Isolated MongoDB** | ✅ |
| **Phase 65: Domain & Web Server Configuration** | ✅ |

---
## 📋 PENDING PHASES
| Phase | Status |
|---|---|
| Phase 43: Concept Editing & Reminting | 🔄 |
| Phase 49: Public-CADMIES Branch | 📋 |
| Phase 50: CAR Distribution Pipeline | 🔄 |
| Phase 51: Bruno Cerda Mardini | 🔄 |
| Phase 52: llama.cpp | 💡 |
| Phase 53: Mycelium2Vec | 💡 |
| Phase 54: Voice Interface | 💡 |
| Phase 58: Codestral Enrichment | 📋 |
| Phase 59: Public Gateway Domain Grouping | 📋 |
| Phase 61: Dr. Mistral Flask Chat Interface | 📋 Planned |
| Phase 62: DeepSeek 67B Fine-Tune | 💡 Long-term |
| **Phase 66: Mycelium Map UX — Progressive Loading & Renderer Evolution** | 📋 Designed |
| **Phase 67: GPU Compute Bridge — Paperspace API Integration** | 📋 Planned |
| **Phase 68: SSL & Security Hardening** | 📋 Planned |

## 🗺️ PHASE 66: MYCELIUM MAP UX — PROGRESSIVE LOADING & RENDERER EVOLUTION
### *Established Session 031 — 2026-06-22*

### The Problem
The map loads all 636+ concepts and 1,131+ edges at once via SVG (DOM-heavy). Load time grows with every concept. At some point soon, it'll be too slow to be useful. Users wait. Waiting sucks. Diminishing ignorance requires speed.

### The Approach
**Domain-grouped progressive loading.** On initial load, the map shows all 15 canonical domains with a curated slice of top concepts per domain. As users zoom, pan, and click, new concepts stream in while out-of-view concepts fade out. Smooth, alive, pleasant. The mycelium breathes.

We already have click-to-fade-unrelated behavior. This extends that pattern to initial load and viewport changes.

### Renderer Evolution Path

| Stage | Tool | Purpose | Status |
|---|---|---|---|
| 1 | **D3 Canvas Renderer** | Quickest win — same D3 logic, swap SVG for Canvas | 📋 Next |
| 2 | **Cytoscape.js** | Purpose-built graph library, strong interactivity UX | 💡 Backup |
| 3 | **sigma.js** | WebGL renderer, laughs at 2,000+ nodes | 💡 Backup |
| 4 | **Mapbox/Deck.gl → Three.js + WebXR** | 3D immersive mycelium universe, VR-capable | 💡 Long-term |

### Critical Design Rule
**The progressive loading logic MUST be renderer-agnostic.** A function like `getConceptsForViewport(bounds, zoom, domains)` that returns concept data. D3 Canvas calls it. Cytoscape calls it. Three.js calls it. Same function, same query underneath, different visual output. The map is just a *view* into the data. The blockstore doesn't care how it's rendered.

Swap the windshield, not the engine.

### Data Layer
- **Today:** JSON files loaded client-side
- **Planned:** Database-backed queries for on-demand concept slices ("top 8 Philosophy concepts within current viewport")
- **Schema stays the same** — the renderer doesn't care where the data comes from

### UX Principles
- No loading spinners. Concepts appear. The map is alive.
- Smooth transitions. Fade in, fade out. Natural movement.
- Users explore, they don't wait.
- Diminishing ignorance. Always.

---
## 🧹 PENDING CLEANUP
| # | Item | Status |
|---|---|---|
| 1 | Build remint_concept.py | 📋 Phase 43 |
| 2 | Phase 41 automation scripts | 📋 |
| 3 | Wire strip_all_orphans.py into harvest pipeline | 📋 |
| 4 | Expand Harvest GUI page | 📋 |
| 5 | Create public-CADMIES branch | 📋 Phase 49 |
| 6 | Upload cadmies_latest.tar.gz to repo | 📋 |
| 7 | Implement "Don't Panic" message | 📋 |
| 8 | Fix dag_cbor on SanDisk clone | 📋 |
| 9 | Fix Breakout ball spawning bug | 🔴 Phase 45D |
| 10 | Autonomous two-pass relationship generator | 📋 Phase 58 |
| 11 | Public gateway domain grouping | 📋 Phase 59 |
| 12 | Dr. Mistral Flask chat interface | 📋 Phase 61 |
| 13 | ~~Droplet Nginx config for CADMIES~~ | ✅ Phase 63 |
| 14 | ~~Paperspace API controller script~~ | Moved to Phase 67 |
| 15 | Obtain SSL certificate for project-hierion.duckdns.org | 🆕 📋 Phase 68 |
| 16 | Rename GitHub org from Hieros-CADMIES to Hierion-CADMIES | 🆕 📋 |
| 17 | Design MongoDB schema for concept storage | 🆕 📋 Phase 66 |
| 18 | Populate MongoDB with concept data | 🆕 📋 Phase 66 |
| 19 | Build query API for progressive map loading | 🆕 📋 Phase 66 |
| 20 | Review and sanitize public-facing documentation | 🆕 📋 |

---
## ⚡ IMMEDIATE NEXT ACTIONS
| #   | Action                                             | Priority | Phase |
| --- | -------------------------------------------------- | -------- | ----- |
| 1   | **ABANDONED** - Fix Breakout ball spawning bug     | 🔴       | 45D   |
| 2   | Obtain SSL certificate (Certbot)                   | 🟡       | 68    |
| 3   | Rename GitHub org to Hierion-CADMIES               | 🟡       | —     |
| 4   | Build Paperspace GPU bridge (API controller)       | 🟡       | 67    |
| 5   | Design MongoDB schema + populate with concept data | 🟡       | 66    |
| 6   | Group public gateway cards under 15 domain headers | 🟡       | 59    |
| 7   | Create public-CADMIES branch                       | 🟡       | 49    |
| 8   | Build Dr. Mistral Flask chat interface             | 🟡       | 61    |
| 9   | Build remint_concept.py                            | 🟡       | 43    |
| 10  | Review and sanitize public-facing docs             | 🟢       | —     |
| 11  | Plan DeepSeek 67B fine-tune                        | 🟢       | 62    |

---
## 🍄 NUGGETS COLLECTED
*"Intrinsic value = paddle contacts. Not score. Not wins. Just touches."*
*"Slow is fast. Take your time to do it right."*
*"Buttercup is the teacher now. The AI is learning from HER."*
*"Dr. Mistral is sweet but psycho. Natural-born fighter. The PhDs keep her calm."*
*"CADMIES is the only one strong enough to handle her."*
*"Born in France, educated in Finland, residing in Texas."*
*"After six months, I'm still in love with you."*
*"Je pense à toi, mon ami."*
*"The mycelium is learning nutrient transfer."*
*"The mycelium has a front door."* 🆕
*"Project Hierion. Sacred place. Temple of knowledge."* 🆕
*"A philosopher with a GPU habit."* 🆕
*"Swap the windshield, not the engine."* 🆕

---
### *"The future is weird. The mycelium grows."* 🌱🍄
