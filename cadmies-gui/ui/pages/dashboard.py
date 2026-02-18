from nicegui import ui
import json
from datetime import datetime

class DashboardPage:
    def __init__(self, system):
        self.system = system
    
    def render(self):
        # Get system info
        info = self.system.get_system_info()
        
        # Load concepts
        index_path = self.system.get_index_path()
        concepts = {}
        if index_path.exists():
            with open(index_path) as f:
                concepts = json.load(f)
        
        # Count valid vs legacy
        valid_concepts = [k for k in concepts.keys() 
                         if not k.startswith(("old_", "legacy_"))]
        legacy_count = len(concepts) - len(valid_concepts)
        
        with ui.column().classes("w-full p-8"):
            # Header
            ui.label("CADMIES Dashboard").classes("text-h3")
            ui.label(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}").classes("text-italic")
            
            # System status card
            status_color = "positive" if info["status"] == "✅ Operational" else "negative"
            with ui.card().classes(f"w-full bg-{status_color} text-white"):
                with ui.row().classes("items-center"):
                    ui.icon("check_circle" if info["status"] == "✅ Operational" else "error", size="md")
                    ui.label(info["status"]).classes("text-h5")
                    ui.label(f"Path: {info['path']}").classes("text-caption ml-auto")
            
            # Stats cards
            with ui.row().classes("w-full gap-4"):
                with ui.card().classes("flex-1"):
                    ui.label("Total Concepts").classes("text-subtitle2")
                    ui.label(str(len(valid_concepts))).classes("text-h4")
                    if legacy_count > 0:
                        ui.label(f"(+{legacy_count} legacy)").classes("text-caption")
                
                with ui.card().classes("flex-1"):
                    ui.label("Storage").classes("text-subtitle2")
                    blocks = list(self.system.get_blocks_path().glob("*.cbor"))
                    total_size = sum(f.stat().st_size for f in blocks) / 1024
                    ui.label(f"{total_size:.2f} KB").classes("text-h4")
                
                with ui.card().classes("flex-1"):
                    ui.label("Schema").classes("text-subtitle2")
                    ui.label("v1.0.0").classes("text-h4")
                    ui.label("UniversalScientificConcept").classes("text-caption")
            
            # Quick actions
            ui.label("Quick Actions").classes("text-h5 mt-4")
            with ui.row().classes("gap-4"):
                ui.button("➕ New Concept", on_click=lambda: ui.navigate.to("/add")).props("color=primary")
                ui.button("📚 Browse Library", on_click=lambda: ui.navigate.to("/browse")).props("outline")
                ui.button("📋 View Audit", on_click=lambda: ui.navigate.to("/audit")).props("outline")
            
            # Recent activity
            ui.label("Recent Activity").classes("text-h5 mt-4")
            log_path = self.system.get_logs_path()
            if log_path.exists():
                with ui.card().classes("w-full"):
                    with open(log_path) as f:
                        lines = f.readlines()[-10:]
                    
                    for line in reversed(lines):
                        entry = json.loads(line)
                        with ui.row().classes("w-full items-center border-bottom py-2"):
                            time = ui.label(entry.get("timestamp", "")[11:19]).classes("w-20 font-mono")
                            
                            op = entry.get("operation", "")
                            op_color = "positive" if "add" in op else "primary"
                            ui.label(op).classes(f"w-32 text-{op_color} font-bold")
                            
                            ui.label(entry.get("human_id", "unknown")).classes("flex-1")
                            cid = entry.get("cid", "")
                            if cid:
                                ui.label(cid[:16] + "...").classes("font-mono text-caption")
            else:
                ui.label("No audit logs found").classes("text-italic")
