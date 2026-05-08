"""
File: tkinter_add_concept.py
GUI: CADMIES Tkinter Interface
Version: 1.0.0
System: CADMIES-IPLD / cadmies-gui
Status: ACTIVE

Purpose: Add Concept page — full form for submitting new concepts to the
         mycelium. Saves JSON to source_concepts/ for CID minting.

Dependencies: tkinter, json, datetime, tkinter_theme, tkinter_paths

Version History:
  1.0.0 — Initial Tkinter implementation, full CID spec form
"""

import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from pathlib import Path

import tkinter_theme as theme
from tkinter_paths import SOURCE_CONCEPTS_DIR

# Dropdown options
DOMAINS = [
    "Philosophy", "Biology", "Cognitive_Science", "Complexity_Science",
    "Physics", "Mathematics", "Buddhist_Philosophy", "Taoist_Philosophy",
    "Epistemology", "Ethics", "Climate_Ethics", "Ecology", "Other"
]

TYPES = [
    "PhilosophicalPrinciple", "ScientificTheory", "ScientificHypothesis",
    "BiologicalAdaptation", "PsychologicalConcept", "MathematicalTheorem",
    "Other"
]

DIFFICULTY_LEVELS = ["beginner", "intermediate", "expert"]


class AddConceptPage:
    """Form page for adding new concepts to the mycelium."""

    def __init__(self, parent):
        self.parent = parent
        self.fields = {}

    def render(self):
        # Header
        header = tk.Frame(self.parent, bg=theme.WHITE)
        header.pack(fill=tk.X, padx=30, pady=(30, 10))

        tk.Label(
            header,
            text="➕  Add Concept",
            font=("Arial", 22, "bold"),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Submit a new concept to the mycelium. JSON will be saved to source_concepts/ for CID minting.",
            font=("Arial", 10),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT_LIGHT
        ).pack(anchor="w")

        # Scrollable form area
        canvas = tk.Canvas(self.parent, bg=theme.DEEPSEEK_SURFACE, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.parent, orient=tk.VERTICAL, command=canvas.yview)
        form_frame = tk.Frame(canvas, bg=theme.DEEPSEEK_SURFACE)

        form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 60)), "units")
        def _bind_scroll(event): event.widget.bind_all("<MouseWheel>", _on_mousewheel)
        def _unbind_scroll(event): event.widget.unbind_all("<MouseWheel>")
        canvas.bind("<Enter>", _bind_scroll)
        canvas.bind("<Leave>", _unbind_scroll)

        # ── Required Fields ──────────────────────────────────────────
        self._section_label(form_frame, "Required Fields")

        self._text_field(form_frame, "Human ID", "human_id",
                         "Unique snake_case identifier (e.g., 'my_new_concept')")
        self._text_field(form_frame, "Title", "title",
                         "Display title of the concept")
        self._text_field(form_frame, "Definition", "definition",
                         "Clear 1-5 sentence definition", height=3)

        # Domain dropdown + Other
        self._dropdown_with_other(form_frame, "Domain", "domain", DOMAINS)
        self._dropdown_with_other(form_frame, "Type", "type", TYPES)

        # ── Optional Fields ──────────────────────────────────────────
        self._section_label(form_frame, "Optional Details")

        self._text_field(form_frame, "Subdomain", "subdomain",
                         "Specific subcategory (e.g., 'Embodied Cognition')")
        self._text_field(form_frame, "Mantra", "mantra",
                         "Short memorable phrase")
        self._text_field(form_frame, "Poetic Version", "poetic_version",
                         "Metaphorical or poetic expression of the concept", height=2)

        # Axioms (multi-line)
        tk.Label(
            form_frame,
            text="Core Truths (Axioms) — one per line",
            font=("Arial", 10, "bold"),
            bg=theme.DEEPSEEK_SURFACE,
            fg=theme.DEEPSEEK_TEXT
        ).pack(anchor="w", padx=30, pady=(15, 5))

        axioms_text = tk.Text(form_frame, height=4, font=("Arial", 10),
                              bg=theme.WHITE, relief=tk.FLAT,
                              highlightbackground=theme.DEEPSEEK_SUBTLE,
                              highlightthickness=1)
        axioms_text.pack(fill=tk.X, padx=30, pady=(0, 10))
        self.fields['axioms'] = axioms_text

        # Builds Upon, Related To, Contradicts
        self._text_field(form_frame, "Builds Upon",
                         "builds_upon",
                         "Comma-separated human_ids this concept extends")
        self._text_field(form_frame, "Related To",
                         "related_to",
                         "Comma-separated human_ids with meaningful connections")
        self._text_field(form_frame, "Contradicts",
                         "contradicts",
                         "Comma-separated human_ids this challenges")

        # Difficulty levels
        self._section_label(form_frame, "Difficulty Levels")
        diff_frame = tk.Frame(form_frame, bg=theme.DEEPSEEK_SURFACE)
        diff_frame.pack(fill=tk.X, padx=30, pady=(0, 10))
        self.diff_fields = {}
        for level in DIFFICULTY_LEVELS:
            tk.Label(diff_frame, text=f"{level.title()}:",
                     font=("Arial", 9), bg=theme.DEEPSEEK_SURFACE,
                     fg=theme.DEEPSEEK_TEXT).pack(anchor="w", pady=(5, 2))
            text = tk.Text(diff_frame, height=2, font=("Arial", 9),
                          bg=theme.WHITE, relief=tk.FLAT,
                          highlightbackground=theme.DEEPSEEK_SUBTLE,
                          highlightthickness=1)
            text.pack(fill=tk.X, pady=(0, 5))
            self.diff_fields[level] = text

        # ── Metadata ─────────────────────────────────────────────────
        self._section_label(form_frame, "Metadata")
        self._text_field(form_frame, "Certainty Score (0.0 - 1.0)",
                         "certainty_score",
                         "How confident are you in this concept? (e.g., 0.85)")
        self._text_field(form_frame, "Genesis",
                         "genesis",
                         "Origin story — how was this concept discovered?", height=2)

        # ── Submit Button ────────────────────────────────────────────
        btn_frame = tk.Frame(form_frame, bg=theme.DEEPSEEK_SURFACE)
        btn_frame.pack(fill=tk.X, padx=30, pady=(20, 30))

        tk.Button(
            btn_frame,
            text="Submit Concept to Mycelium",
            font=("Arial", 12, "bold"),
            bg=theme.DEEPSEEK_INDIGO,
            fg=theme.WHITE,
            activebackground=theme.DEEPSEEK_ACCENT,
            activeforeground=theme.WHITE,
            relief=tk.FLAT,
            padx=25,
            pady=12,
            cursor="hand2",
            command=self._submit
        ).pack(side=tk.LEFT)

        tk.Button(
            btn_frame,
            text="Reset Form",
            font=("Arial", 10),
            bg=theme.DEEPSEEK_SURFACE_ALT,
            fg=theme.DEEPSEEK_TEXT,
            activebackground=theme.DEEPSEEK_SUBTLE,
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor="hand2",
            command=self._reset
        ).pack(side=tk.RIGHT)

    # ── Form Helpers ─────────────────────────────────────────────

    def _section_label(self, parent, text):
        tk.Label(
            parent,
            text=text,
            font=("Arial", 14, "bold"),
            bg=theme.DEEPSEEK_SURFACE,
            fg=theme.DEEPSEEK_INDIGO
        ).pack(anchor="w", padx=30, pady=(20, 10))

    def _text_field(self, parent, label, key, tooltip, height=1):
        tk.Label(
            parent,
            text=label,
            font=("Arial", 10, "bold"),
            bg=theme.DEEPSEEK_SURFACE,
            fg=theme.DEEPSEEK_TEXT
        ).pack(anchor="w", padx=30, pady=(10, 2))

        if height == 1:
            widget = tk.Entry(
                parent,
                font=("Arial", 10),
                bg=theme.WHITE,
                relief=tk.FLAT,
                highlightbackground=theme.DEEPSEEK_SUBTLE,
                highlightthickness=1
            )
            widget.pack(fill=tk.X, padx=30, pady=(0, 5))
        else:
            widget = tk.Text(
                parent,
                height=height,
                font=("Arial", 10),
                bg=theme.WHITE,
                relief=tk.FLAT,
                highlightbackground=theme.DEEPSEEK_SUBTLE,
                highlightthickness=1
            )
            widget.pack(fill=tk.X, padx=30, pady=(0, 5))

        self.fields[key] = widget

        if tooltip:
            tk.Label(
                parent,
                text=f"  💡 {tooltip}",
                font=("Arial", 8, "italic"),
                bg=theme.DEEPSEEK_SURFACE,
                fg=theme.DEEPSEEK_TEXT_LIGHT
            ).pack(anchor="w", padx=30)

    def _dropdown_with_other(self, parent, label, key, options):
        tk.Label(
            parent,
            text=label,
            font=("Arial", 10, "bold"),
            bg=theme.DEEPSEEK_SURFACE,
            fg=theme.DEEPSEEK_TEXT
        ).pack(anchor="w", padx=30, pady=(10, 2))

        var = tk.StringVar(value=options[0])
        menu = tk.OptionMenu(parent, var, *options)
        menu.config(font=("Arial", 10), bg=theme.WHITE, relief=tk.FLAT)
        menu.pack(anchor="w", padx=30, pady=(0, 5))

        self.fields[key] = var
        self.fields[f"{key}_other"] = None

    # ── Form Actions ──────────────────────────────────────────────

    def _get_value(self, key):
        """Get the value of a field, handling both Entry and Text widgets."""
        widget = self.fields.get(key)
        if widget is None:
            return ""
        if isinstance(widget, tk.Text):
            return widget.get("1.0", "end-1c").strip()
        if isinstance(widget, tk.StringVar):
            val = widget.get()
            if val == "Other":
                other_key = f"{key}_other"
                return self.fields.get(other_key, "")
            return val
        if isinstance(widget, tk.Entry):
            return widget.get().strip()
        return ""

    def _submit(self):
        """Validate and save the concept."""
        human_id = self._get_value("human_id")
        title = self._get_value("title")
        definition = self._get_value("definition")

        if not human_id or not title or not definition:
            messagebox.showwarning(
                "Missing Fields",
                "Human ID, Title, and Definition are required."
            )
            return

        # Build concept dict
        concept = {
            "schema_version": "1.0.0",
            "human_id": human_id.strip().replace(" ", "_"),
            "title": title.strip(),
            "definition": definition.strip(),
            "type": self._get_value("type"),
            "domain": self._get_value("domain"),
            "subdomain": self._get_value("subdomain"),
            "axioms": [a.strip() for a in self._get_value("axioms").split("\n") if a.strip()],
            "poetic_version": self._get_value("poetic_version"),
            "mantra": self._get_value("mantra"),
            "builds_upon": [b.strip() for b in self._get_value("builds_upon").split(",") if b.strip()],
            "related_to": [r.strip() for r in self._get_value("related_to").split(",") if r.strip()],
            "contradicts": [c.strip() for c in self._get_value("contradicts").split(",") if c.strip()],
            "metadata": {
                "created": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "creator": "Hieros-CADMIES",
                "certainty_score": float(self._get_value("certainty_score") or 0.5),
                "version": 1,
                "license": "CC BY-SA 4.0",
                "purpose": "educational",
                "genesis": self._get_value("genesis")
            },
            "difficulty_levels": {}
        }

        for level in DIFFICULTY_LEVELS:
            text = self.diff_fields[level].get("1.0", "end-1c").strip()
            if text:
                concept["difficulty_levels"][level] = text

        # Save to source_concepts/
        SOURCE_CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)
        filename = f"{concept['human_id']}.json"
        filepath = SOURCE_CONCEPTS_DIR / filename

        with open(filepath, "w") as f:
            json.dump(concept, f, indent=2)

        messagebox.showinfo(
            "Concept Saved",
            f"✅ '{concept['title']}' saved to:\n{filepath}\n\n"
            f"Next step: Run the CID generator to mint this concept into the mycelium.\n\n"
            f"Command:\npython tools/core/cid_generator_v1_1_0.py --concept-file source_concepts/{filename}"
        )

    def _reset(self):
        """Reset all form fields."""
        for key, widget in self.fields.items():
            if isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
            elif isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.StringVar):
                widget.set(DOMAINS[0] if key == "domain" else (TYPES[0] if key == "type" else ""))
        for text in self.diff_fields.values():
            text.delete("1.0", tk.END)