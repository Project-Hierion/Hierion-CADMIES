from nicegui import ui
from gui_concept import Concept
from gui_tools.cid_wrapper import CIDGenerator
from pydantic import ValidationError

class AddConceptPage:
    def __init__(self, system):
        self.system = system
        self.cid_gen = CIDGenerator(system)
        
    def render(self):
        with ui.column().classes("w-full p-8"):
            ui.label("Add New Metaphysical Concept").classes("text-h3")
            ui.label("All fields required").classes("text-italic")
            
            # Form
            with ui.card().classes("w-full"):
                name = ui.input("Concept Name *").classes("w-full").props("outlined")
                name.tooltip("Will be converted to: lowercase_with_underscores")
                
                concept_type = ui.select(
                    label="Concept Type *",
                    options=[
                        "MetaphysicalPrinciple",
                        "PhilosophicalHypothesis", 
                        "PhilosophicalTheory",
                        "MechanisticPrinciple",
                        "MetaphysicalConcept",
                        "TestConcept"
                    ]
                ).classes("w-full").props("outlined")
                
                domain = ui.select(
                    label="Domain *",
                    options=[
                        "Metaphysics",
                        "SystemsTheory",
                        "InformationTheory",
                        "ConsciousnessStudies",
                        "Testing"
                    ]
                ).classes("w-full").props("outlined")
                
                subdomain = ui.input("Subdomain *").classes("w-full").props("outlined")
                description = ui.textarea("Description *").classes("w-full").props("outlined autogrow")
                
                # Preview
                ui.separator()
                ui.label("Preview").classes("text-h6")
                preview = ui.markdown().classes("w-full bg-grey-1 p-4 rounded border")
                
                def update_preview():
                    import re
                    human_id = re.sub(r'[^a-zA-Z0-9\s-]', '', name.value or "")
                    human_id = human_id.lower().replace(' ', '_')
                    
                    preview.set_content(f"""
# {name.value or '[Concept Name]'}
**Human ID:** `{human_id or '[will be auto-generated]'}`

**Type:** {concept_type.value or 'Not selected'}  
**Domain:** {domain.value or 'Not selected'}  
**Subdomain:** {subdomain.value or 'Not selected'}  

{description.value or '*Description will appear here*'}
                    """)
                
                # Live preview updates
                name.on("input", update_preview)
                concept_type.on("change", update_preview)
                domain.on("change", update_preview)
                subdomain.on("input", update_preview)
                description.on("input", update_preview)
                
                # Submit button
                async def submit():
                    try:
                        # Validate with Pydantic
                        concept = Concept(
                            name=name.value,
                            concept_type=concept_type.value,
                            domain=domain.value,
                            subdomain=subdomain.value,
                            description=description.value
                        )
                        
                        # Show progress
                        with ui.dialog() as dialog, ui.card().classes("p-8 items-center"):
                            ui.label("Generating CID...").classes("text-h6")
                            ui.spinner(size="lg")
                        dialog.open()
                        
                        try:
                            cid = await self.cid_gen.generate_async(concept)
                            dialog.close()
                            
                            # Success dialog
                            with ui.dialog() as success_dialog, ui.card().classes("p-8"):
                                ui.label("✅ Concept Added Successfully").classes("text-h5 text-positive")
                                ui.markdown(f"""
**Name:** {name.value}
**Human ID:** `{concept.name}`
**CID:** `{cid}`

Stored in: `{self.system.get_blocks_path()}`
                                """)
                                ui.button("Close", on_click=success_dialog.close)
                                ui.button("Add Another", on_click=lambda: (success_dialog.close(), None))
                            success_dialog.open()
                            
                            # Clear form
                            name.value = ""
                            concept_type.value = None
                            domain.value = None
                            subdomain.value = ""
                            description.value = ""
                            preview.set_content("")
                            
                        except Exception as e:
                            dialog.close()
                            ui.notify(f"Error: {str(e)}", type="negative", multi_line=True)
                    
                    except ValidationError as e:
                        # Show validation errors
                        for error in e.errors():
                            ui.notify(f"{error['loc'][0]}: {error['msg']}", type="warning")
                
                ui.button("Generate CID & Store", on_click=submit).props("color=primary size=large").classes("mt-4")
