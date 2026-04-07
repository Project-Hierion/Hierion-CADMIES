# CADMIES-IPLD

**Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem**

A philosophical and technical framework for content-addressed, scientifically-validated knowledge storage and sharing.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Hieros-CADMIES/CADMIES.git
cd CADMIES/CADMIES-IPLD

# Install dependencies
pip install dag-cbor multiformats

# Generate a concept
python tools/core/cid_generator_v1_1_0.py --concept-file source_concepts/example.json

# Read a concept
python tools/core/cbor_reader.py natural_selection

What is CADMIES?

CADMIES is a system for storing scientific and philosophical concepts as immutable, content-addressed blocks (IPLD). Each concept has a permanent CID (Content IDentifier) that changes if and only if the content changes.

Key principles:

    Content-addressing – Same content = same CID, always

    Provenance tracking – Every concept has a verifiable creation record

    Scientific validation – Four-tier validation system (Basic → Standard → Rigorous → Strict)

    Verification – Scientists can verify concepts using ORCID

    CAR sharing – Export/import concepts as single files

Core Concepts
Concept	Description
CID	Content Identifier – permanent, content-addressed hash
Block	A single concept or provenance record stored as CBOR
Provenance	Creation, verification, and supersedence records
Mycelium	The network of interconnected concepts
CAR file	A bundle of blocks for sharing
Directory Structure
```text
CADMIES-IPLD/
├── README.md                      # This file
├── CAR_USER_GUIDE.md              # Complete CAR export/import guide
├── store/
│   ├── blocks/                    # CBOR blocks (concepts + provenance)
│   └── index/                     # human_id → CID mappings
├── tools/
│   ├── core/                      # Core tools
│   │   ├── cid_generator_v1_1_0.py
│   │   ├── cbor_reader.py
│   │   ├── provenance_manager.py
│   │   ├── verification_manager.py
│   │   └── paths.py
│   ├── car_utils.py               # CAR reader/writer
│   ├── export_to_car.py           # Export concepts to CAR
│   ├── import_from_car.py         # Import CAR files
│   └── import_from_github.py      # Download and import from GitHub
├── agents/                        # Executable agents
│   └── code/                      # Agent implementations
└── source_concepts/               # JSON concept definitions
```

CAR File System (Sharing Concepts)

CADMIES uses CAR (Content Addressable Archive) files to share concepts between instances. A CAR file bundles one or more concepts with their provenance into a single file.
Quick Export/Import
bash

# Export a single concept
python tools/export_to_car.py natural_selection --output share.car

# Import a CAR file
python tools/import_from_car.py share.car

# Export everything (backup)
python tools/export_to_car.py --all --output full_backup.car

Verification Workflow

Scientists can verify concepts using ORCID and send back a CAR file:
bash

# Export a verified concept as CAR
python tools/core/verification_manager.py --export-verification \
  --concept-cid <CID> \
  --verifier-key "scientist@example.com" \
  --source orcid \
  --output verified.car

# Preview verification without importing
python tools/import_from_car.py verified.car --verify-only

# Import verification
python tools/import_from_car.py verified.car

Import from GitHub
bash

python tools/import_from_github.py --url https://github.com/.../concept.car

📖 Complete instructions: See CAR_USER_GUIDE.md
Verification Badges
Badge	Level	Meaning
🔴	0	Unverified
🟡	1	Self-verified
🟢	2	Verified (ORCID or institution)
💎	3	Highly verified (2+ ORCID or ORCID+institution)
Tools
Tool	Purpose
cid_generator_v1_1_0.py	Generate CID from JSON concept
cbor_reader.py	Read concept by CID or human_id
provenance_manager.py	Create and query provenance records
verification_manager.py	Add verification statements, check status
export_to_car.py	Export concepts to CAR files
import_from_car.py	Import CAR files into mycelium
import_from_github.py	Download and import from GitHub
car_utils.py	Low-level CAR reader/writer
Dependencies
bash

pip install dag-cbor multiformats

No other external dependencies. Air-gap compatible.
License

AGPLv3 with Commons Clause

Free for:

    Individual learning and research

    Academic institutions

    Non-profit organizations

    Open source projects

    Personal knowledge management

Commercial use requires permission. See LICENSE for details.

Contact: hieroscadmies@proton.me
Philosophical Note

    "A fortress is not measured by the height of its walls, but by the integrity of its foundations and the vigilance of its guardians."

CADMIES is a digital mycorrhiza – a network where knowledge grows organically, distributed across independent colonies. No single point of failure. No central authority. Just the mycelium. And you.

The fortress stands. The mycelium grows. 🌱