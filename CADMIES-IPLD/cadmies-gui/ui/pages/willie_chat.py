"""
File: willie_chat.py
GUI: Willie the Librarian Chat Interface
Version: 1.0.2
System: CADMIES-IPLD / cadmies-gui
Status: ACTIVE

Changelog 1.0.2:
  - Sequential Ollama calls (CPU-only — one at a time)
  - 1-second delay between semantic search and main query
  - Keyword-only fallback if semantic search fails
  - Restored working v1.0.0 callback pattern
"""

import sys
import asyncio
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools" / "core"))
sys.path.insert(0, str(REPO_ROOT))

from nicegui import ui
import ollama

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
            with ui.row().classes("items-center gap-4 mb-2"):
                ui.label(WILLIE_AVATAR).classes("text-h3")
                ui.label("Willie the Librarian").classes("text-h3")

            ui.markdown(
                "*Ach, ask me anythin' about the mycelium. I'll dig through the stacks for ye.*\n\n"
                "*Willie writes with a Scottish groundskeeper's accent. "
                "If a word looks odd, it's meant to. He knows his way around the stacks.*"
            ).classes("text-sm text-gray-500 mb-4")

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

            self.messages_container = ui.column().classes("w-full gap-2 mb-4")

            with ui.row().classes("w-full gap-2"):
                self.query_input = ui.input(
                    placeholder="Ask Willie about the mycelium..."
                ).classes("flex-grow")

                self.send_button = ui.button("Send", icon="send")

            self.send_button.on_click(self.send_message)
            self.query_input.on("keydown.enter", self.send_message)

    async def send_message(self):
        """Handle sending a message. Sequential Ollama calls for CPU-only system."""
        query = self.query_input.value.strip()
        if not query:
            return

        self.query_input.value = ""
        self.send_button.disable()

        with self.messages_container:
            with ui.card().classes("w-full bg-blue-50 self-end max-w-2xl ml-auto"):
                ui.markdown(f"**You:** {query}")

        # Create response card
        with self.messages_container:
            with ui.card().classes("w-full bg-green-50 max-w-2xl"):
                with ui.row().classes("items-start gap-2"):
                    ui.label(WILLIE_AVATAR).classes("text-h6")
                    response_display = ui.html(
                        "<em>Searching the mycelium...</em>"
                    ).classes("flex-grow")

        try:
            # Step 1: Keyword search (fast, no Ollama call)
            all_cids = load_all_concept_cids()
            relevant = search_mycelium(query, all_cids, use_semantic=False)
            context_str = build_context_for_llm(relevant, self.max_concepts.value)

            # Step 2: Attempt semantic search separately (uses Ollama — wait for it)
            try:
                response_display.set_content("<em>Expanding search with semantic context...</em>")
                def _semantic_search():
                    return search_mycelium(query, all_cids, use_semantic=True)
                
                relevant = await asyncio.to_thread(_semantic_search)
                context_str = build_context_for_llm(relevant, self.max_concepts.value)
            except Exception:
                pass  # Semantic search failed — keyword results are fine

            # Step 3: Brief pause so Ollama finishes any lingering work
            await asyncio.sleep(1)

            # Step 4: Build prompt and call Ollama for the main answer
            response_display.set_content("<em>Formulating answer...</em>")

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
                f"TONE: {self.tone_select.value}. "
                f"Speak with occasional Scottish groundskeeper flavor.\n\n"
                f"If the mycelium doesn't have relevant concepts, say so honestly."
            )

            full_prompt = f"{context_str}\n\nUser Question: {query}\n\nWillie's Answer:"

            def _call_ollama():
                response = ollama.generate(
                    model=self.model_select.value,
                    prompt=full_prompt,
                    system=system_prompt,
                    stream=False,
                    options={"temperature": 0.7, "num_predict": 500},
                )
                return response.get("response", "").strip()

            response_text = await asyncio.to_thread(_call_ollama)
            response_display.set_content(response_text)

        except Exception as e:
            response_display.set_content(
                f"👓 *Ach, somethin's wrong:* `{e}`"
            )

        finally:
            self.send_button.enable()


def create_willie_page():
    """Create the Willie chat page. Called from gui_main.py /willie route."""
    page = WillieChatPage(system=None)
    page.render()