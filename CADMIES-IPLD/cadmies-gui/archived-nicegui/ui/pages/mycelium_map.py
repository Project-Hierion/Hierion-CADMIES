from nicegui import ui
from pathlib import Path

class MyceliumPage:
    def __init__(self, system):
        self.system = system
    
    def render(self):
        with ui.column().classes("w-full p-8"):
            ui.label("Mycelium Map").classes("text-h3")
            ui.label("Knowledge graph of connected concepts").classes("text-italic mb-4")
            
            # Serve the HTML file
            html_path = Path("/workspaces/CADMIES/CADMIES-IPLD/mycelium_map.html")
            if html_path.exists():
                ui.html(html_path.read_text())
            else:
                ui.label("⚠️ Mycelium map not found. Run the relationship extraction script first.").classes("text-negative")
