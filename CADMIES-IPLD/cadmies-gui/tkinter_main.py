#!/usr/bin/env python3
"""
File: tkinter_main.py
GUI: CADMIES Tkinter Interface
Version: 1.0.0
System: CADMIES-IPLD / cadmies-gui
Status: ACTIVE

Purpose: Main launcher — chains splash screen → main application window.
         Run this file to start CADMIES GUI.

Dependencies: tkinter, tkinter_splash, tkinter_app

Version History:
  1.0.0 — Initial Tkinter implementation
"""

import sys
from pathlib import Path

# Ensure we can import from the CADMIES root
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import tkinter_splash
import tkinter_app


def main():
    """Launch CADMIES with splash screen then main application."""
    tkinter_splash.show_splash(5000)
    
    cadmies_app = tkinter_app.CADMIESApp()
    cadmies_app.run()


if __name__ == "__main__":
    main()