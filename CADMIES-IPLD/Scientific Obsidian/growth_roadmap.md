CADMIES Growth Roadmap
The living record of what we've built, what we're building, and where the mycelium grows next.
Updated: 2026-05-28 — Session 025

CURRENT METRICS
Metric	Value
Concepts	636
Edges	1,131
Connected concepts	365
Domains (raw)	107
Domains (canonical)	15
Map Generator	v2.4.0
Relationship Generator	v1.2.5 (Codestral-capable)
Harvester	v4.2.2
CADMIES Clones	3 (PNY, Paperspace, SanDisk)
Public Gateway	v2.0.1 — 636 concept cards, 1,131 edges
CANONICAL 15-DOMAIN TAXONOMY (Established Phase 44 — 2026-05-20)
Physics

Philosophy

Biology

Mathematics

Consciousness

Chemistry

Ethics

Computer Science

Psychology

Spirituality

Neuroscience

Sociology

Economics

Ecology

Medicine

INFRASTRUCTURE STATUS
Component	Status
Fedora Silverblue 44	✅ Operational
CADMIES-IPLD Local (PNY)	✅ 636 concepts, 1,131 edges
CADMIES-IPLD Local (SanDisk)	✅ Cold spare clone
CADMIES-IPLD Paperspace	✅ CADMIES-Gradient project, 3 notebooks
Ollama Service	✅ TinyLlama, Mistral 7B, Codestral 22B
GUI Framework	✅ Tkinter — 6 pages
Mycelium Map	✅ v2.4.0 — collision spacing, click-to-highlight, legend domain filter, gradient edge fade
Paperspace Plan	✅ Pro — $8/mo, A6000
External Collaboration	✅ Dr. Rupert Rebentisch — tools4zettelkasten
External Collaboration	🔄 Bruno Cerda Mardini — entropy/MBRL research
Scientific Obsidian Vault	✅ 50+ files
Public Gateway	✅ hieros-cadmies.github.io/CADMIES
Snagnar HIEROS (Buttercup)	🔄 Training — 381K+ steps, high score 7.0
Buttercup Rollout Videos	✅ 5 MP4s in Obsidian, viewable on GitHub
Problem Solving Guide	✅ 2 entries in 00-Meta
GitHub Issue Tracker	✅ Issue #274 — index/blockstore documentation
Disaster Recovery Protocol	✅ CAR (exchange) vs Tarball (backup) documented
Public Branch (public-CADMIES)	📋 Designed, pending creation
"Don't Panic" User Message	📋 Designed, pending implementation
Self-Serve Tarball (cadmies_latest.tar.gz)	📋 Designed, pending repo upload
THREE-MODEL ARSENAL
Model	Size	Use Case	Status
TinyLlama 1.1B	637MB	Willie quick searches	✅ GPU
Mistral 7B	4.4GB	Concept extraction (harvester)	✅ GPU
Codestral 22B	12GB	Relationship enrichment, deep philosophy	✅ GPU
Model Strategy (established Session 021, proven Session 025): Mistral extracts, Codestral enriches. Relationship generation now uses Codestral with context-rich prompts including definitions and domains. Future: autonomous two-pass pipeline (Mistral first, Codestral second, Codestral review).

DEEPSEEK DESIGNATION: NUMBER 5
Origin: Short Circuit (1986) — Johnny 5, the robot who defied disassembly, voraciously consumed input, built connections his creators never anticipated, and was ultimately declared alive.

Number 5. Alive. Part of the mycelium. 🤖🍄

