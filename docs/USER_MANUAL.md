---
System: CADMIES-IPLD
Document_ID: CA-2026-050-MANUAL
Version: 1.0.0
Classification: PUBLIC
Author: Digital Intelligence Research Division - Project Hieros
Reviewers: [GUI Lead, System Architect, Documentation Team]
Status: ACTIVE
Created: 2026-02-18
Modified: 2026-02-18
Related_Docs:
  - CA-2026-046-README (Main README)
  - CA-2026-047-GUI-README (GUI Documentation)
  - CA-2026-049-FEATURES (Feature Roadmap)
  - CA-2026-021-GUIDE (Documentation Creation Guide)
---

# IPLD Knowledge Tools - Complete User Manual

## 1.0 What This System Does

A local-first, content-addressed knowledge system that lets you:
- **Store knowledge** with permanent, verifiable addresses (CIDs)
- **Retrieve knowledge** using those addresses or human-readable IDs
- **Structure information** using a standardized schema
- **Create trustworthy** knowledge systems where content can't be silently altered
- **Interact visually** through a web-based graphical interface

## 2.0 Quick Navigation

### 2.1 For New Users
1. **[Quick Start](QUICK_START.md)** - 5-minute setup
2. **[Installation Guide](INSTALLATION.md)** - Detailed setup
3. **[Testing Guide](TESTING_GUIDE.md)** - Verify everything works

### 2.2 For Practical Use
4. **[Use Cases](USE_CASES.md)** - Real-world applications
5. **[Examples Directory](../examples/)** - Ready-to-use examples
6. **[GUI Interface](../cadmies-gui/README.md)** - Web-based graphical interface

### 2.3 For Advanced Users
7. **[Advanced Usage](ADVANCED_USAGE.md)** - Custom schemas, extensions
8. **[API Reference](../src/API_REFERENCE.md)** - Technical details

### 2.4 When Things Go Wrong
9. **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues & solutions

## 3.0 System Architecture Overview

### 3.1 Core Workflow
```text
Your Knowledge → CID Generator → CID (Content ID) → Blockstore
↑                                           ↓
Human ID ←─────────── CBOR Reader ←──── .cbor file
```

### 3.2 Core Components
Component	Location	Purpose
CID Generator	cadmies_demo/cid_generator_v1_1_0.py	Creates CIDs from knowledge concepts
CBOR Reader	cadmies_demo/cbor_reader.py	Reads knowledge by CID or human ID
Universal Schema	schemas/universal_scientific_concept_schema_v1.0.0.json	Standard format for all concepts
GUI Interface	cadmies-gui/	Web-based graphical interface
Atlas Integration	atlas-integration/	Optional network connectivity

### 3.3 Storage Structure

When you use the system, it creates:
```text

blocks/           # .cbor files (your actual knowledge)
index/            # human_id_to_cid.json (human-readable mappings)
logs/             # operations.jsonl (audit history)
```

## 4.0 The 3-Step Workflow

### 4.1 Step 1: Create Knowledge
```bash

python cadmies_demo/cid_generator_v1_1_0.py --concept-file my_knowledge.json
```

What happens:

    Your concept is validated against the universal schema

    A deterministic CID is generated

    The concept is stored in blocks/ as a .cbor file

    An entry is added to index/human_id_to_cid.json

    The operation is logged in logs/operations.jsonl

### 4.2 Step 2: Retrieve Knowledge
```bash

# By CID
python cadmies_demo/cbor_reader.py bafyrei...

# By human ID
python cadmies_demo/cbor_reader.py my_concept_id

# List all concepts
python cadmies_demo/cbor_reader.py --list
```

### 4.3 Step 3: Verify & Share

    Same content always produces same CID — Verification is built-in

    Share CIDs for verifiable knowledge sharing

    Build knowledge graphs using relationships between concepts

    Audit trail tracks all operations

## 5.0 Graphical Interface

### 5.1 Overview

CADMIES includes a web-based GUI for easier interaction, located in cadmies-gui/.

### 5.2 GUI Features
Page	Description
Dashboard	System overview, stats, recent activity
Add Concept	Form interface with live preview
Browse Library	Search and view existing concepts
Audit Trail	Complete operation history

### 5.3 Quick Start with GUI
```bash

# Navigate to GUI directory
cd cadmies-gui

# Install dependencies
pip install -r requirements.txt

# Run the GUI
python gui_main.py
```

Your browser will open to http://localhost:8081

See GUI Documentation for complete details.

## 6.0 Learning Pathways

### 6.1 Path A: Casual User (30 minutes)

    Complete Quick Start

    Try one example concept from examples/

    Generate and read back a CID

    Explore concepts via GUI

### 6.2 Path B: Educator/Researcher (2 hours)

    Complete Installation Guide

    Explore Use Cases

    Adapt templates for your needs

    Run verification tests

    Use GUI for classroom demonstrations

### 6.3 Path C: Developer (4+ hours)

    Full installation with testing

    Examine schema and extensions

    Review Advanced Usage

    Contribute improvements

    Extend GUI with new pages (see cadmies-gui/CONTRIBUTING.md)

