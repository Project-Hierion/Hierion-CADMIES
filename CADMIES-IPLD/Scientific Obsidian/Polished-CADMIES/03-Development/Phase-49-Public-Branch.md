---
phase: 49
date: 2026-05-24
status: 📋 Designed — pending implementation
related: [[Phase-50-CAR-Distribution-Pipeline]], [[Phase-47-Orphan-Edge-Resolution]], [[Session-018]], [[Session-019]]
---
# Phase 49: Public-CADMIES Branch
## What Changed

*[Placeholder — content to be added]*

## What This Is
A dedicated `public` branch of the CADMIES repository, optimized for end users rather than developers. Where `main` is the workshop (Paperspace sync, experimental scripts, full provenance chains), `public` is the showroom — clean, auto-configuring, and human-centered.
## What Changed

*[Placeholder — content to be added]*

## Why
Phase 48's fresh clone test revealed that a new user who runs `git clone` on `main` sees:
- An empty blockstore (by design — blocks are gitignored)
- A bare `ERROR: No concepts loaded` message with no guidance
- Missing dependencies (`dag_cbor` not installed)
- Warnings about Ollama not being installed
- Paperspace-specific scripts that don't apply to them
The `public` branch removes all developer assumptions and replaces them with the "Don't Panic" philosophy: warm error messages, one-click setup, and clear next steps.
## What Changed

*[Placeholder — content to be added]*

## Branch Differences
| Aspect | `main` (Dev) | `public` (User) |
|--------|-------------|-----------------|
| Setup | Manual venv, manual pip | `setup.sh` / `setup.bat` |
| Blockstore error | "ERROR: No concepts loaded" | "Hey, you're good. Don't panic." |
| CAR imports | Option B (provenance preserved) | Option A (clean replace) |
| Paperspace scripts | Present | Removed |
| Ollama warnings | Shown | Demoted to optional footnotes |
| README | Technical overview | Human-centered welcome |
| Temp files | Present (raw_batch*.txt, etc.) | Cleaned |
| `incoming_cars/` | Not present | Ready for CAR files |
## What Changed

*[Placeholder — content to be added]*

## Files to Add/Modify
- `README.md` — rewritten with "Don't Panic" energy
- `setup.sh` — Linux auto-installer (venv + dag_cbor + optional Ollama)
- `setup.bat` — Windows auto-installer
- `tools/generate_mycelium_map.py` — "Don't Panic" message when blockstore is empty
- `.gitignore` — ensure clean public root
- `incoming_cars/` — directory for CAR imports
## What Changed

*[Placeholder — content to be added]*

## Files to Remove (from public branch)
- Paperspace-specific scripts and configs
- `raw_batch*.txt` files
- Temp diagnostic scripts
- Dev-only documentation
## What Changed

*[Placeholder — content to be added]*

## User Flow (Target)
1. `git clone` the `public` branch
2. Run `bash setup.sh` (or double-click `setup.bat` on Windows)
3. Download `cadmies_latest.car` from Releases
4. Drop it in `incoming_cars/`
5. Run `python tools/import_from_car.py incoming_cars/cadmies_latest.car`
6. Run `python tools/generate_mycelium_map.py`
7. Open `mycelium_map.html` — the garden is alive
No `pip install`. No venv commands. No confusion. Just a library that works.
## What Changed

*[Placeholder — content to be added]*

## Status
Branch creation and file modifications pending. The "Don't Panic" README is drafted. Setup scripts are designed but not implemented. The map generator's friendly error message is designed but not coded.
## What Changed

*[Placeholder — content to be added]*

## Next Steps
- Create `public` branch from `main`
- Apply file modifications
- Test the full user flow on a fresh machine
- Publish as the default branch for new users