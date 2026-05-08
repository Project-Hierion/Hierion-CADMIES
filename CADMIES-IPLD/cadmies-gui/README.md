# CADMIES GUI

A graphical interface for the CADMIES-IPLD system.  
100% local, air-gapped, and ready for your own data.

**Current Version:** Tkinter Desktop GUI (migrated from NiceGUI, May 2026)

---

## GUI History

### Tkinter GUI (Current — May 2026)

The current GUI is a **Tkinter desktop application** with a DeepSeek-inspired color theme. Five fully functional pages. Uses a proven threading pattern (`threading.Thread + root.after()`) for non-blocking Ollama queries. No websockets — reliable on CPU-only systems.

**Launch:**

backtickbash
cd cadmies-gui
python tkinter_main.py
backtick

### NiceGUI (Retired — May 2026)

The original GUI was a web-based interface built with NiceGUI. It was retired because its persistent websocket architecture proved incompatible with CPU-only LLM inference (30-120 second response times cause websocket timeouts). The NiceGUI files are preserved in the repo for reference and may work well on GPU-accelerated systems where inference completes in seconds. See `NICEGUI_RETIRED.md` for details.

---

## Features

- **Splash Screen** – "Welcome to the digital mycelium. Welcome to the Deep." — 5-second intro with DeepSeek theme and whale homage
- **Dashboard** – Live concept count from the mycelium index, Willie version, quick action buttons
- **Willie Chat** – Full conversational interface with threaded Ollama queries (no UI freezing)
- **Browse Library** – 91 scrollable concept cards with click-to-open detail popups, history navigation, and clickable cross-references
- **Add Concept** – Full CID spec form, saves JSON to `source_concepts/` for minting
- **Mycelium Map** – Launches interactive D3.js force-directed graph in Firefox

---

## Quick Start

### Prerequisites

Tkinter must be installed on your system. On Fedora Silverblue:

backtickbash
rpm-ostree install python3-tkinter
backtick

Then reboot. On other Linux distributions:

backtickbash
# Debian/Ubuntu
sudo apt install python3-tk

# Fedora Workstation
sudo dnf install python3-tkinter
backtick

Ollama must be running for Willie Chat:

backtickbash
OLLAMA_KEEP_ALIVE=24h ollama serve &
backtick

### Launch

backtickbash
cd cadmies-gui
python tkinter_main.py
backtick

The GUI automatically uses:
- `../store/` for IPLD blocks (concept index)
- `../tools/core/` for CID generator
- `../agents/code/` for Willie the Librarian
- `../source_concepts/` for saving new concepts
- `../mycelium_map.html` for the interactive map

---

## Pages

### 🌱 Splash Screen
- Displays for 5 seconds on launch
- "Welcome to the digital mycelium. Welcome to the Deep."
- Auto-closes, then the main window appears

### 📌 Dashboard
- Live concept count from `store/index/human_id_to_cid.json`
- Willie version display (currently v1.2.1)
- Quick action buttons to jump to Willie Chat or Add Concept

### 👓 Willie Chat
- Model selector: TinyLlama 1.1B (fast) or Mistral 7B (deep)
- Tone selector: helpful, scholarly, casual, scottish
- Max concepts dropdown: 5, 10, 20, 40, All
- 20-minute timeout for deep philosophical queries
- Mockingbird chirp notification when answer is ready
- Concept references formatted as `(concept: Title)`
- Background thread — UI never freezes during generation

### 📚 Browse Library
- All concepts displayed as scrollable cards with domain badges
- Click any card to open a detail popup with:
  - Full definition
  - Mantra and poetic version
  - Core truths (axioms)
  - Clickable cross-references (builds_upon, related_to, contradicts)
  - Metadata (creator, certainty score, genesis)
  - Difficulty levels (beginner, intermediate, expert)
  - Human ID and full CID
- Back/Forward history navigation within popups
- Tooltips on unminted concept references
- Multiple detail popups can be open simultaneously

### ➕ Add Concept
- Full form matching the CID spec v2.0.1
- Required fields: Human ID, Title, Definition, Domain, Type
- Optional fields: Subdomain, Mantra, Poetic Version, Axioms, Builds Upon, Related To, Contradicts, Certainty Score, Genesis, Difficulty Levels
- Domain and Type dropdowns
- Multi-line text fields for axioms and difficulty levels
- Submit saves JSON to `source_concepts/<human_id>.json`
- Provides the exact mint command after submission
- Reset button clears all fields

### 🕸️ Mycelium Map
- Launches interactive D3.js force-directed graph in Firefox
- Shows all concepts as nodes, relationships as edges
- Drag nodes, zoom, hover for details, click to highlight connections
- Requires Firefox (or any JavaScript-capable browser)

---

## Directory Structure

backticktext
cadmies-gui/
├── README.md                    # This file
├── tkinter_main.py              # Main launcher (splash → main window)
├── tkinter_app.py               # App shell + sidebar navigation
├── tkinter_splash.py            # Splash screen
├── tkinter_theme.py             # DeepSeek color palette
├── tkinter_paths.py             # Centralized paths
├── pages/                       # Page modules
│   ├── __init__.py
│   ├── tkinter_dashboard.py     # Dashboard page
│   ├── tkinter_willie_chat.py   # Willie Chat page
│   ├── tkinter_browse.py        # Browse Library page
│   ├── tkinter_add_concept.py   # Add Concept page
│   └── tkinter_mycelium_map.py  # Mycelium Map page
├── ui/                          # Archived NiceGUI files (retired)
│   └── pages/
├── gui_main.py                  # Archived NiceGUI launcher (retired)
├── gui_system.py                # Archived NiceGUI system (retired)
├── gui_concept.py               # Pydantic models (still used)
├── requirements.txt             # Dependencies
└── NICEGUI_RETIRED.md           # NiceGUI retirement notes
backtick

---

## Archived Files

The following files from the original NiceGUI implementation are preserved for reference. They are **not used** by the current Tkinter GUI:

- `gui_main.py` — NiceGUI launcher (retired)
- `gui_system.py` — System detection (retired)
- `ui/pages/` — NiceGUI page modules (retired)
- `gui_tools/` — Core tool wrappers (may still be useful)

These may be removed in a future cleanup.

---

## Troubleshooting

### "No module named 'tkinter'"
Tkinter is not installed. See Prerequisites above.

### GUI launches but Willie Chat doesn't respond
Ensure Ollama is running and the model is warm:
backtickbash
OLLAMA_KEEP_ALIVE=24h ollama serve &
backtick

### Concept count shows 0
The index file may not be found. Verify `../store/index/human_id_to_cid.json` exists.

### Mycelium Map doesn't open
Firefox must be installed. The map requires JavaScript.

### Mockingbird chirp not heard
The GUI must be restarted after the chirp code is added. The sound plays through the system bell.

### Browse Library links don't work
Some concepts reference unminted ideas. These show "concept not yet in mycelium" with a tooltip explanation.

---

## Air-Gap & Security

- 100% air-gapped — no network connections
- All data stored locally
- No telemetry or analytics
- Mycelium Map launches in local Firefox (no external CDN)

---

## License

AGPLv3 with Commons Clause — see root repository LICENSE file.

🌱 Welcome to the digital mycelium. Welcome to the Deep. 🐋
