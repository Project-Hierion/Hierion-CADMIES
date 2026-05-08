"""
File: tkinter_willie_chat.py
GUI: CADMIES Tkinter Interface
Version: 1.0.0
System: CADMIES-IPLD / cadmies-gui
Status: ACTIVE

Purpose: Willie the Librarian chat interface. Uses proven threading.Thread +
         root.after() pattern for non-blocking Ollama queries. No websockets.

Dependencies: tkinter, threading, requests, llm_mycelium_reader, tkinter_theme, tkinter_paths

Version History:
  1.0.0 — Initial Tkinter implementation, keyword search, model/tone/max selectors
  1.0.1 — Added "All" option to max concepts dropdown
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import requests
import sys
from pathlib import Path

import tkinter_theme as theme
from tkinter_paths import AGENTS_DIR

# Make Willie's reader importable
sys.path.insert(0, str(AGENTS_DIR / "code"))
try:
    from llm_mycelium_reader import (
        search_mycelium,
        build_context_for_llm,
        load_all_concept_cids,
    )
    WILLIE_AVAILABLE = True
except ImportError:
    WILLIE_AVAILABLE = False

OLLAMA_URL = "http://localhost:11434/api/generate"
WILLIE_AVATAR = "👓"

MODELS = {
    "tinyllama:1.1b": "TinyLlama 1.1B (Fast)",
    "mistral:7b": "Mistral 7B (Deep)",
}

TONES = ["helpful", "scholarly", "casual", "scottish"]


class WillieChatPage:
    """Willie the Librarian chat interface."""

    def __init__(self, parent):
        self.parent = parent

    def render(self):
        # Header
        header = tk.Frame(self.parent, bg=theme.WHITE)
        header.pack(fill=tk.X, padx=30, pady=(30, 10))

        tk.Label(
            header,
            text="👓  Willie the Librarian",
            font=("Arial", 22, "bold"),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Ach, ask me anythin' about the mycelium. I'll dig through the stacks for ye.",
            font=("Arial", 10, "italic"),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT_LIGHT
        ).pack(anchor="w")

        # Controls row
        controls = tk.Frame(self.parent, bg=theme.DEEPSEEK_SURFACE)
        controls.pack(fill=tk.X, padx=30, pady=(0, 10))

        # Model selector
        tk.Label(
            controls, text="Model:", font=("Arial", 10),
            bg=theme.DEEPSEEK_SURFACE, fg=theme.DEEPSEEK_TEXT
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.model_var = tk.StringVar(value="tinyllama:1.1b")
        model_menu = tk.OptionMenu(
            controls, self.model_var, *MODELS.keys()
        )
        model_menu.config(
            font=("Arial", 10),
            bg=theme.WHITE,
            relief=tk.FLAT
        )
        model_menu.pack(side=tk.LEFT, padx=(0, 15))

        # Tone selector
        tk.Label(
            controls, text="Tone:", font=("Arial", 10),
            bg=theme.DEEPSEEK_SURFACE, fg=theme.DEEPSEEK_TEXT
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.tone_var = tk.StringVar(value="helpful")
        tone_menu = tk.OptionMenu(
            controls, self.tone_var, *TONES
        )
        tone_menu.config(
            font=("Arial", 10),
            bg=theme.WHITE,
            relief=tk.FLAT
        )
        tone_menu.pack(side=tk.LEFT, padx=(0, 15))

        # Max concepts
        tk.Label(
            controls, text="Max Concepts:", font=("Arial", 10),
            bg=theme.DEEPSEEK_SURFACE, fg=theme.DEEPSEEK_TEXT
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.max_var = tk.StringVar(value="5")
        max_menu = tk.OptionMenu(
            controls, self.max_var, "5", "10", "20", "40", "All"
        )
        max_menu.config(
            font=("Arial", 10),
            bg=theme.WHITE,
            relief=tk.FLAT
        )
        max_menu.pack(side=tk.LEFT)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.parent,
            wrap=tk.WORD,
            font=("Arial", 10),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT,
            state=tk.DISABLED,
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 10))

        # Configure text tags for styling
        self.chat_display.tag_configure(
            "user_label",
            foreground=theme.DEEPSEEK_INDIGO,
            font=("Arial", 10, "bold")
        )
        self.chat_display.tag_configure(
            "willie_label",
            foreground=theme.SUCCESS_GREEN,
            font=("Arial", 10, "bold")
        )
        self.chat_display.tag_configure(
            "system_message",
            foreground=theme.DEEPSEEK_TEXT_LIGHT,
            font=("Arial", 9, "italic")
        )
        self.chat_display.tag_configure(
            "thinking",
            foreground=theme.WARNING_AMBER,
            font=("Arial", 9, "italic")
        )

        # Welcome message
        self._add_message(
            "system",
            "Willie the Librarian is ready. Model warm? Let's talk mycelium.\n"
            "💡 Tip: Select 'mistral:7b' for deep reasoning (slower). "
            "'tinyllama:1.1b' for quick answers."
        )

        # Input area
        input_frame = tk.Frame(self.parent, bg=theme.WHITE)
        input_frame.pack(fill=tk.X, padx=30, pady=(0, 20))

        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bg=theme.DEEPSEEK_SURFACE,
            relief=tk.FLAT
        )
        self.input_field.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(10, 10), pady=10)
        self.input_field.bind("<Return>", self._send_message)

        self.send_btn = tk.Button(
            input_frame,
            text="Send",
            font=("Arial", 11, "bold"),
            bg=theme.DEEPSEEK_INDIGO,
            fg=theme.WHITE,
            activebackground=theme.DEEPSEEK_ACCENT,
            activeforeground=theme.WHITE,
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._send_message
        )
        self.send_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

    def _add_message(self, sender, message):
        """Add a message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)

        if sender == "user":
            self.chat_display.insert(tk.END, "You: ", "user_label")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        elif sender == "willie":
            self.chat_display.insert(tk.END, "Willie: ", "willie_label")
            self.chat_display.insert(tk.END, f"{message}\n\n")
        elif sender == "thinking":
            self.chat_display.insert(tk.END, f"{message}\n", "thinking")
        else:
            self.chat_display.insert(tk.END, f"{message}\n\n", "system_message")

        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _send_message(self, event=None):
        """Handle send button or Enter key."""
        query = self.input_field.get().strip()
        if not query:
            return

        self.input_field.delete(0, tk.END)
        self.send_btn.config(state=tk.DISABLED)
        self._add_message("user", query)
        self._add_message("thinking", "👓 Searching the mycelium...")

        # Run in background thread (proven v4.5 pattern)
        threading.Thread(
            target=self._get_willie_response,
            args=(query,),
            daemon=True
        ).start()

    def _get_willie_response(self, query):
        """Background thread: search mycelium + call Ollama."""
        try:
            # Search mycelium (keyword-only to avoid extra Ollama call in GUI)
            if WILLIE_AVAILABLE:
                all_cids = load_all_concept_cids()
                relevant = search_mycelium(query, all_cids, use_semantic=False)
                max_val = self.max_var.get()
                if max_val == "All":
                    max_concepts = len(relevant) if relevant else 1
                else:
                    max_concepts = int(max_val)
                context_str = build_context_for_llm(relevant, max_concepts)
            else:
                context_str = "Mycelium search unavailable."

            system_prompt = (
                f"You are Willie the Librarian, caretaker of CADMIES "
                f"(Cosmium Angelo Digital Mycorrhizal Intelligence EcoSystem) — "
                f"a content-addressed knowledge network of scientific and "
                f"philosophical concepts.\n\n"
                f"HOW TO ANSWER:\n"
                f"1. FIRST: Answer the user's question using YOUR OWN knowledge.\n"
                f"2. SECOND: Compare your answer to what CADMIES says.\n"
                f"3. THIRD: Explain how the mycelium concepts connect to each other.\n"
                f"4. FINALLY: Give a brief summary.\n\n"
                f"CONCEPT REFERENCES: When you reference a CADMIES concept, "
                f"format it like this: '(concept: Concept Title)'. "
                f"This helps the user identify which ideas come from the mycelium.\n\n"
                f"TONE: {self.tone_var.get()}. "
                f"Speak with occasional Scottish groundskeeper flavor.\n\n"
                f"If the mycelium doesn't have relevant concepts, say so honestly."
            )

            full_prompt = (
                f"{context_str}\n\n"
                f"User Question: {query}\n\n"
                f"Willie's Answer:"
            )

            payload = {
                "model": self.model_var.get(),
                "prompt": full_prompt,
                "system": system_prompt,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 1000},
            }

            # This call blocks the THREAD, not the UI (proven pattern)
            response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=1200
            )

            if response.status_code == 200:
                result = response.json()
                answer = result.get("response", "No response generated.").strip()
                # Update UI from the main thread (proven pattern)
                self.parent.after(0, lambda: self._add_message("willie", answer))
                # Mockingbird chirp notification
                def _chirp():
                    self.parent.bell()
                    self.parent.after(60, self.parent.bell)
                    self.parent.after(120, self.parent.bell)
                    self.parent.after(180, self.parent.bell)
                    self.parent.after(350, self.parent.bell)
                    self.parent.after(450, self.parent.bell)
                    self.parent.after(550, self.parent.bell)
                self.parent.after(0, _chirp)
            else:
                self.parent.after(0, lambda: self._add_message(
                    "system", f"❌ Ollama returned status {response.status_code}"
                ))

        except requests.exceptions.Timeout:
            self.parent.after(0, lambda: self._add_message(
                "system", "⏰ Request timed out after 5 minutes. Try a simpler query."
            ))
        except requests.exceptions.ConnectionError:
            self.parent.after(0, lambda: self._add_message(
                "system", "❌ Cannot connect to Ollama. Is it running on localhost:11434?"
            ))
        except Exception as e:
            self.parent.after(0, lambda: self._add_message(
                "system", f"❌ Error: {e}"
            ))
        finally:
            self.parent.after(0, lambda: self.send_btn.config(state=tk.NORMAL))