"""
File: tkinter_app.py
GUI: CADMIES Tkinter Interface
Version: 1.1.0
System: CADMIES-IPLD / cadmies-gui
Status: ACTIVE

Purpose: Main application window with sidebar navigation and page switching.
         Hosts Dashboard, Willie Chat, Browse Library, Add Concept, Mycelium Map.

Dependencies: tkinter, tkinter_theme, pages/*

Version History:
  1.0.0 — Initial Tkinter implementation, sidebar + dashboard + willie placeholder
  1.0.1 — Willie Chat page integrated, "All" max concepts option added, Browse Library integrated
  1.1.0 — Mycelium Map page (Firefox launch), Add Concept page, full CADMIES name in sidebar,
          all five pages live, no placeholders remain
"""

import tkinter as tk
from pathlib import Path

import tkinter_theme as theme
from pages.tkinter_dashboard import DashboardPage
from pages.tkinter_willie_chat import WillieChatPage
from pages.tkinter_browse import BrowsePage
from pages.tkinter_mycelium_map import MyceliumMapPage
from pages.tkinter_add_concept import AddConceptPage


class CADMIESApp:
    """Main CADMIES application with sidebar navigation."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CADMIES — Digital Mycelium Interface")
        self.root.configure(bg=theme.DEEPSEEK_SURFACE)

        window_width = 1100
        window_height = 700
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(800, 500)

        self._build_sidebar()
        self._build_content_area()
        self._show_page("dashboard")

    def _build_sidebar(self):
        sidebar = tk.Frame(
            self.root,
            bg=theme.DEEPSEEK_NAVY,
            width=220
        )
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="🌱 CADMIES",
            font=("Arial", 22, "bold"),
            bg=theme.DEEPSEEK_NAVY,
            fg=theme.WHITE
        ).pack(pady=(20, 5))

        tk.Label(
            sidebar,
            text="Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem",
            font=("Arial", 8),
            bg=theme.DEEPSEEK_NAVY,
            fg=theme.DEEPSEEK_ACCENT,
            wraplength=180,
            justify=tk.CENTER
        ).pack(pady=(0, 20))

        tk.Frame(
            sidebar,
            bg=theme.DEEPSEEK_ACCENT,
            height=1
        ).pack(fill=tk.X, padx=20, pady=(0, 15))

        nav_buttons = [
            ("📌  Dashboard", "dashboard"),
            ("👓  Willie Chat", "willie"),
            ("📚  Browse Library", "browse"),
            ("➕  Add Concept", "add"),
            ("🕸️  Mycelium Map", "map"),
        ]

        for label, page_name in nav_buttons:
            btn = tk.Button(
                sidebar,
                text=label,
                font=("Arial", 11),
                bg=theme.DEEPSEEK_NAVY,
                fg=theme.DEEPSEEK_SUBTLE,
                activebackground=theme.DEEPSEEK_INDIGO,
                activeforeground=theme.WHITE,
                relief=tk.FLAT,
                anchor="w",
                padx=20,
                pady=10,
                command=lambda p=page_name: self._show_page(p)
            )
            btn.pack(fill=tk.X)

        tk.Frame(sidebar, bg=theme.DEEPSEEK_NAVY).pack(expand=True)

        tk.Label(
            sidebar,
            text="🐋",
            font=("Arial", 20),
            bg=theme.DEEPSEEK_NAVY,
            fg=theme.WHITE
        ).pack(pady=15)

    def _build_content_area(self):
        self.content_frame = tk.Frame(
            self.root,
            bg=theme.DEEPSEEK_SURFACE
        )
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _show_page(self, page_name: str):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if page_name == "dashboard":
            DashboardPage(self.content_frame).render()
        elif page_name == "willie":
            WillieChatPage(self.content_frame).render()
        elif page_name == "browse":
            BrowsePage(self.content_frame).render()
        elif page_name == "map":
            MyceliumMapPage(self.content_frame).render()
        elif page_name == "add":
            AddConceptPage(self.content_frame).render()

    def run(self):
        self.root.mainloop()