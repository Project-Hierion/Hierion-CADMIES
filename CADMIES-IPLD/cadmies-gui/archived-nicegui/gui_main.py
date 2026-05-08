import sys
from pathlib import Path
import json
from operator import index

from nicegui import ui
from fastapi.staticfiles import StaticFiles

# === PATH SETUP: Make tools/core importable from GUI ===
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools" / "core"))

# Now we can use the centralized paths
from paths import PROJECT_ROOT, STORE_DIR, BLOCKS_DIR, ensure_dirs

# === GUI IMPORTS ===
from gui_system import CadmiesSystem
from ui.pages.dashboard import DashboardPage
from ui.pages.add_concept import AddConceptPage
from ui.pages.browse import BrowsePage
from ui.pages.audit import AuditPage

class CadmiesApp:
    def __init__(self):
        self.system = CadmiesSystem()
        self.init_ui()
    
    def init_ui(self):
        # Verify CADMIES system first
        system_ok, checks = self.system.verify_system()
        
        if not system_ok:
            # Show detailed error page
            @ui.page("/")
            def error_page():
                with ui.column().classes("w-full p-8 items-center"):
                    ui.label("❌ CADMIES System Not Found").classes("text-h3 text-negative")
                    ui.label("Expected structure:").classes("text-h6 mt-4")
                    ui.code("""
your-cadmies-root/
└── tools/
    └── core/
        ├── store/
        │   ├── blocks/
        │   ├── index/
        │   └── logs/
        ├── cid_generator_v1.1.0.py
        └── cbor_reader.py
                    """)
                    ui.label(f"Current path: {self.system.base_path}").classes("font-mono")
                    
                    ui.label("Missing components:").classes("text-h6 mt-4")
                    for component, exists in checks.items():
                        icon = "✅" if exists else "❌"
                        ui.label(f"{icon} {component}")
            return
        
        # Serve static files for mycelium map (NOW PORTABLE!)
        from nicegui import app
        app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT)), name="static")

        # ========== HOME PAGE (Landing Page) ==========
        @ui.page("/")
        def home_page():
            # Sidebar drawer
            with ui.left_drawer().classes("bg-primary") as drawer:
                ui.label("CADMIES IPLD Explorer").classes("text-h6 text-white")
                ui.separator()
                ui.link("🏠 Home", "/").classes("text-white")
                ui.link("📊 Dashboard", "/dashboard").classes("text-white")
                ui.link("➕ Add Concept", "/add").classes("text-white")
                ui.link("📚 Browse Library", "/browse").classes("text-white")
                ui.link("📋 Audit Trail", "/audit").classes("text-white")
                ui.link("🕸️ Mycelium Map", "/static/mycelium_map.html").classes("text-white").props("target=_blank")
                ui.separator()
                ui.label(f"Store: {self.system.store_path}").classes("text-caption text-white")
            
            # Main content area
            with ui.column().classes("w-full p-8"):
                ui.label("Welcome to CADMIES").classes("text-h3")
                ui.label("Select an option from the sidebar to begin.").classes("text-italic")
                # Count concepts from the index file directly
                import json
                index_path = self.system.get_index_path()
                if index_path.exists():
                    with open(index_path) as f:
                        index = json.load(f)
                    concept_count = len(index)
                else:
                    concept_count = 0
                ui.label(f"📚 {concept_count} concepts available").classes("mt-4")
        
        # ========== DASHBOARD PAGE ==========
        @ui.page("/dashboard")
        def dashboard():
            with ui.left_drawer().classes("bg-primary") as drawer:
                ui.label("CADMIES IPLD Explorer").classes("text-h6 text-white")
                ui.separator()
                ui.link("🏠 Home", "/").classes("text-white")
                ui.link("📊 Dashboard", "/dashboard").classes("text-white")
                ui.link("➕ Add Concept", "/add").classes("text-white")
                ui.link("📚 Browse Library", "/browse").classes("text-white")
                ui.link("📋 Audit Trail", "/audit").classes("text-white")
                ui.link("🕸️ Mycelium Map", "/static/mycelium_map.html").classes("text-white").props("target=_blank")
                ui.separator()
                ui.label(f"Store: {self.system.store_path}").classes("text-caption text-white")
            DashboardPage(self.system).render()
        
        # ========== ADD CONCEPT PAGE ==========
        @ui.page("/add")
        def add():
            with ui.left_drawer().classes("bg-primary") as drawer:
                ui.label("CADMIES IPLD Explorer").classes("text-h6 text-white")
                ui.separator()
                ui.link("🏠 Home", "/").classes("text-white")
                ui.link("📊 Dashboard", "/dashboard").classes("text-white")
                ui.link("➕ Add Concept", "/add").classes("text-white")
                ui.link("📚 Browse Library", "/browse").classes("text-white")
                ui.link("📋 Audit Trail", "/audit").classes("text-white")
                ui.link("🕸️ Mycelium Map", "/static/mycelium_map.html").classes("text-white").props("target=_blank")
                ui.separator()
                ui.label(f"Store: {self.system.store_path}").classes("text-caption text-white")
            AddConceptPage(self.system).render()
        
        # ========== BROWSE PAGE ==========
        @ui.page("/browse")
        def browse():
            with ui.left_drawer().classes("bg-primary") as drawer:
                ui.label("CADMIES IPLD Explorer").classes("text-h6 text-white")
                ui.separator()
                ui.link("🏠 Home", "/").classes("text-white")
                ui.link("📊 Dashboard", "/dashboard").classes("text-white")
                ui.link("➕ Add Concept", "/add").classes("text-white")
                ui.link("📚 Browse Library", "/browse").classes("text-white")
                ui.link("📋 Audit Trail", "/audit").classes("text-white")
                ui.link("🕸️ Mycelium Map", "/static/mycelium_map.html").classes("text-white").props("target=_blank")
                ui.separator()
                ui.label(f"Store: {self.system.store_path}").classes("text-caption text-white")
            BrowsePage(self.system).render()
        
        # ========== AUDIT PAGE ==========
        @ui.page("/audit")
        def audit():
            with ui.left_drawer().classes("bg-primary") as drawer:
                ui.label("CADMIES IPLD Explorer").classes("text-h6 text-white")
                ui.separator()
                ui.link("🏠 Home", "/").classes("text-white")
                ui.link("📊 Dashboard", "/dashboard").classes("text-white")
                ui.link("➕ Add Concept", "/add").classes("text-white")
                ui.link("📚 Browse Library", "/browse").classes("text-white")
                ui.link("📋 Audit Trail", "/audit").classes("text-white")
                ui.link("🕸️ Mycelium Map", "/static/mycelium_map.html").classes("text-white").props("target=_blank")
                ui.separator()
                ui.label(f"Store: {self.system.store_path}").classes("text-caption text-white")
            AuditPage(self.system).render()
    
    def run(self):
        ui.run(
            title="CADMIES IPLD Explorer",
            favicon="📚",
            dark=False,
            port=8081,
            show=True,
            reload=False
        )

if __name__ == "__main__":
    app = CadmiesApp()
    app.run()
