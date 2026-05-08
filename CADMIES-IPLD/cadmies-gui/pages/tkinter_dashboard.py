"""
File: tkinter_dashboard.py
GUI: CADMIES Tkinter Interface
Version: 1.0.0
System: CADMIES-IPLD / cadmies-gui
Status: ACTIVE

Purpose: Dashboard page showing mycelium stats (concept count, Willie version)
         and quick action buttons.

Dependencies: tkinter, tkinter_theme, tkinter_paths

Version History:
  1.0.0 — Initial Tkinter implementation, stat cards, quick actions
  1.0.1 — Fixed path resolution using tkinter_paths, removed DeepSeek stat card
"""

import tkinter as tk
import json

import tkinter_theme as theme
from tkinter_paths import INDEX_FILE


class DashboardPage:
    """Dashboard showing mycelium stats and welcome message."""

    def __init__(self, parent):
        self.parent = parent

    def render(self):
        header = tk.Frame(self.parent, bg=theme.WHITE)
        header.pack(fill=tk.X, padx=30, pady=(30, 20))

        tk.Label(
            header,
            text="Dashboard",
            font=("Arial", 22, "bold"),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Welcome to the digital mycelium. Welcome to the Deep.",
            font=("Arial", 11),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT_LIGHT
        ).pack(anchor="w")

        stats_frame = tk.Frame(self.parent, bg=theme.DEEPSEEK_SURFACE)
        stats_frame.pack(fill=tk.X, padx=30, pady=(0, 20))

        concept_count = 0
        if INDEX_FILE.exists():
            with open(INDEX_FILE) as f:
                index = json.load(f)
            concept_count = len(index)

        self._stat_card(stats_frame, "📚", str(concept_count), "Concepts in Mycelium")
        self._stat_card(stats_frame, "🔗", "v1.2.1", "Willie Search")

        actions_frame = tk.Frame(self.parent, bg=theme.DEEPSEEK_SURFACE)
        actions_frame.pack(fill=tk.X, padx=30, pady=(0, 20))

        tk.Label(
            actions_frame,
            text="Quick Actions",
            font=("Arial", 14, "bold"),
            bg=theme.DEEPSEEK_SURFACE,
            fg=theme.DEEPSEEK_TEXT
        ).pack(anchor="w", pady=(0, 10))

        tk.Button(
            actions_frame,
            text="👓  Ask Willie a Question",
            font=("Arial", 11),
            bg=theme.DEEPSEEK_INDIGO,
            fg=theme.WHITE,
            activebackground=theme.DEEPSEEK_ACCENT,
            activeforeground=theme.WHITE,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(anchor="w", pady=(0, 5))

        tk.Button(
            actions_frame,
            text="➕  Add a New Concept",
            font=("Arial", 11),
            bg=theme.DEEPSEEK_ACCENT,
            fg=theme.WHITE,
            activebackground=theme.DEEPSEEK_INDIGO,
            activeforeground=theme.WHITE,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(anchor="w")

    def _stat_card(self, parent, icon, value, label):
        card = tk.Frame(
            parent,
            bg=theme.WHITE,
            padx=20,
            pady=15,
            highlightbackground=theme.DEEPSEEK_SUBTLE,
            highlightthickness=1
        )
        card.pack(side=tk.LEFT, padx=(0, 15))

        tk.Label(card, text=icon, font=("Arial", 24), bg=theme.WHITE).pack()
        tk.Label(
            card, text=value, font=("Arial", 20, "bold"),
            bg=theme.WHITE, fg=theme.DEEPSEEK_INDIGO
        ).pack()
        tk.Label(
            card, text=label, font=("Arial", 9),
            bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT_LIGHT
        ).pack()