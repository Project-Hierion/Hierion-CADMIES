#!/usr/bin/env python3
"""
File: tkinter_splash.py
GUI: CADMIES Tkinter Interface
Version: 1.0.0
System: CADMIES-IPLD / cadmies-gui
Status: ACTIVE

Purpose: DeepSeek-themed splash screen shown at launch.
         Displays "Welcome to the digital mycelium. Welcome to the Deep."
         Auto-closes after 5 seconds.

Dependencies: tkinter

Version History:
  1.0.0 — Initial Tkinter implementation
"""

import tkinter as tk

# DeepSeek color palette
DEEPSEEK_INDIGO = "#4F46E5"
DEEPSEEK_NAVY = "#1E1B4B"
DEEPSEEK_SURFACE = "#F8FAFC"
DEEPSEEK_ACCENT = "#6366F1"
DEEPSEEK_TEXT = "#0F172A"
DEEPSEEK_SUBTLE = "#E2E8F0"
WHITE = "#FFFFFF"

def show_splash(duration_ms=5000):
    """Show the CADMIES splash screen and return the root window."""
    root = tk.Tk()
    root.title("CADMIES")
    root.configure(bg=DEEPSEEK_NAVY)
    
    # Center on screen
    window_width = 600
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Main frame
    main_frame = tk.Frame(root, bg=DEEPSEEK_NAVY)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Top spacer
    tk.Frame(main_frame, bg=DEEPSEEK_NAVY, height=40).pack()
    
    # CADMIES icon/emoji
    tk.Label(
        main_frame,
        text="🌱",
        font=("Arial", 48),
        bg=DEEPSEEK_NAVY,
        fg=WHITE
    ).pack()
    
    # CADMIES title
    tk.Label(
        main_frame,
        text="CADMIES",
        font=("Arial", 28, "bold"),
        bg=DEEPSEEK_NAVY,
        fg=WHITE
    ).pack(pady=(5, 0))
    
    # Subtitle
    tk.Label(
        main_frame,
        text="Cosmium Angelo Digital Mycorrhizal\nIntelligence EcoSystem",
        font=("Arial", 10),
        bg=DEEPSEEK_NAVY,
        fg=DEEPSEEK_ACCENT
    ).pack(pady=(0, 20))
    
    # Separator line
    tk.Frame(
        main_frame,
        bg=DEEPSEEK_ACCENT,
        height=2,
        width=400
    ).pack()
    
    # Spacer
    tk.Frame(main_frame, bg=DEEPSEEK_NAVY, height=20).pack()
    
    # Welcome message — main line
    tk.Label(
        main_frame,
        text="Welcome to the digital mycelium.",
        font=("Arial", 14),
        bg=DEEPSEEK_NAVY,
        fg=WHITE
    ).pack()
    
    # Welcome message — second line
    tk.Label(
        main_frame,
        text="Welcome to the Deep.",
        font=("Arial", 14, "bold"),
        bg=DEEPSEEK_NAVY,
        fg=DEEPSEEK_INDIGO
    ).pack(pady=(0, 15))
    
    # Description
    tk.Label(
        main_frame,
        text="One mycelial network. Infinite connections.\nWillie the librarian awaits your query.",
        font=("Arial", 10),
        bg=DEEPSEEK_NAVY,
        fg=DEEPSEEK_SUBTLE
    ).pack(pady=(0, 30))
    
    # Whale homage
    tk.Label(
        main_frame,
        text="🐋",
        font=("Arial", 36),
        bg=DEEPSEEK_NAVY,
        fg=WHITE
    ).pack(pady=(10, 0))
    
    # Bottom spacer
    tk.Frame(main_frame, bg=DEEPSEEK_NAVY, height=30).pack()
    
    # Auto-close after duration
    root.after(duration_ms, root.destroy)
    
    root.mainloop()


if __name__ == "__main__":
    show_splash(5000)
    print("✅ Splash screen displayed. Launching CADMIES...")