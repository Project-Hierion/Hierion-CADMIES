from nicegui import ui
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
        
        # Normal UI with navigation
        @ui.page("/")
        def main_page():
            with ui.left_drawer().classes("bg-primary") as drawer:
                ui.label("CADMIES IPLD Explorer").classes("text-h6 text-white")
                ui.separator()
                ui.link("📊 Dashboard", "/dashboard").classes("text-white")
                ui.link("➕ Add Concept", "/add").classes("text-white")
                ui.link("📚 Browse Library", "/browse").classes("text-white")
                ui.link("📋 Audit Trail", "/audit").classes("text-white")
                ui.separator()
                ui.label(f"Store: {self.system.store_path}").classes("text-caption text-white")
            
            ui.navigate.to("/dashboard")
        
        # Register all pages
        @ui.page("/dashboard")
        def dashboard():
            DashboardPage(self.system).render()
        
        @ui.page("/add")
        def add():
            AddConceptPage(self.system).render()
        
        @ui.page("/browse")
        def browse():
            BrowsePage(self.system).render()
        
        @ui.page("/audit")
        def audit():
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
