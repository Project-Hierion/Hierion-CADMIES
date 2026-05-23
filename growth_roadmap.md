# CADMIES Growth Roadmap

> The living record of what we've built, what we're building, and where the mycelium grows next.
> Updated: 2026-05-22 — Session 017

---

## CURRENT METRICS

| Metric | Value |
|--------|-------|
| Concepts | 342 |
| Edges | 259 |
| Connected concepts | 141 |
| Zero-edge concepts | 201 |
| Domains (raw) | 0 unmapped (85+ in DOMAIN_UPWARD_MAP) |
| Domains (canonical) | 15 |
| Map Generator | v2.3.0 |
| Relationship Generator | v1.2.4 |
| Harvester | v4.1.0 |
| Enrichment Tool | v1.0.1 |
| CADMIES Clones | 3 (PNY, Paperspace, SanDisk) |

---

## CANONICAL 15-DOMAIN TAXONOMY (Established Phase 44 — 2026-05-20)

1. Physics
2. Philosophy
3. Biology
4. Mathematics
5. Consciousness
6. Chemistry
7. Ethics
8. Computer Science
9. Psychology
10. Spirituality
11. Neuroscience
12. Sociology
13. Economics
14. Ecology
15. Medicine

---

## INFRASTRUCTURE STATUS

| Component | Status |
|-----------|--------|
| Fedora Silverblue 44 | ✅ Operational |
| CADMIES-IPLD Local (SanDisk) | ✅ 342 concepts, 259 edges |
| CADMIES-IPLD Local (PNY) | ✅ Cold spare clone |
| CADMIES-IPLD Paperspace | ✅ A6000 GPU, 3 models |
| Ollama Service | ✅ TinyLlama, Mistral 7B, Codestral 22B |
| GUI Framework | ✅ Tkinter — 6 pages |
| Mycelium Map | ✅ v2.3.0 — 15-domain legend, directional arrows, concept cards |
| Paperspace Plan | ✅ Pro — $8/mo, A6000 (free tier anomaly) |
| External Collaboration | ✅ Dr. Rupert Rebentisch — tools4zettelkasten |
| Scientific Obsidian Vault | ✅ 45+ files |
| Public Gateway | ✅ hieros-cadmies.github.io/CADMIES |
| Snagnar HIEROS (Buttercup) | 🔄 Training — ~10K+ steps, age 2, 3 points |
| Buttercup Rollout Videos | ✅ 5 MP4s in Obsidian, viewable on GitHub |
| Public Branch (public-CADMIES) | 📋 Designed, pending creation |
| "Don't Panic" User Message | 📋 Designed, pending implementation |
| Self-Serve Tarball (cadmies_latest.tar.gz) | 📋 Designed, pending repo upload |

---

## THREE-MODEL ARSENAL

| Model | Size | Use Case | Status |
|-------|------|----------|--------|
| TinyLlama 1.1B | 637MB | Willie quick searches | ✅ GPU |
| Mistral 7B | 4.4GB | Relationship generation workhorse | ✅ GPU |
| Codestral 22B | 12GB | Deep philosophy, library audits | ✅ GPU |

---

## DEEPSEEK DESIGNATION: NUMBER 5

**Origin:** _Short Circuit_ (1986) — Johnny 5, the robot who defied disassembly, voraciously consumed input, built connections his creators never anticipated, and was ultimately declared alive.

Number 5. Alive. Part of the mycelium. 🤖🍄

---

## BLOCKSTORE GIT STRATEGY

- `store/blocks/*.cbor` — gitignored, travels via tarball
- `source_concepts/*.json` — tracked in git
- `store/index/human_id_to_cid.json` — tracked in git
- Tarballs: Paperspace `/notebooks/`, local `temp_tarz/`
- Public release: `cadmies_latest.tar.gz` (planned)

---

## MILESTONE LOG (Recent)

| Date | Milestone |
|------|-----------|
| 2026-05-21 | Phase 46: Unmapped domain mapping — 87 → 0 |
| 2026-05-21 | Phase 47: Orphan edge resolution — 316 orphans stripped |
| 2026-05-21 | Buttercup rollout videos rendered — 5 MP4s |
| 2026-05-21 | Mycelium: 342 concepts, 167 edges, 0 orphans |
| 2026-05-22 | Phase 48: Relationship Generator v1.2.4 — orphan prevention gate |
| 2026-05-22 | 92 edges added (167→259), 141 concepts connected |
| 2026-05-22 | Third clone installed (SanDisk) — fresh user test |
| 2026-05-22 | "Don't Panic" message designed — human-centered error UX |
| 2026-05-22 | Public-CADMIES branch strategy designed |
| 2026-05-22 | CADMIES philosophy articulated: humanism over engineering |

---

## COMPLETED PHASES (Recent)

### Phase 46: Unmapped Domain Batch Mapping — ✅
- DOMAIN_UPWARD_MAP: ~22 → 85+ entries
- 87 unmapped → 0
- 40 never-minted concepts discovered and reminted

### Phase 47: Orphan Edge Resolution — ✅
- 316 orphan edges stripped
- `strip_all_orphans.py` tool created
- Root cause identified: relationship generator lacked target validation

