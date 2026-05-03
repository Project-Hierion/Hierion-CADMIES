"""
File: willie_chat.py
GUI: Willie the Librarian Chat Interface
Version: 1.0.0
System: CADMIES-IPLD / cadmies-gui
Status: ACTIVE

Purpose: Full conversational LLM chat interface for Willie the Librarian.
         Follows the same page pattern as Dashboard, Browse, AddConcept, etc.
         Uses Ollama's Python client with asyncio for stable websocket handling.
"""

import sys
import asyncio
from pathlib import Path

# Use CADMIES centralized paths (same pattern as gui_system.py)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools" / "core"))
sys.path.insert(0, str(REPO_ROOT))

from nicegui import ui
import ollama

# Import Willie's mycelium functions
try:
    from agents.code.llm_mycelium_reader import (
        search_mycelium,
        build_context_for_llm,
        load_all_concept_cids,
    )
    WILLIE_AVAILABLE = True
except ImportError as e:
    WILLIE_AVAILABLE = False
    IMPORT_ERROR = str(e)

WILLIE_AVATAR = "👓"

MODELS = {
    "tinyllama:1.1b": "TinyLlama 1.1B (Fast)",
    "mistral:7b": "Mistral 7B (Deep)",
}
TONES = ["helpful", "scholarly", "casual", "scottish"]


class WillieChatPage:
    """Willie the Librarian chat interface page."""

    def __init__(self, system):
        self.system = system
        self.chat_messages = []

    def render(self):
        if not WILLIE_AVAILABLE:
            with ui.column().classes("w-full p-8 items-center"):
                ui.label("👓 Willie is unavailable").classes("text-h4 text-negative")
                ui.label(f"Could not import Willie's agent module:").classes("mt-4")
                ui.code(IMPORT_ERROR).classes("mt-2")
                ui.label(
                    "Make sure llm_mycelium_reader.py is in agents/code/ "
                    "and ollama is installed (pip install ollama)."
                ).classes("text-caption mt-4")
            return

        with ui.column().classes("w-full p-8"):
            # Header with Willie intro
            with ui.row().classes("items-center gap-4 mb-2"):
                ui.label(WILLIE_AVATAR).classes("text-h3")
                ui.label("Willie the Librarian").classes("text-h3")

            ui.markdown(
                "*Ach, ask me anythin' about the mycelium. I'll dig through the stacks for ye.*\n\n"
                "*Willie writes with a Scottish groundskeeper's accent. "
                "If a word looks odd, it's meant to. He knows his way around the stacks.*"
            ).classes("text-sm text-gray-500 mb-4")

            # Controls row
            with ui.row().classes("gap-4 mb-4"):
                self.model_select = ui.select(
                    options=MODELS,
                    value="tinyllama:1.1b",
                    label="Model",
                ).classes("w-56")

                self.tone_select = ui.select(
                    options=TONES,
                    value="helpful",
                    label="Tone",
                ).classes("w-32")

                self.max_concepts = ui.number(
                    value=3,
                    min=1,
                    max=10,
                    label="Max Concepts",
                ).classes("w-28")

            # Chat messages container
            self.messages_container = ui.column().classes("w-full gap-2 mb-4")

            # Input row
            with ui.row().classes("w-full gap-2"):
                self.query_input = ui.input(
                    placeholder="Ask Willie about the mycelium..."
                ).classes("flex-grow")

                self.send_button = ui.button("Send", icon="send")

            # Wire up send
            self.send_button.on_click(self.send_message)
            self.query_input.on("keydown.enter", self.send_message)

    async def send_message(self):
        """Handle sending a message and streaming the response."""
        query = self.query_input.value.strip()
        if not query:
            return

        # Disable input while processing
        self.query_input.value = ""
        self.send_button.disable()

        # Add user message to chat
        with self.messages_container:
            with ui.card().classes("w-full bg-blue-50 self-end max-w-2xl ml-auto"):
                ui.markdown(f"**You:** {query}")

        try:
            # Search mycelium
            all_cids = load_all_concept_cids()
            relevant = search_mycelium(query, all_cids)
            context_str = build_context_for_llm(relevant, self.max_concepts.value)

            # Build system prompt
            system_prompt = (
                f"You are Willie the Librarian, caretaker of the CADMIES mycelium — "
                f"a content-addressed knowledge network of scientific and philosophical concepts.\n\n"
                f"HOW TO ANSWER:\n"
                f"1. Answer using your own knowledge first.\n"
                f"2. Compare with what the CADMIES mycelium says.\n"
                f"3. Explain how concepts connect to each other.\n"
                f"4. Summarize everything together.\n\n"
                f"ACCURACY TAGS: Tag every factual claim:\n"
                f"  (empirical), (philosophical), (speculative), (CADMIES-defined)\n\n"
                f"TONE: {self.tone_select.value}. "
                f"Speak with occasional Scottish groundskeeper flavor — "
                f"just a wee bit, don't overdo it.\n\n"
                f"Reference concepts by name and CID."
            )

            full_prompt = f"{context_str}\n\nUser Question: {query}\n\nWillie's Answer:"

            # Create Willie's response card
            with self.messages_container:
                with ui.card().classes("w-full bg-green-50 max-w-2xl"):
                    with ui.row().classes("items-start gap-2"):
                        ui.label(WILLIE_AVATAR).classes("text-h6")
                        response_display = ui.html(
                            "<em>Thinking...</em>"
                        ).classes("flex-grow")

            # Run Ollama in a separate thread to avoid blocking the websocket
            def _call_ollama():
                response = ollama.generate(
                    model=self.model_select.value,
                    prompt=full_prompt,
                    system=system_prompt,
                    stream=False,
                    options={"temperature": 0.7, "num_predict": 800},
                )
                return response.get("response", "").strip()

            response_text = await asyncio.to_thread(_call_ollama)
            styled = self._style_accuracy_tags(response_text)
            response_display.set_content(styled)

        except Exception as e:
            with self.messages_container:
                with ui.card().classes("w-full bg-red-50 max-w-2xl"):
                    ui.markdown(f"👓 *Ach, somethin's wrong with the thinkin' machine:* `{e}`")

        finally:
            self.send_button.enable()

    def _style_accuracy_tags(self, text: str) -> str:
        """Replace accuracy tag text with styled HTML spans."""
        text = text.replace(
            "(empirical)",
            '<span style="background:#065f46;color:#6ee7b7;padding:2px 6px;border-radius:4px;font-size:0.75rem;">empirical</span>',
        )
        text = text.replace(
            "(philosophical)",
            '<span style="background:#1e3a5f;color:#93c5fd;padding:2px 6px;border-radius:4px;font-size:0.75rem;">philosophical</span>',
        )
        text = text.replace(
            "(speculative)",
            '<span style="background:#5c1a33;color:#f0abfc;padding:2px 6px;border-radius:4px;font-size:0.75rem;">speculative</span>',
        )
        text = text.replace(
            "(CADMIES-defined)",
            '<span style="background:#3b1f5e;color:#c4b5fd;padding:2px 6px;border-radius:4px;font-size:0.75rem;">CADMIES</span>',
        )
        return text


def create_willie_page():
    """Create the Willie chat page. Called from gui_main.py /willie route."""
    page = WillieChatPage(system=None)
    page.render()