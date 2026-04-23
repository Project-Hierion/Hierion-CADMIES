# CADMIES GUI

A graphical interface for the CADMIES-IPLD system.  
100% local, air-gapped, and ready for your own data.

## Features

- **Dashboard** – System overview, stats, recent activity, hidden easter egg (click the 🌱)
- **Add Concept** – Form interface with client-side live preview (updates when you click out of fields)
- **Browse Library** – Search and view existing concepts with provenance sticky notes
- **Audit Trail** – Complete operation history with timeline
- **Mycelium Map** – Interactive knowledge graph visualization (173+ nodes, 160+ edges)

## Quick Start

### Navigate to GUI directory (from CADMIES-IPLD root)
```bash
cd cadmies-gui
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the GUI
```bash
python gui_main.py
```

The GUI automatically uses:
- `../store/` for IPLD blocks
- `../tools/core/` for CID generator and CBOR reader

## First-Time Setup

If this is a fresh clone, you'll only have the 2 seed blocks. Import the full mycelium first:

```bash
# From the CADMIES-IPLD root directory
python tools/import_from_github.py --url https://github.com/Hieros-CADMIES/CADMIES/releases/download/v0.2.0-reader-capability/full_mycelium_v0.2.0.car
```

Then launch the GUI to browse 50+ interconnected concepts.

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
│       ├── cid_generator_v1_1_0.py
│       └── cbor_reader.py
├── mycelium_map.html     # Generated knowledge graph
└── cadmies-gui/          # This directory
```

## Usage

### Adding a Concept
1. Click "Add Concept" in the sidebar navigation
2. Fill in the form:
   - **Concept Name** – Will be converted to snake_case automatically
   - **Concept Type** – Select from dropdown
   - **Domain** – Select from dropdown
   - **Subdomain** – Free text
   - **Description** – The core definition
3. **Live Preview** – Updates automatically when you click out of each field (air-gap compatible)
4. Click "Generate CID & Store"
5. View the new CID and confirmation dialog

### Browsing Concepts
1. Click "Browse Library" in the sidebar
2. Search by concept name
3. Click "View" on any concept to see details including:
   - Full definition
   - Provenance sticky notes (who created it, when)
   - Version history (supersedes links)
   - Relationships, proofs, and difficulty levels
4. Toggle between grid and list views

### Mycelium Map (Knowledge Graph)
1. Click "Mycelium Map" in the sidebar
2. Explore the interactive graph:
   - **Nodes** = concepts (color-coded by domain)
   - **Edges** = relationships (builds_upon, relates_to, specializes, contradicts)
   - Click any node to see concept name
   - Zoom and drag to navigate
3. **Easter egg:** Type `cadmies` anywhere on the map to activate a special visual tribute

### Dashboard Easter Egg
Click the 🌱 seedling next to "CADMIES Dashboard" for a bittersweet surprise.

## Project Structure
```text
gui/
├── gui_main.py              # Application entry point (with persistent sidebar)
├── gui_system.py            # CADMIES system detection
├── gui_concept.py           # Data models (Pydantic)
├── gui_tools/               # Core tool wrappers
│   ├── cid_wrapper.py       # Calls cid_generator
│   └── reader_wrapper.py    # Calls cbor_reader
├── ui/                      # UI pages
│   └── pages/
│       ├── dashboard.py     # Dashboard with easter egg
│       ├── add_concept.py   # Form with client-side preview
│       ├── browse.py        # Concept library
│       ├── audit.py         # Operation timeline
│       └── mycelium_map.py  # Knowledge graph (static serving)
├── requirements.txt         # Dependencies
├── CONTRIBUTING.md          # Guide for contributors
└── ROADMAP.md               # Planned features
```

## Persistent Sidebar Navigation

The GUI features a persistent sidebar on ALL pages:
- 🏠 **Home** – Landing page with welcome message
- 📊 **Dashboard** – System overview
- ➕ **Add Concept** – Create new concepts
- 📚 **Browse Library** – View existing concepts
- 📋 **Audit Trail** – Operation history
- 🕸️ **Mycelium Map** – Knowledge graph visualization

## Air-Gap & Security

**Current version: 100% air-gapped**
- No network connections (except optional mycelium map CDN for Cytoscape.js)
- All data stored locally
- No telemetry or analytics
- Live preview uses client-side JavaScript (no server communication)

**Future:** Optional secure sharing (sandboxed, user-consent only)

## Configuration

Set `CADMIES_TOOLS_PATH` environment variable to use a custom location:
```bash
export CADMIES_TOOLS_PATH=/absolute/path/to/your/tools/core
python gui_main.py
```

## Troubleshooting

### "CADMIES System Not Found"
- Verify your tools directory exists
- Check that `tools/core/store/` exists
- Ensure Python scripts are present

### Concept won't add
- All fields are required
- Name will be cleaned (special chars removed)
- Check Python script paths in console output

### Preview not updating
- Preview updates when you click out of a field (not while typing)
- This is intentional for air-gap compatibility

### No audit logs
- First operation creates the log file
- Check `store/logs/operations.jsonl`

### Mycelium Map not loading
- Ensure `mycelium_map.html` exists in the CADMIES-IPLD root
- Run the relationship extraction script to generate it

### Empty library after fresh clone
- The clone includes only 2 seed blocks
- Run the import command in **First-Time Setup** above to get the full 50+ concepts

## Contributing

See `CONTRIBUTING.md` for step-by-step guide on adding new features.

## Roadmap

See `ROADMAP.md` for planned features and priorities.

## License

AGPLv3 with Commons Clause – see root repository LICENSE file.

🌱 Let the mycelium grow!
