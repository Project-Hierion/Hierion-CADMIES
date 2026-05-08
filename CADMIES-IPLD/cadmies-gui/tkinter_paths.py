"""
File: tkinter_paths.py
GUI: CADMIES Tkinter Interface
Version: 1.0.0
System: CADMIES-IPLD / cadmies-gui
Status: ACTIVE

Purpose: Centralized path management for the Tkinter GUI.
         Provides PROJECT_ROOT, STORE_DIR, INDEX_FILE, etc.
         Sits in cadmies-gui/ — no sys.path manipulation needed.

Dependencies: pathlib

Version History:
  1.0.0 — Initial Tkinter implementation, adapted from tools/core/paths.py
"""

from pathlib import Path

# This file is in cadmies-gui/, so go up one level to CADMIES-IPLD/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Standard paths
STORE_DIR = PROJECT_ROOT / "store"
BLOCKS_DIR = STORE_DIR / "blocks"
INDEX_FILE = STORE_DIR / "index" / "human_id_to_cid.json"
LOGS_DIR = STORE_DIR / "logs"
SOURCE_CONCEPTS_DIR = PROJECT_ROOT / "source_concepts"
AGENTS_DIR = PROJECT_ROOT / "agents"