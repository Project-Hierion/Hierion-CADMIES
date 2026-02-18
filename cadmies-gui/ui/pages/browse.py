from nicegui import ui
from gui_tools.reader_wrapper import ConceptReader

class BrowsePage:
    def __init__(self, system):
        self.system = system
        self.reader = ConceptReader(system)
        self.search_query = ""
        self.view_mode = "grid"  # grid or list
    
    def render(self):
        # Get concepts
        concepts = self.reader.get_valid_concepts()
        
        with ui.column().classes("w-full p-8"):
            # Header
            with ui.row().classes("w-full items-center"):
                ui.label("Concept Library").classes("text-h3 flex-1")
                ui.label(f"{len(concepts)} concepts").classes("text-italic")
            
            # Search and filters
            with ui.row().classes("w-full items-center gap-4"):
                search_input = ui.input("🔍 Search concepts...") \
                    .classes("flex-1").props("outlined") \
                    .bind_value(self, "search_query")
                
                # View toggle
                with ui.button_group():
                    ui.button("📱", on_click=lambda: setattr(self, 'view_mode', 'grid')) \
                        .props(f"flat {'' if self.view_mode == 'grid' else 'outline'}")
                    ui.button("📋", on_click=lambda: setattr(self, 'view_mode', 'list')) \
                        .props(f"flat {'' if self.view_mode == 'list' else 'outline'}")
            
            # Apply search filter
            filtered = self.reader.search_concepts(self.search_query)
            
            # Results count
            ui.label(f"Showing {len(filtered)} results").classes("text-caption")
            
            # Display concepts
            if self.view_mode == "grid":
                with ui.grid(columns=3).classes("w-full gap-4 mt-4"):
                    for concept_id, cid in filtered.items():
                        self._render_grid_card(concept_id, cid)
            else:
                with ui.column().classes("w-full gap-2 mt-4"):
                    for concept_id, cid in filtered.items():
                        self._render_list_item(concept_id, cid)
    
    def _render_grid_card(self, concept_id, cid):
        with ui.card().classes("cursor-pointer hover:shadow-lg w-full"):
            ui.label(concept_id.replace('_', ' ').title()).classes("text-h6")
            ui.label(f"CID: {cid[:16]}...").classes("text-caption font-mono")
            
            async def view_details():
                content = await self.reader.read_concept_async(concept_id)
                with ui.dialog() as dialog, ui.card().classes("w-96 p-4 max-h-96 overflow-auto"):
                    ui.label(concept_id.replace('_', ' ').title()).classes("text-h5")
                    ui.separator()
                    ui.markdown(content)
                    ui.button("Close", on_click=dialog.close).props("flat").classes("mt-4")
                dialog.open()
            
            ui.button("View", on_click=view_details).props("flat").classes("mt-2")
    
    def _render_list_item(self, concept_id, cid):
        with ui.card().classes("w-full cursor-pointer hover:shadow-lg"):
            with ui.row().classes("w-full items-center p-2"):
                ui.label(concept_id.replace('_', ' ').title()).classes("text-h6 flex-1")
                ui.label(cid[:24] + "...").classes("font-mono text-caption")
                
                async def view_details(cid=cid, name=concept_id):
                    content = await self.reader.read_concept_async(name)
                    with ui.dialog() as dialog, ui.card().classes("w-96 p-4"):
                        ui.label(name.replace('_', ' ').title()).classes("text-h5")
                        ui.separator()
                        ui.markdown(content)
                        ui.button("Close", on_click=dialog.close)
                    dialog.open()
                
                ui.button("View", on_click=view_details).props("flat").classes("ml-4")