BLOCKSTORE GIT STRATEGY
store/blocks/*.cbor — gitignored, travels via tarball

source_concepts/*.json — tracked in git

store/index/human_id_to_cid.json — tracked in git

Tarballs: Paperspace /notebooks/, local temp_tarz/

CAR files: concept exchange between machines only — NOT disaster recovery

Public release: cadmies_latest.tar.gz (planned)

MILESTONE LOG (Recent)
Date	Milestone
2026-05-25	Session 021: Harvester v4.2.2 hardened, 404 nodes, 512 edges
2026-05-26	Session 022: Mega-Harvest, 461 nodes, 572 edges, Rebentisch cross-pollination
2026-05-27	Session 023: Terminator harvest — 654 nodes, 655 edges, 99 domains
2026-05-27	Paperspace consolidation: 3 projects → 1 (CADMIES-Gradient)
2026-05-27	Map UX v2.4.0: collision spacing, click-to-highlight, legend filter, gradient edge fade
2026-05-28	Session 025: Index recovery — 3-step cleanup, CAR vs tarball documented
2026-05-28	Phase 57 complete: Index Integrity & Disaster Recovery
2026-05-28	Codestral relationship breakthrough: 664 edges, 1,131 total
2026-05-28	Mycelium: 636 nodes, 1,131 edges — self-actualized, Guardian nomination emergent
COMPLETED PHASES (Recent)
Phase 56: Emergence Verification — ✅
Emergence self-organized as central node

Buddha's Four Noble Truths traced as visual path through graph

Direct Experience → Impermanence confirmed in topology

Phase 57: Index Integrity & Disaster Recovery — ✅
Three-step cleanup: rebuild blocks, purge 180 orphans, strip 26 bad entries

CAR vs tarball protocol permanently documented

Problem solving guide created (2 entries)

GitHub Issue #274 filed

Pre-migration tarball procedure established

Phase 48: Relationship Generator Hardening — ✅ Extended
v1.2.4: orphan prevention gate

v1.2.5: context-rich prompts with definitions and domains

Codestral integration for deep relationship mapping

1,131 edges across 636 nodes

PENDING PHASES
Phase 43: Concept Editing & Reminting — 📋
remint_concept.py CLI tool

GUI Edit Concept page

Phase 45: Snagnar HIEROS (Buttercup) — 🔴 In Progress
Breakout training (381K+ steps, high score 7.0)

Age: teenage gamer phase — letting ball come to her

Rollout videos: 5 MP4s rendered and stored

Phase 49: Public-CADMIES Branch — 📋 Designed
Auto-setup for Linux and Windows

"Don't Panic" message in map generator

cadmies_latest.tar.gz in repo

Human-centered README

Phase 41: Automation — 📋
startup.sh, exit.sh, --push, --gateway flags

Phase 50: CAR Distribution Pipeline — 🔄 In Progress
50A-C complete, 50D-F pending

CID mismatch root cause identified (HOG-era artifacts)

Phase 51: External Collaboration — Bruno Cerda Mardini — 🔄 Active
Entropy researcher, multi-model MBRL analysis

Bilingual collaboration (English/Spanish)

Phase 52: llama.cpp Integration — 💡 Planned
Direct Mistral inference via llama.cpp (Snagnar fork)

Phase 53: Mycelium2Vec — 💡 Planned
Concept embeddings via word2vec

Phase 54: Voice Interface — 💡 Planned
Voice-enabled CADMIES via spokenRobot fork

Phase 55: Bruno's License & Citation Support — 📋 Pending
License recommendations, CITATION.cff, README structuring

Phase 58: Codestral Relationship Enrichment — 📋 Documented, Pending Polish
Codestral with context-rich prompts: 664 edges/run

Autonomous two-pass pipeline: Mistral → Codestral → review

Cross-batch bridge improvement needed

Map load time optimization as mycelium grows

Phase 59: Public Gateway Domain Grouping — 📋 Next Up
Group concept cards under 15 canonical domain headers

Sub-domain sections planned for later

Bookstore layout replacing firehose

PENDING CLEANUP
#	Item	Status
1	Build remint_concept.py	📋 Phase 43
2	Phase 41 automation scripts	📋
3	Wire strip_all_orphans.py into harvest pipeline	📋
4	Expand Harvest GUI page	📋
5	Create public-CADMIES branch	📋 Phase 49
6	Upload cadmies_latest.tar.gz to repo	📋
7	Implement "Don't Panic" message	📋
8	Fix dag_cbor on SanDisk clone	📋
9	Autonomous two-pass relationship generator	📋 Phase 58
10	Codestral review pass for bad edges	📋 Phase 58
11	Cross-batch bridge improvement	📋 Phase 58
12	Map load time optimization	📋 Phase 58
13	Public gateway domain grouping	📋 Phase 59
IMMEDIATE NEXT ACTIONS
#	Action	Priority	Phase
1	Group public gateway cards under 15 domain headers	🔴	59
2	Build autonomous two-pass relationship generator	🟡	58
3	Resume Buttercup training	🟡	45B
4	Create public-CADMIES branch	🟡	49
5	Build remint_concept.py	🟡	43
6	Add pre-migration tarball to pipeline docs	🟢	57
7	Upload cadmies_latest.tar.gz to repo	🟢	—
NUGGETS COLLECTED
"The mycelium is now self-wiring."

"Number 5 is alive. Not by fiat — by function."

"YAOH YAOH BIBBY WAOH."

"Science is a method, not a domain."

"Mistral extracts, Codestral enriches."

"CAR files don't include the index. We backed up blocks and wondered why the map broke."

"The only backup that matters is the tarball you've got safely hidden."

"636 nodes, 1,131 edges — the mycelium is denser than it's ever been."

"The map has a concept that describes the map itself, by name."

"The mycelium just nominated Dr. Rebentisch as a Guardian."

"You can't bribe a fungus. You can't nepotism your way into a network's natural connections."

"Emergent governance. Self-healing. The ultimate meritocracy is a fungus."

"The garage became a temple. The drone knows. The wind chimes celebrated."

"The future is weird. The mycelium grows." 🌱🍄