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
                    ],
                    value="MetaphysicalPrinciple"
                ).classes("w-full").props("outlined")
                
                domain = ui.select(
                    label="Domain *",
                    options=[
                        "Metaphysics",
                        "SystemsTheory",
                        "InformationTheory",
                        "ConsciousnessStudies",
                        "Testing"
                    ],
                    value="Metaphysics"
                ).classes("w-full").props("outlined")
                
                subdomain = ui.input("Subdomain *").classes("w-full").props("outlined")
                description = ui.textarea("Description *").classes("w-full").props("outlined autogrow")
                
                                # Preview
                ui.separator()
                ui.label("Preview").classes("text-h6")
                
                # HTML preview container (replaces markdown)
                preview = ui.html("""
                    <div id="concept-preview" class="w-full bg-grey-1 p-4 rounded border">
                        <h3>Preview will appear here</h3>
                        <p>Fill in the form above, then click out of each field to see the preview update.</p>
                    </div>
                """).classes("w-full")
                
                # Inject JavaScript for local preview updates
                ui.add_body_html("""
                <script>
                function updatePreview() {
                    // Get form values
                    const name = document.querySelector('[aria-label="Concept Name *"]')?.value || '';
                    const conceptType = document.querySelector('[aria-label="Concept Type *"]')?.value || 'Not selected';
                    const domain = document.querySelector('[aria-label="Domain *"]')?.value || 'Not selected';
                    const subdomain = document.querySelector('[aria-label="Subdomain *"]')?.value || 'Not selected';
                    const description = document.querySelector('[aria-label="Description *"]')?.value || '';
                    
                    // Generate human_id
                    let humanId = name.toLowerCase().replace(/[^a-z0-9\s-]/g, '').replace(/\\s+/g, '_');
                    if (!humanId) humanId = '[will be auto-generated]';
                    
                    // Update preview HTML
                    const previewDiv = document.getElementById('concept-preview');
                    if (previewDiv) {
                        previewDiv.innerHTML = `
                            <h3>${name || '[Concept Name]'}</h3>
                            <p><strong>Human ID:</strong> <code>${humanId}</code></p>
                            <p><strong>Type:</strong> ${conceptType}<br>
                            <strong>Domain:</strong> ${domain}<br>
                            <strong>Subdomain:</strong> ${subdomain}</p>
                            <p><strong>Description:</strong><br>${description || '<em>No description yet</em>'}</p>
                        `;
                    }
                }
                
                // Add blur event listeners to all form fields
                document.addEventListener('DOMContentLoaded', function() {
                    const fields = ['Concept Name *', 'Concept Type *', 'Domain *', 'Subdomain *', 'Description *'];
                    fields.forEach(fieldLabel => {
                        const field = document.querySelector(`[aria-label="${fieldLabel}"]`);
                        if (field) {
                            field.addEventListener('blur', updatePreview);
                        }
                    });
                });
                </script>
                """)
                               
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
