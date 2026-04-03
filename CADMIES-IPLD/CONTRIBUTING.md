First off, thank you for considering contributing to CADMIES! 🧑🏽‍🌾🍄

## Quick Navigation

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Priority Tasks](#priority-tasks)
- [How to Contribute](#how-to-contribute)
- [Style Guide](#style-guide)
- [Questions](#questions)

## Code of Conduct

This project adheres to the principles of ethical knowledge sharing (AGPLv3 + Commons Clause). We expect all contributors to:
- Respect the Commons Clause (no commercial exploitation without reciprocity)
- Share improvements back to the community
- Prioritize educational and research purposes
- Be excellent to each other

## Getting Started

### Prerequisites
```bash
pip install dag-cbor multiformats nicegui pydantic python-dotenv aiofiles
```
Clone and Setup
bash

git clone https://github.com/Hieros-CADMIES/CADMIES.git
cd CADMIES/CADMIES-IPLD
python tools/core/cid_generator_v1_1_0.py

Run the GUI
bash

cd cadmies-gui
python gui_main.py
# Open http://localhost:8081

Development Environment

GitHub Codespaces recommended - one-click environment:

    Click Code → Codespaces → Create codespace on main

    All dependencies pre-installed

    Ready to code immediately

Local development:

    Python 3.9+

    Linux/Mac/Windows (WSL2 recommended for Windows)

Project Structure
text

CADMIES-IPLD/
├── cadmies-gui/              # Web interface (NiceGUI)
│   ├── ui/pages/             # Dashboard, Add Concept, Browse, Audit, Mycelium Map
│   ├── gui_tools/            # CID generator and CBOR reader wrappers
│   └── gui_main.py           # Main entry point
├── tools/core/               # Core CLI tools
│   ├── cid_generator_v1_1_0.py
│   ├── cbor_reader.py
│   ├── provenance_manager.py
│   └── paths.py
├── store/                    # IPLD block storage
│   ├── blocks/               # CBOR files (CID-named)
│   ├── index/                # human_id → CID mappings
│   └── logs/                 # operations.jsonl
├── source_concepts/          # Human-readable JSON sources
└── specs/                    # CID Structure Specification

Priority Tasks

We maintain a live roadmap. Here are the current priorities:
🔜 HIGH PRIORITY (Help Wanted)
Task	Location	Difficulty	Estimated Time
CAR File System	tools/core/	Intermediate	2-4 hours
- Build export_to_car.py			
- Build import_from_car.py			
- GitHub Release workflow	.github/workflows/		
Add Formula Field to GUI	cadmies-gui/ui/pages/add_concept.py	Beginner	1 hour
Add Proofs Section	cadmies-gui/ui/pages/add_concept.py	Intermediate	2 hours
Fix Preview Pane	cadmies-gui/ui/pages/add_concept.py	Beginner	30 min
Add Missing Concept Types	cadmies-gui/ui/pages/add_concept.py	Beginner	15 min
📋 PLANNED (Good for First-Time Contributors)
Task	Location	Difficulty
Add Home/Back buttons	cadmies-gui/ui/pages/*.py	Beginner
Provenance timeline viewer	cadmies-gui/ui/pages/audit.py	Intermediate
Export graph as PNG/SVG	mycelium_map.html	Intermediate
Add tooltips everywhere	cadmies-gui/ui/pages/	Beginner
🚀 ADVANCED (Experienced Contributors)
Task	Location	Difficulty
3D Matrix mode for Mycelium Map	mycelium_map.html	Advanced
Path finding between concepts	mycelium_map.html	Advanced
USB Key Infrastructure	tools/core/key_manager.py	Advanced
ORCID Integration	tools/core/orcid_stamper.py	Advanced
How to Contribute
1. Claim a Task

    Comment on the issue or open a new one

    Say "I'm working on [task name]"

2. Create a Branch
bash

git checkout -b feature/your-feature-name

3. Make Changes

    Follow style guide below

    Test your changes

    Update documentation if needed

4. Commit and Push
bash

git add .
git commit -m "Add: brief description of what you did"
git push origin feature/your-feature-name

5. Open a Pull Request

    Go to GitHub

    Click "Compare & pull request"

    Describe your changes

    Request review

Style Guide
Python

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

Testing

Before submitting, run:
bash

# Test CID generation
python tools/core/cid_generator_v1_1_0.py

# Test retrieval
python tools/core/cbor_reader.py --list

# Test GUI
cd cadmies-gui
python gui_main.py
# Verify all pages load

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