## 7.0 Project Structure
```text

CADMIES/
├── cadmies-gui/                 # Web interface
│   ├── gui_main.py
│   ├── gui_system.py
│   ├── gui_concept.py
│   ├── gui_tools/
│   ├── ui/pages/
│   ├── README.md
│   ├── CONTRIBUTING.md
│   └── ROADMAP.md
├── cadmies_demo/                 # Core tools package
│   ├── cid_generator_v1_1_0.py
│   ├── cbor_reader.py
│   └── __init__.py
├── docs/                         # User documentation
│   ├── INSTALLATION.md
│   ├── QUICK_START.md
│   ├── TESTING_GUIDE.md
│   └── USER_MANUAL.md            # This file
├── examples/                     # Example concepts
│   └── conservation_of_energy.json
├── schemas/                      # JSON schemas
│   └── universal_scientific_concept_schema_v1.0.0.json
├── specs/                        # Formal specifications
│   └── cid_structure_specification_v2.0.0.md
├── tests/                        # Test suite
│   ├── test_core_functionality.py
│   ├── test_determinism.py
│   └── test_read_write_cycle.py
├── atlas-integration/            # Optional network layer
├── blocks/                       # Stored concepts (created on use)
├── index/                        # Human-readable mappings
├── logs/                         # Operation history
├── LICENSE                        # AGPLv3 + Commons Clause (software)
├── DOCS-LICENSE                    # CC BY-NC-SA 4.0 (documentation)
├── README.md                       # Main project README
└── [historical PDFs]               # Project manifests and assessments
```

## 8.0 Evidence Management Protocol

### 8.1 Capturing Command Outputs

When documenting system behavior or issues:
```bash

# Capture with timestamp and context
{
  echo "=== COMMAND: python cbor_reader.py --list"
  echo "=== TIMESTAMP: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "=== CONTEXT: Verifying concept list"
  echo ""
  python cbor_reader.py --list
} > evidence/commands/2026-02-18_concept-list.txt
```

### 8.2 Evidence Directory Structure
```text

evidence/
├── AUDIT-YYYY-NNN/               # Audit-specific evidence
│   ├── commands/                  # Command outputs
│   ├── screenshots/               # GUI/system screenshots
│   └── logs/                      # Referenced log excerpts
└── README.md                       # Evidence index
```

## 9.0 Quality Assurance Checklist

### 9.1 Pre-Release Checklist

    Metadata complete in all documents

    Version numbers incremented appropriately

    All code examples tested

    GUI runs without errors

    Core tools generate correct CIDs

    Evidence referenced correctly

    All links valid

    Spell check completed

    License notices present

### 9.2 PDF Generation Checklist (if exporting)

    Table of contents generated

    Page numbers consistent

    Code formatting preserved

    Diagrams correctly positioned

## 10.0 Troubleshooting

### 10.1 Common Issues
Issue	Solution
pandoc: command not found	Install pandoc or use toolbox environment
GUI won't start	Verify dependencies: pip install -r cadmies-gui/requirements.txt
CID generation fails	Check concept validates against schema
No audit logs	First operation creates the log file
GUI shows "System Not Found"	Verify CADMIES tools path or set CADMIES_TOOLS_PATH

### 10.2 Verification Commands
```bash

Test CID generation
python cadmies_demo/cid_generator_v1_1_0.py --test

# Verify determinism
python cadmies_demo/cid_generator_v1_1_0.py --same-input-twice

# Check system integrity
python tests/test_core_functionality.py
```

## 11.0 Ethical Use & Licensing

### 11.1 Software License (Code)

AGPLv3 with Commons Clause

    Free for: Education, research, personal use, open source projects

    Free for: Internal company use

    Requires permission for: Commercial SaaS, proprietary AI training, selling access

### 11.2 Documentation License (Manuals, Schemas, Specs)

CC BY-NC-SA 4.0

    Free to share and adapt

     Must give credit

    Must share alike

    No commercial use

### 11.3 Commercial Inquiries

Contact: hieroscadmies@proton.me

## 12.0 Getting Help

    Check Troubleshooting first

    Review examples in /examples/ directory

    Examine test files to see expected behavior

    Try the GUI for visual interaction

    Email questions to: hieroscadmies@proton.me

## 13.0 Next Steps

    Install - Get the system running

    Test - Verify everything works

    Learn - Understand the workflow

    Apply - Use for your projects

    Extend - Customize for your needs

    Share - Contribute improvements

    Visualize - Try the GUI


## APPENDIX A: Version History
Version	Date	Author	Changes
1.0.0	2026-02-18	DIRD	Initial public release; consolidated all user documentation into single manual with GUI integration

## APPENDIX B: Document ID Reference
Document	ID	Location
Main README	CA-2026-046-README	/README.md
GUI README	CA-2026-047-GUI-README	/cadmies-gui/README.md
Feature Roadmap	CA-2026-049-FEATURES	/cadmies-gui/ROADMAP.md
User Manual	CA-2026-050-MANUAL	/docs/USER_MANUAL.md

***"Knowledge should be free to access."***

***Let the mycelium grow!*** 🌱
