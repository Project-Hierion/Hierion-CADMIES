"""
File: tkinter_browse.py
GUI: CADMIES Tkinter Interface
Version: 1.3.0
System: CADMIES-IPLD / cadmies-gui
Status: ACTIVE

Purpose: Browse Library page — card-based scrollable list of all mycelium concepts.
         Click any card to open a detail popup with full concept info.
         Detail popup supports history navigation and clickable related concepts.

Dependencies: tkinter, json, tkinter_theme, tkinter_paths, llm_mycelium_reader

Version History:
  1.0.0 — Initial Tkinter implementation, card layout, click-to-open detail
  1.1.0 — Added mantra, subdomain, builds_upon, related_to, contradicts, metadata,
          difficulty levels to detail popup. Clickable related concepts with
          back/forward navigation history. Fixed human ID text color.
  1.2.0 — Fixed broken links: parses colon/slash-format references to find
          correct human_id in index. Fixed scroll conflicts with multiple popups
          open (per-popup mousewheel binding). Added link-failure feedback.
          Cleaned up mousewheel unbind on popup close. Mid-word cut prevention
          on card definition snippets.
  1.3.0 — Standardized link icons (🔗 across all sections). Contradicts distinguished
          by red color only. Unresolved references show 📋 with "(concept not yet
          in mycelium)". Hover tooltips on unresolved links explain the status.
"""

import tkinter as tk
import json
import sys

import tkinter_theme as theme
from tkinter_paths import INDEX_FILE

# Import concept loader
sys.path.insert(0, str(INDEX_FILE.parent.parent.parent / "agents" / "code"))
try:
    from cadmies_concept_reader import load_concept as _load_concept_raw
    READER_AVAILABLE = True
except ImportError:
    READER_AVAILABLE = False
    _load_concept_raw = None


def _resolve_human_id(reference: str) -> str | None:
    """
    Resolve a concept reference to its actual human_id in the index.
    Handles colon/slash formats like 'buddhist_philosophy:principle/non_attachment_vs_detachment'
    by trying: the full string, the part after the last slash, the part after the last colon,
    and the part after the last colon+slash.
    Returns the matching human_id or None.
    """
    if not INDEX_FILE.exists():
        return None

    with open(INDEX_FILE) as f:
        index = json.load(f)

    # Direct match
    if reference in index:
        return reference

    # Try stripping prefixes: 'domain:subdomain/human_id' -> 'human_id'
    candidates = []

    # After last slash
    if '/' in reference:
        candidates.append(reference.rsplit('/', 1)[-1])

    # After last colon
    if ':' in reference:
        candidates.append(reference.rsplit(':', 1)[-1])

    # After last colon+slash combined
    if '/' in reference and ':' in reference:
        last_sep = max(reference.rfind(':'), reference.rfind('/'))
        candidates.append(reference[last_sep + 1:])

    # Also try replacing slashes with underscores
    for c in list(candidates):
        candidates.append(c.replace('/', '_'))

    for candidate in candidates:
        if candidate in index:
            return candidate

    return None


def _load_full_concept(human_id_or_cid):
    """Load a concept by human_id or CID. Returns dict or None."""
    if not READER_AVAILABLE or not INDEX_FILE.exists():
        return None

    resolved = _resolve_human_id(human_id_or_cid)
    if resolved is None:
        return None

    with open(INDEX_FILE) as f:
        index = json.load(f)

    cid = index.get(resolved)
    if cid is None:
        return None

    result = _load_concept_raw(cid)
    if 'error' in result:
        return None
    return result


