# NiceGUI Interface (Archived — May 2026)

This directory contains the original CADMIES graphical interface built with [NiceGUI](https://nicegui.io/), a web-based UI framework. It was retired in favor of the Tkinter desktop GUI due to websocket timeout issues on CPU-only systems.

## Why Was This Retired?

NiceGUI uses persistent websockets for real-time UI updates. When running LLM inference on CPU (30-120 second response times), the websocket connection idles out and drops — taking the entire UI with it. Multiple attempts to fix this (increased ping timeouts, streaming, singleton patterns, sequential execution) were unsuccessful.

## Does It Still Work?

**Yes — on GPU-accelerated systems.** If your machine has an NVIDIA GPU (CUDA) or AMD GPU (ROCm) and Ollama inference completes in 2-5 seconds, the NiceGUI interface should work without websocket drops. The websocket timeout never triggers because responses arrive quickly.

## Launch Instructions (GPU Users)

backtickbash
# From CADMIES-IPLD root
cd cadmies-gui/archived-nicegui
pip install -r requirements.txt
python gui_main.py
backtick

Open `http://localhost:8081` in your browser.

## Features (Preserved)

- Dashboard with system stats and easter egg (click the 🌱)
- Add Concept page with live preview
- Browse Library with search and provenance view
- Willie Chat interface (subject to same websocket limitations)
- Mycelium Map (interactive knowledge graph)
- Audit Trail

## Why Keep This?

This is part of CADMIES history. The NiceGUI interface was the first GUI, built May 3-7, 2026. It proved the concept of a visual mycelium browser. It also taught us an important lesson about architecture matching hardware constraints. For GPU users, it may still be the better interface — it's more visually polished and browser-based.

## Current GUI

The active CADMIES GUI is a Tkinter desktop application at `cadmies-gui/tkinter_main.py`. See `cadmies-gui/README.md` for details.

---

*Retired with gratitude. The cathedral's first stained glass window.* 🌱
