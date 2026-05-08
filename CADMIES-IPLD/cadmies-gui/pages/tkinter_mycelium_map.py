"""
File: tkinter_mycelium_map.py
GUI: CADMIES Tkinter Interface
Version: 1.0.0
System: CADMIES-IPLD / cadmies-gui
Status: ACTIVE

Purpose: Mycelium Map page — launches the interactive D3/SVG mycelium
         visualization in Firefox. The map requires a JavaScript-capable
         browser and cannot be embedded in Tkinter directly.

Technical Note: Firefox (or any modern browser) is required to view the
         interactive mycelium map. The map uses D3.js for force-directed
         graph rendering and SVG for visualization.

Dependencies: tkinter, webbrowser, tkinter_theme, tkinter_paths

Version History:
  1.0.0 — Initial Tkinter implementation, Firefox launch button
"""

import tkinter as tk
import webbrowser
from pathlib import Path

import tkinter_theme as theme
from tkinter_paths import PROJECT_ROOT

# Path to the mycelium map HTML file
MAP_FILE = PROJECT_ROOT / "mycelium_map.html"


class MyceliumMapPage:
    """Page with information about the mycelium map and a launch button."""

    def __init__(self, parent):
        self.parent = parent

    def render(self):
        # Header
        header = tk.Frame(self.parent, bg=theme.WHITE)
        header.pack(fill=tk.X, padx=30, pady=(30, 10))

        tk.Label(
            header,
            text="🕸️  Mycelium Map",
            font=("Arial", 22, "bold"),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Interactive visualization of the CADMIES knowledge network",
            font=("Arial", 10),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT_LIGHT
        ).pack(anchor="w")

        # Main content
        content = tk.Frame(self.parent, bg=theme.DEEPSEEK_SURFACE)
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))

        # Info card
        info_card = tk.Frame(
            content,
            bg=theme.WHITE,
            padx=30,
            pady=25,
            highlightbackground=theme.DEEPSEEK_SUBTLE,
            highlightthickness=1
        )
        info_card.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            info_card,
            text="About the Mycelium Map",
            font=("Arial", 14, "bold"),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT
        ).pack(anchor="w", pady=(0, 10))

        tk.Label(
            info_card,
            text=(
                "The mycelium map is an interactive force-directed graph showing all 87 concepts "
                "in the CADMIES knowledge network. Each node is a concept. Each connection is a "
                "relationship — builds_upon, related_to, or contradicts.\n\n"
                "• Drag nodes to rearrange the network\n"
                "• Scroll to zoom in and out\n"
                "• Hover over a node to see the concept name\n"
                "• Click a node to highlight its connections\n\n"
                "The map requires Firefox (or any modern browser) to render the interactive "
                "visualization. It will open in your default browser when you click the button below."
            ),
            font=("Arial", 10),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT,
            wraplength=700,
            justify=tk.LEFT
        ).pack(anchor="w")

        # Map status
        map_exists = MAP_FILE.exists()
        status_frame = tk.Frame(content, bg=theme.DEEPSEEK_SURFACE)
        status_frame.pack(fill=tk.X, pady=(0, 20))

        if map_exists:
            tk.Label(
                status_frame,
                text="✅  Mycelium map file found",
                font=("Arial", 11),
                bg=theme.DEEPSEEK_SURFACE,
                fg=theme.SUCCESS_GREEN
            ).pack(anchor="w", pady=(0, 10))

            launch_btn = tk.Button(
                status_frame,
                text="🕸️  Launch Mycelium Map in Firefox",
                font=("Arial", 12, "bold"),
                bg=theme.DEEPSEEK_INDIGO,
                fg=theme.WHITE,
                activebackground=theme.DEEPSEEK_ACCENT,
                activeforeground=theme.WHITE,
                relief=tk.FLAT,
                padx=25,
                pady=12,
                cursor="hand2",
                command=self._launch_map
            )
            launch_btn.pack(anchor="w")

            tk.Label(
                status_frame,
                text=f"Map location: {MAP_FILE}",
                font=("Arial", 8),
                bg=theme.DEEPSEEK_SURFACE,
                fg=theme.DEEPSEEK_TEXT_LIGHT
            ).pack(anchor="w", pady=(5, 0))
        else:
            tk.Label(
                status_frame,
                text="❌  Mycelium map file not found",
                font=("Arial", 11),
                bg=theme.DEEPSEEK_SURFACE,
                fg=theme.ERROR_RED
            ).pack(anchor="w", pady=(0, 5))

            tk.Label(
                status_frame,
                text=f"Expected at: {MAP_FILE}\nRun the map generator script to create it.",
                font=("Arial", 9),
                bg=theme.DEEPSEEK_SURFACE,
                fg=theme.DEEPSEEK_TEXT_LIGHT
            ).pack(anchor="w")

        # Technical note
        note_frame = tk.Frame(
            content,
            bg=theme.DEEPSEEK_SURFACE_ALT,
            padx=15,
            pady=10,
            highlightbackground=theme.DEEPSEEK_SUBTLE,
            highlightthickness=1
        )
        note_frame.pack(fill=tk.X)

        tk.Label(
            note_frame,
            text=(
                "📋  Technical Note: The mycelium map uses D3.js and SVG for interactive "
                "visualization. This requires a JavaScript-capable web browser (Firefox recommended). "
                "The map cannot be embedded directly in the Tkinter GUI. Future versions may support "
                "embedded webview rendering."
            ),
            font=("Arial", 8, "italic"),
            bg=theme.DEEPSEEK_SURFACE_ALT,
            fg=theme.DEEPSEEK_TEXT_LIGHT,
            wraplength=700,
            justify=tk.LEFT
        ).pack(anchor="w")

    def _launch_map(self):
        """Open the mycelium map in the default web browser."""
        if MAP_FILE.exists():
            webbrowser.open(f"file://{MAP_FILE}")