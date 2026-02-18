# Contributing to CADMIES GUI

## Step-by-Step Example: Adding a "Concept Map" Page

### 1. Create the Page File

**File:** `ui/pages/concept_map.py`

from nicegui import ui
from gui_system import CadmiesSystem

class ConceptMapPage:
    def __init__(self, system: CadmiesSystem):
        self.system = system
        self.concepts = []
        
    def render(self):
        # Load concepts from index
        import json
        index_path = self.system.get_index_path()
        if index_path.exists():
            with open(index_path) as f:
                self.concepts = list(json.load(f).keys())
        
        with ui.column().classes("w-full p-8"):
            ui.label("Concept Map").classes("text-h3")
            ui.label("Visual relationship between concepts").classes("text-italic")
            
            # Simple list for now (could be a graph later)
            with ui.row().classes("w-full gap-4 flex-wrap"):
                for concept in self.concepts[:20]:
                    with ui.card().classes("cursor-pointer hover:shadow-lg"):
                        ui.label(concept.replace('_', ' ').title())
                        
                        async def view_concept(c=concept):
                            ui.navigate.to(f"/browse?q={c}")
                        
                        ui.button("View", on_click=view_concept).props("flat")

2. Register in gui_main.py

Find the section where pages are registered (around line 40-60) and add:
python

from ui.pages.concept_map import ConceptMapPage  # Add this import

# In the init_ui method, with other page registrations:
@ui.page("/concept-map")
def concept_map():
    ConceptMapPage(self.system).render()

3. Add to Navigation Drawer

Find the navigation drawer section (around line 30-40) and add:
python

with ui.left_drawer().classes("bg-primary") as drawer:
    ui.label("CADMIES IPLD Explorer").classes("text-h6 text-white")
    ui.separator()
    ui.link("📊 Dashboard", "/dashboard").classes("text-white")
    ui.link("➕ Add Concept", "/add").classes("text-white")
    ui.link("📚 Browse Library", "/browse").classes("text-white")
    ui.link("🗺️ Concept Map", "/concept-map").classes("text-white")  # Add this line
    ui.link("📋 Audit Trail", "/audit").classes("text-white")
    ui.separator()
    ui.label(f"Store: {self.system.store_path}").classes("text-caption text-white")

4. Optional: Add Query Parameters

For pages that accept parameters (like /browse?q=consciousness):
python

@ui.page("/browse")
def browse():
    # Get query parameter
    query = ui.query.get("q", "")
    BrowsePage(self.system, initial_query=query).render()
    
# Then in your page class __init__, accept the parameter
def __init__(self, system, initial_query=""):
    self.system = system
    self.initial_query = initial_query

Complete Pattern Summary

# 1. CREATE (ui/pages/yourpage.py)
class YourPage:
    def __init__(self, system):
        self.system = system
    
    def render(self):
        with ui.column():
            ui.label("Your Content")

# 2. REGISTER (gui_main.py)
from ui.pages.yourpage import YourPage

@ui.page("/your-route")
def your_page():
    YourPage(self.system).render()

# 3. LINK (navigation drawer)
ui.link("🚀 Your Page", "/your-route").classes("text-white")

That's it. The page appears in navigation and is accessible at http://localhost:8081/your-route.
Development Guidelines

    No hardcoded paths – Use CadmiesSystem methods

    Maintain air-gap – No network calls without explicit user consent

    Async for I/O – Use async/await for file/subprocess operations

    Follow naming – snake_case for files, PascalCase for classes

    Add to navigation – Always include a link in the drawer

Testing Your Changes

    Run the GUI locally:

cd gui
python gui_main.py

    Navigate to your new page

    Verify all functionality

    Check console for errors

Submitting a Pull Request

    Create a feature branch from main

    Make your changes

    Test thoroughly

    Submit PR with clear description

    Reference any related issues or roadmap items

Questions? Open an issue or start a discussion.
