A graphical interface for the CADMIES-IPLD system.  
100% local, air-gapped, and ready for your own data.

## Features

- **Dashboard** – System overview, stats, recent activity
- **Add Concept** – Form interface with live preview
- **Browse Library** – Search and view existing concepts
- **Audit Trail** – Complete operation history

## Quick Start

## Navigate to GUI directory (from CADMIES-IPLD root)
```bash
cd cadmies-gui
```

## Install dependencies
```bash
pip install -r requirements.txt
```

## Run the GUI
```bash
python gui_main.py
```
The GUI automatically uses:

    ../store/ for IPLD blocks

    ../tools/core/ for CID generator and CBOR reader
    
## Directory Structure

The GUI expects this structure (configurable via env):
```text
CADMIES-IPLD/
├── store/
│   ├── blocks/           # CBOR files
│   ├── index/            # human_id_to_cid.json
│   └── logs/             # operations.jsonl
├── tools/
│   └── core/
│       ├── cid_generator_v1.1.0.py
│       └── cbor_reader.py
└── cadmies-gui/          # This directory
```

## Usage

Adding a Concept

    Click "Add Concept" in navigation

    Fill in the form (live preview updates)

    Click "Generate CID & Store"

    View the new CID and confirmation

## Browsing Concepts

    Click "Browse Library"

    Search by concept name

    Click "View" on any concept to see details

    Toggle between grid and list views

## Project Structure
```text
gui/
├── gui_main.py              # Application entry point
├── gui_system.py            # CADMIES system detection
├── gui_concept.py           # Data models (Pydantic)
├── gui_tools/               # Core tool wrappers
│   ├── cid_wrapper.py       # Calls cid_generator
│   └── reader_wrapper.py    # Calls cbor_reader
├── ui/                      # UI pages
│   └── pages/
│       ├── dashboard.py
│       ├── add_concept.py
│       ├── browse.py
│       └── audit.py
├── requirements.txt         # Dependencies
├── CONTRIBUTING.md          # Guide for contributors
└── ROADMAP.md               # Planned features
```

## Air-Gap & Security

Current version: 100% air-gapped

    No network connections

    All data stored locally

    No telemetry or analytics

    All dependencies are local Python packages

## Future: Optional secure sharing (sandboxed, user-consent only)

### Configuration

Set CADMIES_TOOLS_PATH environment variable to use a custom location:

export CADMIES_TOOLS_PATH=/absolute/path/to/your/tools/core
```bash
python gui_main.py
```

## Troubleshooting

"CADMIES System Not Found"

    Verify your tools directory exists

    Check that tools/core/store/ exists

    Ensure Python scripts are present

Concept won't add

    All fields are required

    Name will be cleaned (special chars removed)

    Check Python script paths in console output

No audit logs

    First operation creates the log file

    Check store/logs/operations.jsonl

## Contributing
See CONTRIBUTING.md for step-by-step guide on adding new features.

## Roadmap
See ROADMAP.md for planned features and priorities.

## License
AGPLv3 with Commons Clause – see root repository LICENSE file.