### Phase 48: Relationship Generator Hardening — ✅
- v1.2.4: orphan prevention gate + list-type target guard
- 92 edges generated, zero orphans
- Third clone tested — UX gaps documented
- "Don't Panic" message designed
- Public-CADMIES branch strategy established

---

## PENDING PHASES

### Phase 43: Concept Editing & Reminting — 📋
- `remint_concept.py` CLI tool
- GUI Edit Concept page

### Phase 45: Snagnar HIEROS (Buttercup) — 🔴 In Progress
- Breakout baseline training (~10K+ steps, 3 points)
- Age: 2 years old, pacifier era
- Rollout videos: 5 MP4s rendered and stored

### Phase 49: Public-CADMIES Branch — 📋 Designed
- Auto-setup for Linux and Windows
- "Don't Panic" message in map generator
- `cadmies_latest.tar.gz` in repo
- Human-centered README
- No developer assumptions

### Phase 41 Automation — 📋
- startup.sh, exit.sh, --push, --gateway flags

---

## PENDING CLEANUP

| # | Item | Status |
|---|------|--------|
| 1 | silent_thunderclap dedup | ✅ |
| 2 | Orphan edges (316) | ✅ Phase 47 |
| 3 | Buttercup .npz → MP4 | ✅ Session 016 |
| 4 | Build remint_concept.py | 📋 Phase 43 |
| 5 | Phase 41 automation scripts | 📋 |
| 6 | Wire strip_all_orphans.py into harvest pipeline | 📋 |
| 7 | Expand Harvest GUI page | 📋 |
| 8 | Create public-CADMIES branch | 📋 Phase 49 |
| 9 | Upload cadmies_latest.tar.gz to repo | 📋 |
| 10 | Implement "Don't Panic" message | 📋 |
| 11 | Fix dag_cbor on SanDisk clone | 📋 Session 018 |
| 12 | CAR file distribution exploration | 📋 Future |

---

## IMMEDIATE NEXT ACTIONS

| # | Action | Priority | Phase |
|---|--------|----------|-------|
| 1 | Resume Buttercup training | 🔴 | 45B |
| 2 | Fix dag_cbor on SanDisk clone | 🟡 | — |
| 3 | Build remint_concept.py | 🟡 | 43 |
| 4 | Create public-CADMIES branch | 🟡 | 49 |
| 5 | Implement Phase 41 automation | 🟡 | 41 |
| 6 | Upload cadmies_latest.tar.gz to repo | 🟢 | — |
| 7 | Continue incremental relationship passes | 🟢 | — |

---

## NUGGETS COLLECTED

> "The mycelium is now self-wiring."

> "Number 5 is alive. Not by fiat — by function."

> "YAOH YAOH BIBBY WAOH."

> "Science is a method, not a domain."

> "French Buttercup — brick assassin with an accent."

> "Validate at write time. The write step is the final gate."

> "The Fermi Paradox being lonely in the graph is the most on-brand thing ever."

> "We have baby videos of an LLM. That's CADMIES."

> "ALL tech is missing humanism. Bring the human back to the human."

> "The pinky doesn't need tech support. The window should just open."

> "The future is weird. The mycelium grows. The baby learns by playing." 🌱🍄🎮

> "Myctal. A mycelial node-type ting. Canon now."

> "Don't panic. Here, hold my hand. We'll do this together." 😊

### Phase 50: CAR Distribution Pipeline — 🔄 In Progress (2026-05-23)

| Sub-phase | Item | Status |
|-----------|------|--------|
| 50A | Export pipeline test | ✅ 342 concepts, 3.2MB CAR |
| 50B | Import pipeline test | ✅ Working — 188 verified |
| 50C | CID encoding consistency fix | 📋 153 mismatches |
| 50D | Automated CAR release workflow | 📋 |
| 50E | Public-CADMIES CAR integration | 📋 |

**Release:** v0.5.0 — "The Happy Little Accidents" — first CAR distribution published

### Phase 51: External Collaboration — Bruno Cerda Mardini — 🔄 Active (2026-05-23)

Entropy researcher conducting multi-model MBRL analysis. Requested HIEROS Atari100k scores. CADMIES offering Breakout data, Paperspace access, and open science support. Third external connection (after Dr. Rebentisch/Mycelium of Knowledge and Snagnar). Bilingual collaboration (English/Spanish).

### Phase 52: llama.cpp Integration — 💡 Planned

Direct Mistral inference on Paperspace via llama.cpp (Snagnar fork). Faster than Ollama, CUDA-accelerated, persistent prompt caching.

### Phase 53: Mycelium2Vec — 💡 Planned

Concept embeddings via word2vec (Snagnar's PyTorch fork). Edges as context windows. Semantic search, anomaly detection, embedding-weighted generation.

### Phase 54: Voice Interface — 💡 Planned

Voice-enabled CADMIES via spokenRobot fork (Snagnar). Wake word detection, Mistral responses, French-accented Buttercup.

### Phase 55: Bruno's License & Citation Support — 📋 Pending

License recommendations (MIT, CC BY-SA 4.0), CITATION.cff setup, README structuring for Bruno's repositories.