class BrowsePage:
    """Browse all concepts as cards in a scrollable canvas."""

    def __init__(self, parent):
        self.parent = parent
        self.all_concepts = []

    def render(self):
        # Header
        header = tk.Frame(self.parent, bg=theme.WHITE)
        header.pack(fill=tk.X, padx=30, pady=(30, 10))

        tk.Label(
            header,
            text="📚  Browse Library",
            font=("Arial", 22, "bold"),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT
        ).pack(anchor="w")

        self._load_concepts()

        tk.Label(
            header,
            text=f"{len(self.all_concepts)} concepts in the mycelium",
            font=("Arial", 10),
            bg=theme.WHITE,
            fg=theme.DEEPSEEK_TEXT_LIGHT
        ).pack(anchor="w")

        # Scrollable card area
        canvas_frame = tk.Frame(self.parent, bg=theme.DEEPSEEK_SURFACE)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(10, 20))

        canvas = tk.Canvas(
            canvas_frame,
            bg=theme.DEEPSEEK_SURFACE,
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            canvas_frame,
            orient=tk.VERTICAL,
            command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas, bg=theme.DEEPSEEK_SURFACE)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 60)), "units")

        def _bind_scroll(event):
            event.widget.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_scroll(event):
            event.widget.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", _bind_scroll)
        canvas.bind("<Leave>", _unbind_scroll)

        for i, concept in enumerate(self.all_concepts):
            self._render_card(scrollable_frame, concept, i)

    def _load_concepts(self):
        """Load all concepts from the index."""
        if not INDEX_FILE.exists():
            return

        with open(INDEX_FILE) as f:
            index = json.load(f)

        for human_id, cid in index.items():
            if READER_AVAILABLE:
                concept = _load_concept_raw(cid)
                if 'error' not in concept:
                    self.all_concepts.append({
                        'human_id': human_id,
                        'cid': cid,
                        'title': concept.get('title', 'Untitled'),
                        'domain': concept.get('domain', 'Unknown'),
                        'definition': concept.get('definition', ''),
                        'type': concept.get('type', ''),
                    })
            else:
                self.all_concepts.append({
                    'human_id': human_id,
                    'cid': cid,
                    'title': human_id.replace('_', ' ').title(),
                    'domain': 'Unknown',
                    'definition': '',
                    'type': '',
                })

        self.all_concepts.sort(key=lambda c: c['title'].lower())

    def _render_card(self, parent, concept, index):
        """Render a single concept card."""
        bg_color = theme.WHITE if index % 2 == 0 else theme.DEEPSEEK_SURFACE_ALT

        card = tk.Frame(
            parent,
            bg=bg_color,
            padx=20,
            pady=12,
            highlightbackground=theme.DEEPSEEK_SUBTLE,
            highlightthickness=1,
            cursor="hand2"
        )
        card.pack(fill=tk.X, padx=0, pady=(0, 1))
        card.bind("<Button-1>", lambda e, c=concept: self._open_detail_popup(c))

        title_frame = tk.Frame(card, bg=bg_color)
        title_frame.pack(fill=tk.X)
        title_frame.bind("<Button-1>", lambda e, c=concept: self._open_detail_popup(c))

        title_label = tk.Label(
            title_frame,
            text=concept['title'],
            font=("Arial", 12, "bold"),
            bg=bg_color,
            fg=theme.DEEPSEEK_TEXT
        )
        title_label.pack(side=tk.LEFT)
        title_label.bind("<Button-1>", lambda e, c=concept: self._open_detail_popup(c))

        domain_badge = tk.Label(
            title_frame,
            text=f" {concept['domain']} ",
            font=("Arial", 8),
            bg=theme.DEEPSEEK_INDIGO,
            fg=theme.WHITE,
            padx=6,
            pady=2
        )
        domain_badge.pack(side=tk.RIGHT)
        domain_badge.bind("<Button-1>", lambda e, c=concept: self._open_detail_popup(c))

        if concept['type']:
            type_badge = tk.Label(
                title_frame,
                text=f" {concept['type']} ",
                font=("Arial", 8),
                bg=theme.DEEPSEEK_ACCENT,
                fg=theme.WHITE,
                padx=6,
                pady=2
            )
            type_badge.pack(side=tk.RIGHT, padx=(0, 5))
            type_badge.bind("<Button-1>", lambda e, c=concept: self._open_detail_popup(c))

        definition = concept.get('definition', '')
        if definition:
            snippet = definition[:150]
            if len(definition) > 150:
                snippet = snippet.rsplit(' ', 1)[0] + "..."
            def_label = tk.Label(
                card,
                text=snippet,
                font=("Arial", 9),
                bg=bg_color,
                fg=theme.DEEPSEEK_TEXT_LIGHT,
                wraplength=700,
                justify=tk.LEFT
            )
            def_label.pack(anchor="w", pady=(4, 4))
            def_label.bind("<Button-1>", lambda e, c=concept: self._open_detail_popup(c))

        id_label = tk.Label(
            card,
            text=f"ID: {concept['human_id']}  •  CID: {concept['cid'][:24]}...",
            font=("Arial", 8),
            bg=bg_color,
            fg=theme.DEEPSEEK_SUBTLE
        )
        id_label.pack(anchor="w")
        id_label.bind("<Button-1>", lambda e, c=concept: self._open_detail_popup(c))

    # ── Tooltip helpers ──────────────────────────────────────────────

    def _show_tooltip(self, event, text):
        """Show a small tooltip popup near the cursor."""
        tooltip = tk.Toplevel(event.widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root + 15}+{event.y_root + 10}")

        label = tk.Label(
            tooltip,
            text=text,
            font=("Arial", 9),
            bg=theme.DEEPSEEK_TEXT,
            fg=theme.WHITE,
            padx=10,
            pady=5,
            wraplength=350,
        )
        label.pack()

        event.widget._tooltip = tooltip

    def _hide_tooltip(self, event):
        """Hide the tooltip."""
        if hasattr(event.widget, '_tooltip') and event.widget._tooltip:
            event.widget._tooltip.destroy()
            event.widget._tooltip = None

    # ── Detail popup ─────────────────────────────────────────────────

    def _open_detail_popup(self, concept):
        """Open the detail popup for a concept. Sets up history tracking."""
        popup = tk.Toplevel(self.parent)
        popup.title(concept['title'])
        popup.configure(bg=theme.WHITE)

        w, h = 650, 600
        x = popup.winfo_screenwidth() // 2 - w // 2
        y = popup.winfo_screenheight() // 2 - h // 2
        popup.geometry(f"{w}x{h}+{x}+{y}")

        popup.history = [concept['human_id']]
        popup.history_index = 0

        popup.protocol("WM_DELETE_WINDOW", lambda: self._close_popup(popup))
        self._build_popup_ui(popup, concept)

    def _close_popup(self, popup):
        """Clean up and close a detail popup."""
        popup.unbind_all("<MouseWheel>")
        popup.destroy()

    def _build_popup_ui(self, popup, concept):
        """Build the full UI inside a detail popup."""
        for widget in popup.winfo_children():
            widget.destroy()

        popup.title(concept['title'])

        # ── Navigation bar ────────────────────────────────────────────
        nav_bar = tk.Frame(popup, bg=theme.DEEPSEEK_SURFACE_ALT, padx=10, pady=5)
        nav_bar.pack(fill=tk.X)

        back_btn = tk.Button(
            nav_bar, text="← Back", font=("Arial", 9),
            bg=theme.DEEPSEEK_SURFACE, relief=tk.FLAT,
            command=lambda: self._navigate_history(popup, -1),
            cursor="hand2"
        )
        back_btn.pack(side=tk.LEFT, padx=(0, 5))
        if popup.history_index <= 0:
            back_btn.config(state=tk.DISABLED)

        fwd_btn = tk.Button(
            nav_bar, text="Forward →", font=("Arial", 9),
            bg=theme.DEEPSEEK_SURFACE, relief=tk.FLAT,
            command=lambda: self._navigate_history(popup, 1),
            cursor="hand2"
        )
        fwd_btn.pack(side=tk.LEFT)
        if popup.history_index >= len(popup.history) - 1:
            fwd_btn.config(state=tk.DISABLED)

        tk.Label(
            nav_bar, text=f"  {popup.history_index + 1} / {len(popup.history)}",
            font=("Arial", 8), bg=theme.DEEPSEEK_SURFACE_ALT, fg=theme.DEEPSEEK_TEXT_LIGHT
        ).pack(side=tk.LEFT, padx=10)

        # ── Scrollable content ────────────────────────────────────────
        canvas = tk.Canvas(popup, bg=theme.WHITE, highlightthickness=0)
        scrollbar = tk.Scrollbar(popup, orient=tk.VERTICAL, command=canvas.yview)
        content = tk.Frame(canvas, bg=theme.WHITE)

        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 60)), "units")

        def _bind_scroll(event):
            event.widget.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_scroll(event):
            event.widget.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", _bind_scroll)
        canvas.bind("<Leave>", _unbind_scroll)

        full = _load_full_concept(concept['human_id'])

        # ── Title ─────────────────────────────────────────────────────
        tk.Label(
            content, text=concept['title'],
            font=("Arial", 18, "bold"), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT
        ).pack(anchor="w", padx=25, pady=(25, 5))

        # ── Badges ────────────────────────────────────────────────────
        badges = tk.Frame(content, bg=theme.WHITE)
        badges.pack(anchor="w", padx=25, pady=(0, 10))

        tk.Label(
            badges, text=f" {concept['domain']} ",
            font=("Arial", 9), bg=theme.DEEPSEEK_INDIGO, fg=theme.WHITE,
            padx=8, pady=3
        ).pack(side=tk.LEFT, padx=(0, 6))

        if full:
            subdomain = full.get('subdomain', '')
            if subdomain:
                tk.Label(
                    badges, text=f" {subdomain} ",
                    font=("Arial", 9), bg=theme.DEEPSEEK_ACCENT, fg=theme.WHITE,
                    padx=8, pady=3
                ).pack(side=tk.LEFT, padx=(0, 6))

        if concept['type']:
            tk.Label(
                badges, text=f" {concept['type']} ",
                font=("Arial", 9), bg=theme.SUCCESS_GREEN, fg=theme.WHITE,
                padx=8, pady=3
            ).pack(side=tk.LEFT)

        if not full:
            tk.Label(
                content,
                text="\nHuman ID: {}\nCID: {}".format(concept['human_id'], concept['cid']),
                font=("Arial", 8), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT_LIGHT
            ).pack(anchor="w", padx=25, pady=(15, 25))
            return

        # ── Mantra ────────────────────────────────────────────────────
        mantra = full.get('mantra', '')
        if mantra:
            tk.Label(
                content, text="Mantra",
                font=("Arial", 12, "bold"), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT
            ).pack(anchor="w", padx=25, pady=(15, 5))
            tk.Label(
                content, text=f"\"{mantra}\"",
                font=("Arial", 11, "italic"), bg=theme.DEEPSEEK_SURFACE_ALT,
                fg=theme.DEEPSEEK_INDIGO, wraplength=580, justify=tk.LEFT,
                padx=15, pady=10
            ).pack(anchor="w", padx=25, pady=(0, 10))

        # ── Definition ────────────────────────────────────────────────
        definition = full.get('definition', concept.get('definition', ''))
        tk.Label(
            content, text="Definition",
            font=("Arial", 12, "bold"), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT
        ).pack(anchor="w", padx=25, pady=(10, 5))
        tk.Label(
            content, text=definition,
            font=("Arial", 10), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT,
            wraplength=580, justify=tk.LEFT
        ).pack(anchor="w", padx=25, pady=(0, 15))

        # ── Poetic Version ────────────────────────────────────────────
        poetic = full.get('poetic_version', '')
        if poetic:
            tk.Label(
                content, text="Poetic Version",
                font=("Arial", 12, "bold"), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT
            ).pack(anchor="w", padx=25, pady=(10, 5))
            tk.Label(
                content, text=f"\"{poetic}\"",
                font=("Arial", 10, "italic"), bg=theme.DEEPSEEK_SURFACE_ALT,
                fg=theme.DEEPSEEK_TEXT_LIGHT, wraplength=580, justify=tk.LEFT,
                padx=15, pady=10
            ).pack(anchor="w", padx=25, pady=(0, 15))

        # ── Core Truths (Axioms) ──────────────────────────────────────
        axioms = full.get('axioms', [])
        if axioms:
            tk.Label(
                content, text="Core Truths",
                font=("Arial", 12, "bold"), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT
            ).pack(anchor="w", padx=25, pady=(10, 5))
            for axiom in axioms:
                tk.Label(
                    content, text=f"• {axiom}",
                    font=("Arial", 10), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT,
                    wraplength=580, justify=tk.LEFT
                ).pack(anchor="w", padx=40, pady=2)

        # ── Builds Upon ───────────────────────────────────────────────
        builds = full.get('builds_upon', [])
        if builds:
            tk.Label(
                content, text="Builds Upon",
                font=("Arial", 12, "bold"), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT
            ).pack(anchor="w", padx=25, pady=(15, 5))
            builds_frame = tk.Frame(content, bg=theme.WHITE)
            builds_frame.pack(anchor="w", padx=25, pady=(0, 10))
            for b in builds:
                resolved = _resolve_human_id(b)
                if resolved is None:
                    link_text = f"📋 {b} (concept not yet in mycelium)"
                    link_fg = theme.DEEPSEEK_TEXT_LIGHT
                else:
                    link_text = f"🔗 {b}"
                    link_fg = theme.DEEPSEEK_INDIGO

                link = tk.Label(
                    builds_frame, text=link_text,
                    font=("Arial", 10, "underline"), bg=theme.WHITE,
                    fg=link_fg, cursor="hand2"
                )
                link.pack(anchor="w", pady=1)
                if resolved:
                    link.bind("<Button-1>", lambda e, hid=b, p=popup: self._follow_link(p, hid))
                else:
                    link.bind("<Enter>", lambda e: self._show_tooltip(
                        e, "This concept is referenced but not yet minted in the mycelium. "
                           "It exists as an idea waiting to be formalized."))
                    link.bind("<Leave>", self._hide_tooltip)

        # ── Related To ────────────────────────────────────────────────
        related = full.get('related_to', [])
        if related:
            tk.Label(
                content, text="Related To",
                font=("Arial", 12, "bold"), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT
            ).pack(anchor="w", padx=25, pady=(15, 5))
            related_frame = tk.Frame(content, bg=theme.WHITE)
            related_frame.pack(anchor="w", padx=25, pady=(0, 10))
            for r in related:
                resolved = _resolve_human_id(r)
                if resolved is None:
                    link_text = f"📋 {r} (concept not yet in mycelium)"
                    link_fg = theme.DEEPSEEK_TEXT_LIGHT
                else:
                    link_text = f"🔗 {r}"
                    link_fg = theme.DEEPSEEK_INDIGO

                link = tk.Label(
                    related_frame, text=link_text,
                    font=("Arial", 10, "underline"), bg=theme.WHITE,
                    fg=link_fg, cursor="hand2"
                )
                link.pack(anchor="w", pady=1)
                if resolved:
                    link.bind("<Button-1>", lambda e, hid=r, p=popup: self._follow_link(p, hid))
                else:
                    link.bind("<Enter>", lambda e: self._show_tooltip(
                        e, "This concept is referenced but not yet minted in the mycelium. "
                           "It exists as an idea waiting to be formalized."))
                    link.bind("<Leave>", self._hide_tooltip)

        # ── Contradicts ───────────────────────────────────────────────
        contradicts = full.get('contradicts', [])
        if contradicts:
            tk.Label(
                content, text="Contradicts",
                font=("Arial", 12, "bold"), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT
            ).pack(anchor="w", padx=25, pady=(15, 5))
            contradicts_frame = tk.Frame(content, bg=theme.WHITE)
            contradicts_frame.pack(anchor="w", padx=25, pady=(0, 10))
            for c in contradicts:
                resolved = _resolve_human_id(c)
                if resolved is None:
                    link_text = f"📋 {c} (concept not yet in mycelium)"
                    link_fg = theme.DEEPSEEK_TEXT_LIGHT
                else:
                    link_text = f"🔗 {c}"
                    link_fg = theme.ERROR_RED

                link = tk.Label(
                    contradicts_frame, text=link_text,
                    font=("Arial", 10, "underline"), bg=theme.WHITE,
                    fg=link_fg, cursor="hand2"
                )
                link.pack(anchor="w", pady=1)
                if resolved:
                    link.bind("<Button-1>", lambda e, hid=c, p=popup: self._follow_link(p, hid))
                else:
                    link.bind("<Enter>", lambda e: self._show_tooltip(
                        e, "This concept is referenced but not yet minted in the mycelium. "
                           "It exists as an idea waiting to be formalized."))
                    link.bind("<Leave>", self._hide_tooltip)

        # ── Metadata ──────────────────────────────────────────────────
        metadata = full.get('metadata', {})
        if metadata:
            tk.Label(
                content, text="Metadata",
                font=("Arial", 12, "bold"), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT
            ).pack(anchor="w", padx=25, pady=(15, 5))

            meta_text = ""
            if metadata.get('created'):
                meta_text += f"Created: {metadata['created']}\n"
            if metadata.get('creator'):
                meta_text += f"Creator: {metadata['creator']}\n"
            if metadata.get('certainty_score') is not None:
                meta_text += f"Certainty: {metadata['certainty_score']}\n"
            if metadata.get('license'):
                meta_text += f"License: {metadata['license']}\n"
            if metadata.get('genesis'):
                meta_text += f"\nGenesis: {metadata['genesis']}"

            tk.Label(
                content, text=meta_text,
                font=("Arial", 9), bg=theme.DEEPSEEK_SURFACE_ALT,
                fg=theme.DEEPSEEK_TEXT_LIGHT, wraplength=580, justify=tk.LEFT,
                padx=15, pady=10
            ).pack(anchor="w", padx=25, pady=(0, 10))

        # ── Difficulty Levels ─────────────────────────────────────────
        difficulties = full.get('difficulty_levels', {})
        if difficulties:
            tk.Label(
                content, text="Difficulty Levels",
                font=("Arial", 12, "bold"), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT
            ).pack(anchor="w", padx=25, pady=(15, 5))

            for level in ['beginner', 'intermediate', 'expert']:
                if level in difficulties:
                    level_frame = tk.Frame(content, bg=theme.DEEPSEEK_SURFACE_ALT)
                    level_frame.pack(anchor="w", padx=25, pady=(5, 5), fill=tk.X)

                    tk.Label(
                        level_frame, text=f"  {level.title()}  ",
                        font=("Arial", 9, "bold"), bg=theme.DEEPSEEK_INDIGO,
                        fg=theme.WHITE, padx=6, pady=2
                    ).pack(anchor="w", padx=10, pady=(10, 5))

                    tk.Label(
                        level_frame, text=difficulties[level],
                        font=("Arial", 9), bg=theme.DEEPSEEK_SURFACE_ALT,
                        fg=theme.DEEPSEEK_TEXT, wraplength=560, justify=tk.LEFT,
                        padx=15, pady=(0, 10)
                    ).pack(anchor="w")

        # ── Human ID + CID ────────────────────────────────────────────
        tk.Label(
            content,
            text=f"\nHuman ID: {concept['human_id']}\nCID: {concept['cid']}",
            font=("Arial", 8), bg=theme.WHITE, fg=theme.DEEPSEEK_TEXT_LIGHT
        ).pack(anchor="w", padx=25, pady=(15, 25))

    # ── Navigation ─────────────────────────────────────────────────

    def _follow_link(self, popup, human_id):
        """Navigate to a related concept by human_id reference."""
        resolved = _resolve_human_id(human_id)
        if resolved is None:
            return

        concept = _load_full_concept(resolved)
        if concept is None:
            return

        new_concept = {
            'human_id': resolved,
            'cid': concept.get('cid', ''),
            'title': concept.get('title', resolved),
            'domain': concept.get('domain', 'Unknown'),
            'definition': concept.get('definition', ''),
            'type': concept.get('type', ''),
        }

        popup.history = popup.history[:popup.history_index + 1]
        popup.history.append(resolved)
        popup.history_index = len(popup.history) - 1

        self._build_popup_ui(popup, new_concept)

    def _navigate_history(self, popup, direction):
        """Go back or forward in the concept history."""
        new_index = popup.history_index + direction
        if new_index < 0 or new_index >= len(popup.history):
            return

        popup.history_index = new_index
        human_id = popup.history[new_index]
        concept = _load_full_concept(human_id)
        if concept is None:
            return

        new_concept = {
            'human_id': human_id,
            'cid': concept.get('cid', ''),
            'title': concept.get('title', human_id),
            'domain': concept.get('domain', 'Unknown'),
            'definition': concept.get('definition', ''),
            'type': concept.get('type', ''),
        }

        self._build_popup_ui(popup, new_concept)