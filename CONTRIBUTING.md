# **First off, thank you for considering contributing to CADMIES! 🧑🏽‍🌾**

## Quick Navigation

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Style Guide](#style-guide)
- [Questions](#questions)

## Code of Conduct

This project adheres to the principles of ethical knowledge sharing (AGPLv3 + Commons Clause). We expect all contributors to:
- Respect the Commons Clause (no commercial exploitation without reciprocity)
- Share improvements back to the community
- Prioritize educational and research purposes
- Be excellent to each other


**This part is for ADVANCED (Experienced Contributors)***
``text
Task	Location	Difficulty
3D Matrix mode for Mycelium Map	mycelium_map.html	Advanced
Path finding between concepts	mycelium_map.html	Advanced
USB Key Infrastructure	tools/core/key_manager.py	Advanced
```

How to Contribute
1. Claim a Task

    Comment on the issue or open a new one

    Say "I'm working on [task name]"

2. Create a Branch

git checkout -b feature/your-feature-name

3. Make Changes

    Follow style guide below

    Test your changes

    Update documentation if needed

4. Commit and Push

git add .
git commit -m "Add: brief description of what you did"
git push origin feature/your-feature-name

5. Open a Pull Request

    Go to GitHub

    Click "Compare & pull request"

    Describe your changes

    Request review

Style Guide

    Follow PEP 8

    Use descriptive variable names

    Add docstrings for functions

    Type hints encouraged

NiceGUI (Frontend)

    Use classes for styling: .classes("w-full p-4")

    Prefer ui.column() and ui.row() over absolute positioning

    Keep JavaScript minimal (air-gap compatibility)

JSON Schemas

    Follow v2.0.0 CID specification

    human_id: snake_case only

    No embedded domain/type in human_id


Getting Help

    Issues: GitHub Issues tab

    Discussions: GitHub Discussions

    Email: hieroscadmies@proton.me

Recognition

All contributors will be:

    Added to CONTRIBUTORS.md

    Mentioned in release notes

    Credited in documentation

License

By contributing, you agree that your contributions will be licensed under AGPLv3 with Commons Clause.

**Let the mycelium grow! 🌱**
*"You can put the tools in people's hands... but whether they will use those tools for genius is quite unpredictable." — Alan Watts*

**Master Roadmap CADMIES-IPLD**
**System:** CADMIES-IPLD | **Updated:** April 8, 2026 | **Status:** ACTIVE

---

## SYSTEM STATUS SNAPSHOT (as of now)
```text
|Component|Status|
|---|---|
|CID Generation|✅ Deterministic (v1.1.0)|
|Provenance Tracking|✅ Auto-creates separate blocks|
|Mycelium Map|✅ 173 nodes, 160 edges, interactive|
|GUI Navigation|✅ Persistent sidebar|
|Easter Eggs|✅ The Cars, The Verve|
|Documentation|✅ Complete suite|
|Air-Gap Compatibility|✅ Client-side live preview|
|CAR File System|✅ COMPLETE|
|HOG Ontology Integration|✅ 39 concepts, 10 domains|
|LLM Bridge|🟡 Ready for integration|
```

---

# PHASE 1: DOCUMENTATION ✅ COMPLETE

- ✅ README notes for first-time users
    
- ✅ CID determinism documented
    
- ✅ Timestamp vs content separation explained
    
- ✅ GUI README with mycelium map and easter eggs
    
- ✅ Source_concepts README with PhD-level template
    
- ✅ CID Structure Specification v2.0.1
    
- ✅ `NOBLE_TRUTHS.md` created
    
- ✅ `COSMIC_SOUNDS.md` created
    

---

# PHASE 2: CAR FILE SYSTEM ✅ COMPLETE
```text
|Component|Status|
|---|---|
|`car_utils.py`|✅ Complete|
|`export_to_car.py`|✅ Complete|
|`import_from_car.py`|✅ Complete|
|`import_from_github.py`|✅ Complete|
|Single/multi/full export|✅ Complete|
|Verification & dry-run modes|✅ Complete|
|CAR User Guide|✅ Complete|
|GitHub Release workflow|📋 PLANNED|
```

---

# PHASE 3: PROVENANCE & TIMESTAMP ARCHITECTURE ✅ COMPLETE

- ✅ Provenance schema and manager
    
- ✅ `created` field optional in concepts
    
- ✅ Auto-provenance on concept generation
    
- ✅ Same content = same CID across machines
    
- ✅ GUI displays provenance sticky notes
    
- ✅ Version history display
    
- ✅ Persistent sidebar navigation
    
- ✅ Client-side live preview (air-gap compatible)
    

---

# PHASE 4: CRYPTOGRAPHIC IDENTITY & VERIFICATION
```text
|Sub-phase|Status|
|---|---|
|4A: USB Key Infrastructure|📋 PLANNED|
|4B: ORCID Integration|⏸️ PENDING APPROVAL|
|4C: Author Identity Display|✅ COMPLETE|
|4D: Verification Chain|✅ COMPLETE|
|4E: Supersedence Tracking|📋 PLANNED|
```

---

# PHASE 5: RELATIONSHIP MAPPING & MYCELIUM NAVIGATION

## Sub-phase 5A-5D ✅ COMPLETE

- ✅ Bidirectional relationship indexer
    
- ✅ Mycelium Map page in GUI
    
- ✅ Interactive graph (Cytoscape.js)
    
- ✅ Node color-coding by domain
    
- ✅ Edge type color-coding and labels
    
- ✅ Click-to-view concept details
    
- ✅ Easter eggs (Cadmies, Verve)
    

## Sub-phase 5E: Mycelium Map Enhancements 📋 PLANNED
```text
|Feature|Status|
|---|---|
|Random Walk button|📋 PLANNED|
|Concept birth announcement|📋 PLANNED|
|Stale concept warning (30+ days)|📋 PLANNED|
|Map legend (color-coded key)|📋 PLANNED|
|Concept preview on hover|📋 PLANNED|
|Keyboard shortcuts|📋 PLANNED|
|Export provenance as plain English|📋 PLANNED|
```

**Default mode for 5E:** All enhancements OFF by default. User toggles ON as desired.

## Sub-phase 5F: Auditory Mycelium (Spatial Audio) 📋 PLANNED

- Domain-to-frequency mapping (Physics: 80Hz, Philosophy: 440Hz, etc.)
    
- 3D spatial audio (Web Audio API + Three.js)
    
- Nodes hum at frequencies based on domain
    
- Harmonic interference beats between connected concepts
    
- Toggle ON/OFF — **Default: OFF**
    

## Sub-phase 5G: Visual Breathing 📋 PLANNED

- Nodes pulse at rates based on verification/connectedness
    
- **Default: OFF**
    

## Sub-phase 5H: Accessibility - Blind Navigation 📋 PLANNED

- Keyboard navigation (Tab, arrow keys)
    
- Web Speech API integration
    
- Screen reader optimized
    
- High contrast mode toggle
    
- Font size controls
    
- **Default: OFF (but persists if user enables)**
    

## Sub-phase 5I: Cosmic Mycelium (NASA Audio Integration) 📋 PLANNED

- Embedded NASA/ESA cosmic sounds
    
- "Cosmic Playback" button on astronomy concepts
    
- Requires optional sound pack download (Tier 2 caching)
    
- **Default: OFF**
    

## Sub-phase 5J: Future Extensions 🔮 FUTURE

- 3D Matrix mode (VR/Oculus vision)
    
- Search functionality
    
- Path finding
    
- Centrality scoring
    
- Export graph as PNG/SVG
    

---

# PHASE 6: SCIENTIFIC CONCEPT MIGRATION 🟡 READY
```text
|Directory|Status|
|---|---|
|`literature_review_dna/`|🟡 READY TO REVIEW|
|`methodology_chain/`|🟡 READY|
|`peer_review_templates/`|🟡 READY|
```

---

# PHASE 7: AUTONOMOUS CONCEPT MINING 🟡 READY

- Pattern miner (heuristic-based, no LLM) — ready to port
    
- LLM pipeline (Ollama/GPT4All) — needs investigation
    
- GUI "Paste & Mine" button — to be added
    

---

# PHASE 8: LLM/RAG/HOG SYSTEM INTEGRATION 🟡 PARTIAL
```text
|Task|Priority|
|---|---|
|Connect CADMIES to Ollama API|🟡 High|
|Import HOG concepts into blockstore|✅ COMPLETE|
|LLM for natural language queries|🟡 Medium|
|LLM for multi-level explanations (PhD → Teenager)|🟡 High|
|LLM for tone adaptation|🟡 Medium|
|Cross-validation with LLM knowledge|🟡 Medium|
```

**Note:** LLM runs **LOCALLY** — no internet required for core LLM functions. Internet only needed for external updates (news, fresh research, GitHub sync, sound pack downloads).

---

# PHASE 9: GUI ENHANCEMENTS 📋 PLANNED

## 9A: Agent Integration (Willie the Librarian)

- "🧠 Analyze with Agent" button on concept cards
    
- Checkbox selection for multi-concept analysis
    
- Willie avatar with dynamic expressions (idle, working, happy, angry)
    
- Willie speech bubbles with contextual messages
    
- **Gradual engagement:** Willie starts with "Aye, I'm Willie. Let me know if I can be of help." Becomes more talkative as user interacts more.
    

## 9B: Progressive Disclosure (The Onion Layers)

- "Peel" button for deeper layers (Catalog → Summary → Standard → Deep dive → Expert)
    
- Breadcrumb trail for current layer depth
    
- "Back to Surface" button
    

## 9C: CAR File Management

- "📦 Export to CAR" on concept cards
    
- "📦 Export Selected" for multi-concept
    
- "📥 Import CAR File" in sidebar
    
- Import modal with file picker, CID preview, conflict detection
    
- **Local CAR ops = always available. Remote CAR ops (GitHub) = require connection.**
    

## 9D: Enhanced Concept Viewing

- Formula field with LaTeX rendering (MathJax/KaTeX)
    
- Proofs/Evidence section with collapsible citations
    
- Difficulty level tabs (Beginner/Intermediate/Expert)
    

## 9E: Navigation & UX Improvements

- Home/Back/Forward buttons on all pages
    
- Keyboard shortcuts cheat sheet (`?`)
    
- Recently viewed concepts sidebar
    
- Bookmark/favorite concept feature
    
- Concept tagging (user-defined, local storage)
    

## 9F: Provenance & Audit Enhancements

- Provenance Timeline Viewer
    
- Audit log browser with search/filter
    
- Verification badges (🔴 🟡 🟢 💎) on concept cards
    

## 9G: Mycelium Map Enhancements

- "Analyze from Map" button
    
- Node search with auto-centering
    
- Path finding modal
    
- Centrality highlighting
    
- Export graph as PNG/SVG
    

## 9H: Willie Personality & Easter Eggs

**Core Willie Personality:**

- Scottish groundskeeper energy, but EDUCATED (librarian)
    
- Protective, competent, slightly suspicious of unproven tech
    
- Warm underneath but doesn't show it until trust is earned
    
- Knows his shit. And his haggis.
    

**Features:**

- **"What Willie is saying, but in English:"** button next to speech bubble
    
    - Not a "translate" (no judgment). A clarification. Willie's gift to the user.
        
    - Willie knows half the world can't understand him. He's not offended. He's practical.
        
    - Tooltip hover: _"Willie knows you're trying. Here's some help."_
        
- Willie mood states (Happy, Angry, Confused, Proud)
    
- Hidden Willie interactions (click avatar for random quote)
    
- Easter egg: Never using translate button for 100+ interactions unlocks hidden voice line
    

## 9I: Accessibility & Air-Gap Features

**Connection Monitor with Capability Registry:**

- Monitors internet connection AND local capability availability (sound pack, 3D assets, etc.)
    
- Three tiers of functionality:
    
    - **Tier 1:** Always works (core CADMIES + local LLM + basic visuals)
        
    - **Tier 2:** Works if cached locally (cosmic audio, high-res assets — fallback gracefully)
        
    - **Tier 3:** Requires connection (news, fresh research, GitHub sync, remote CAR ops)
        
- Internet loss message: _"Internet connection lost. Live updates paused. CADMIES continues fully operational with local knowledge and LLM. Reconnect when ready."_
    
- User must acknowledge message once. If they click away, message dismisses but flag is set. System knows they saw it.
    
- No feature trapping. No repeated nagging.
    

**Accessibility:**

- Keyboard navigation for blind/low-vision users
    
- Web Speech API for screen reader support
    
- High contrast mode toggle
    
- Font size controls with spoken confirmation
    
- 100% air-gap compatibility (local resources only)
    

---

# PHASE 10: DISTRIBUTION 📋 PLANNED

- Publish CAR files as GitHub Releases
    
- Document IPFS integration
    
- Create video tutorial
    

---

# PHASE 11: CAR ENHANCEMENTS 📋 PLANNED

|Feature|Priority|
|---|---|
|Manifest Block|🟢 Low|
|Dependency Resolver|🟢 Low|
|Size Optimizer (zstd compression)|🟡 Medium|
|CAR Validation Levels|🟡 Medium|
|Security Profile|🔴 Low|
|Ecosystem Templates|🔴 Low|
|Runtime Loading Protocol|🔴 Low|
|10MB Size Guideline|🟢 Low|

---

# PHASE 12: AGENT ECOSYSTEM PACKAGING 🔮 FUTURE

- Agent CAR Export (bundle multiple agents)
    
- Runtime + Agents together
    
- Dependency resolution for all agent CIDs
    
- Self-contained ecosystems <10MB
    

---

# PHASE 13: DISTRIBUTION ECOSYSTEM 📋 PLANNED

|Feature|Priority|
|---|---|
|CID Registry|🟡 Medium|
|Reputation System|🟡 Medium|
|Discovery Service|🔮 Future|
|Capability-Based Access|🔮 Future|
|Federation Protocol|🔮 Future|
|Delta Updates|🔮 Future|
|P2P Distribution|🔮 Future|

---

# PHASE 14: RUNTIME INTERPRETER 📋 PLANNED

|Sub-phase|Priority|
|---|---|
|14A: CAR Loader for agent ecosystems|🟡 Medium|
|14B: Graph Walker|🟡 Medium|
|14C: Full Agent Executor|🟡 Medium|
|14D: Memory Manager|🔮 Future|
|14E: Activation Propagation|🔮 Future|

---

# PHASE 15: LLM BRIDGE INTERFACE 🟡 READY

|Sub-phase|Priority|
|---|---|
|15A: Connect CADMIES to Ollama API|🟡 High|
|15B: Natural language queries|🟡 High|
|15C: Multi-level explanations|🟡 High|
|15D: Tone adaptation|🟡 Medium|
|15E: Cross-validation|🟡 Medium|
|15F: Concept discovery via conversation|🟢 Low|

**Critical Note:** LLM runs **LOCALLY** (Mistral 7B or equivalent). No internet required for LLM function. Internet only for external data sources.

---

# PHASE 16: INFRASTRUCTURE & CONTAINERIZATION ✅ EXISTING

- Fedora Silverblue, Podman 5.7.0, Flatpak ecosystem
    
- Toolbox environments, 3-tier backup system
    

---

# PHASE 17: EVOLUTION & LEARNING MECHANISMS 🔮 FUTURE

- Agent Parameter Mutation Engine
    
- Connection Graph Evolution
    
- Experience Memory System
    
- Reinforcement Learning Integration
    
- Cross-Ecosystem Agent Transfer
    
- Symbiotic Relationship Formation
    
- Genetic Algorithm Framework
    

---

# PHASE 18: FUTURE VISIONS (Not Yet Roadmapped)

**VR/Oculus Integration:**

- Immersive mycelium navigation in 3D space
    
- Spatial audio with harmonic interference beats moving in 3D
    
- Physics concepts humming at 80Hz from left, Philosophy at 440Hz from right
    
- Black hole howl from below (like standing on event horizon)
    
- Willie's voice over the shoulder, not from a speaker
    
- Entire mycelium lives on headset (air-gapped)
    

**Willie Origin Story Document:**

- In-universe explanation of how a Scottish groundskeeper became a digital librarian
    
- Flavor text for the docs. Because why not?
    

---

# CORE AXIOMS & NOBLE TRUTHS

|#|Truth|
|---|---|
|0|"Only scale is the difference"|
|1|"To understand one is to understand all"|
|2|"To navigate one is to navigate all"|
|3|"A CID is a finger pointing at the moon"|
|4|"The mycelium is Indra's Net"|
|5|"Provenance is karma"|
|6|"Every concept contains the entire graph"|
|7|"If the blind can hear the mycelium, then the mycelium is real"|

---

# QUICK REFERENCE: WHAT'S READY TO DO RIGHT NOW

|Action|Time Estimate|
|---|---|
|Review genomics concepts|30 min|
|Port pattern-based concept miner|1-2 hours|
|Connect CADMIES to Ollama|1-2 hours|
|Add multi-level LLM explanations|2-3 hours|
|Add CAR manifest block|30 min|
|Add CAR validation levels|1 hour|

---

**End of Roadmap.** 🌱

_"Aye, that's the shape of it. Now get back to work — or don't. I'm no' yer mum."_ — Willie

