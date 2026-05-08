import json
import os
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
            ui.label("Add New Concept").classes("text-h3")
            ui.label("Fields marked * are required. Others enrich the concept and can be added later by any gardener.").classes("text-italic text-grey-7")
            
            with ui.card().classes("w-full"):
                
                # === REQUIRED FIELDS ===
                ui.label("Required").classes("text-h6 text-primary")
                
                name = ui.input("Concept Name *").classes("w-full").props("outlined")
                name.tooltip("Will be converted to: lowercase_with_underscores")
                
                concept_type = ui.select(
                    label="Concept Type *",
                    options=[
                        "ScientificLaw",
                        "ScientificTheory",
                        "ScientificPrinciple",
                        "PhilosophicalPrinciple",
                        "PhilosophicalHypothesis",
                        "MetaphysicalPrinciple",
                        "MetaphysicalConcept",
                        "ThoughtExperiment",
                        "Paradox",
                        "MathematicalTheorem",
                        "CognitiveBias",
                        "Other"
                    ],
                    value="PhilosophicalPrinciple"
                ).classes("w-full").props("outlined")
                
                # Other type input (hidden by default)
                other_type = ui.input("Specify Type").classes("w-full mt-2").props("outlined")
                other_type.visible = False
                
                def on_type_change():
                    other_type.visible = (concept_type.value == "Other")
                concept_type.on('change', on_type_change)
                
                domain = ui.select(
                    label="Domain *",
                    options=[
                        "Physics",
                        "Biology",
                        "Mathematics",
                        "Epistemology",
                        "Philosophy",
                        "Metaphysics",
                        "Psychology",
                        "Economics",
                        "Medicine",
                        "Buddhist_Philosophy",
                        "Complexity_Science",
                        "Cognitive_Science",
                        "SystemsTheory",
                        "InformationTheory",
                        "ConsciousnessStudies",
                        "Testing",
                        "Other"
                    ],
                    value="Philosophy"
                ).classes("w-full").props("outlined")
                
                other_domain = ui.input("Specify Domain").classes("w-full mt-2").props("outlined")
                other_domain.visible = False
                
                def on_domain_change():
                    other_domain.visible = (domain.value == "Other")
                domain.on('change', on_domain_change)
                
                subdomain = ui.input("Subdomain *").classes("w-full").props("outlined")
                subdomain.tooltip("e.g., Classical Mechanics, Applied Ethics, Practice Theory")
                
                description = ui.textarea("Definition *").classes("w-full").props("outlined autogrow")
                description.tooltip("A clear, complete definition of the concept. 1-3 sentences recommended.")
                
                # === OPTIONAL FIELDS ===
                ui.separator()
                ui.label("Optional — Enrichment").classes("text-h6 text-grey-7")
                ui.label("These fields add depth. You or another gardener can fill them in later.").classes("text-italic text-grey-6 text-caption")
                
                axioms = ui.textarea("Axioms (Core Truths)").classes("w-full").props("outlined autogrow")
                axioms.tooltip("Core truths of the concept. One axiom per line. Multiple axioms accepted. e.g., 'Pleasant sensations are impermanent by nature.'")
                
                poetic_version = ui.input("Poetic Version").classes("w-full").props("outlined")
                poetic_version.tooltip("The concept distilled into one beautiful sentence. e.g., 'The bubbles fade, the thirst remains.'")
                
                mantra = ui.input("Mantra").classes("w-full").props("outlined")
                mantra.tooltip("A short, memorable phrase capturing the essence. e.g., 'Notice. Enjoy. Release.'")
                
                # === RELATIONSHIP FIELDS ===
                ui.separator()
                ui.label("Optional — Relationships").classes("text-h6 text-grey-7")
                ui.label("Link this concept to others in the mycelium. Use human_ids (snake_case). Enter one per line.").classes("text-italic text-grey-6 text-caption")
                
                builds_upon = ui.textarea("Builds Upon").classes("w-full").props("outlined autogrow")
                builds_upon.tooltip("Concepts this one directly extends. One human_id per line. Multiple entries accepted. e.g., 'craving_tanha_cycle'")
                
                related_to = ui.textarea("Related To").classes("w-full").props("outlined autogrow")
                related_to.tooltip("Concepts with meaningful connections. One human_id per line. Multiple entries accepted.")
                
                contradicts = ui.textarea("Contradicts").classes("w-full").props("outlined autogrow")
                contradicts.tooltip("Concepts or axioms this challenges. One per line. Multiple entries accepted.")
                
                # === METADATA FIELDS ===
                ui.separator()
                ui.label("Optional — Metadata").classes("text-h6 text-grey-7")
                
                certainty = ui.slider(min=0.0, max=1.0, step=0.01, value=0.8).classes("w-full")
                with ui.row().classes("items-center gap-2"):
                    ui.label("Certainty Score").classes("text-caption text-grey-7")
                    ui.icon("info").classes("text-grey-5").tooltip("How confident are you in this concept? 0.0 = wild guess, 1.0 = irrefutable truth. Use the slider above to adjust.")
                certainty_label = ui.label("0.80").classes("text-h6 text-primary")
                
                def on_certainty_change():
                    certainty_label.set_text(f"{certainty.value:.2f}")
                certainty.on('change', on_certainty_change)
                
                purpose = ui.select(
                    label="Purpose",
                    options=["educational", "research", "personal_knowledge"],
                    value="educational"
                ).classes("w-full").props("outlined")
                
                genesis = ui.textarea("Genesis (Origin Story)").classes("w-full").props("outlined autogrow")
                genesis.tooltip("How this concept came to be. e.g., 'Born from a conversation about Coca-Cola and Buddhist craving, May 2026.'")
                
                # === DIFFICULTY LEVELS ===
                ui.separator()
                ui.label("Optional — Difficulty Levels").classes("text-h6 text-grey-7")
                ui.label("Explain this concept at different levels of understanding.").classes("text-italic text-grey-6 text-caption")
                
                beginner_explanation = ui.textarea("Beginner").classes("w-full").props("outlined autogrow")
                beginner_explanation.tooltip("Explain like they're new to the domain. Simple language, concrete examples.")
                
                intermediate_explanation = ui.textarea("Intermediate").classes("w-full").props("outlined autogrow")
                intermediate_explanation.tooltip("For someone familiar with the domain. Use proper terminology, explore nuances.")
                
                expert_explanation = ui.textarea("Expert").classes("w-full").props("outlined autogrow")
                expert_explanation.tooltip("Full depth. Engage with edge cases, implications, and connections to other advanced concepts.")
                
                # === PREVIEW ===
                ui.separator()
                ui.label("Preview").classes("text-h6")
                
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
                    const name = document.querySelector('[aria-label="Concept Name *"]')?.value || '';
                    const conceptType = document.querySelector('[aria-label="Concept Type *"]')?.value || 'Not selected';
                    const domain = document.querySelector('[aria-label="Domain *"]')?.value || 'Not selected';
                    const subdomain = document.querySelector('[aria-label="Subdomain *"]')?.value || 'Not selected';
                    const description = document.querySelector('[aria-label="Definition *"]')?.value || '';
                    const axioms = document.querySelector('[aria-label="Axioms (Core Truths)"]')?.value || '';
                    const poetic = document.querySelector('[aria-label="Poetic Version"]')?.value || '';
                    const mantra = document.querySelector('[aria-label="Mantra"]')?.value || '';
                    
                    let humanId = name.toLowerCase().replace(/[^a-z0-9\\s-]/g, '').replace(/\\s+/g, '_');
                    if (!humanId) humanId = '[will be auto-generated]';
                    
                    let axiomList = '';
                    if (axioms) {
                        axiomList = '<ul>' + axioms.split('\\n').filter(a => a.trim()).map(a => '<li>' + a + '</li>').join('') + '</ul>';
                    }
                    
                    const previewDiv = document.getElementById('concept-preview');
                    if (previewDiv) {
                        previewDiv.innerHTML = `
                            <h3>${name || '[Concept Name]'}</h3>
                            <p><strong>Human ID:</strong> <code>${humanId}</code></p>
                            <p><strong>Type:</strong> ${conceptType}<br>
                            <strong>Domain:</strong> ${domain}<br>
                            <strong>Subdomain:</strong> ${subdomain}</p>
                            <p><strong>Definition:</strong><br>${description || '<em>No definition yet</em>'}</p>
                            ${axioms ? '<p><strong>Axioms:</strong></p>' + axiomList : ''}
                            ${poetic ? '<p><strong>Poetic Version:</strong> <em>' + poetic + '</em></p>' : ''}
                            ${mantra ? '<p><strong>Mantra:</strong> ' + mantra + '</p>' : ''}
                        `;
                    }
                }
                
                document.addEventListener('DOMContentLoaded', function() {
                    const fields = ['Concept Name *', 'Concept Type *', 'Domain *', 'Subdomain *', 'Definition *', 'Axioms (Core Truths)', 'Poetic Version', 'Mantra'];
                    fields.forEach(fieldLabel => {
                        const field = document.querySelector(`[aria-label="${fieldLabel}"]`);
                        if (field) {
                            field.addEventListener('blur', updatePreview);
                        }
                    });
                });
                </script>
                """)
                
                # === SUBMIT FUNCTION (defined before buttons that reference it) ===
                async def submit():
                    try:
                        # Build concept data with all fields
                        concept_data = {
                            "name": name.value,
                            "concept_type": other_type.value if concept_type.value == "Other" else concept_type.value,
                            "domain": other_domain.value if domain.value == "Other" else domain.value,
                            "subdomain": subdomain.value,
                            "description": description.value
                        }
                        
                        # Add optional fields if provided
                        if axioms.value:
                            concept_data["axioms"] = [a.strip() for a in axioms.value.split("\n") if a.strip()]
                        if poetic_version.value:
                            concept_data["poetic_version"] = poetic_version.value
                        if mantra.value:
                            concept_data["mantra"] = mantra.value
                        if builds_upon.value:
                            concept_data["builds_upon"] = [b.strip() for b in builds_upon.value.split("\n") if b.strip()]
                        if related_to.value:
                            concept_data["related_to"] = [r.strip() for r in related_to.value.split("\n") if r.strip()]
                        if contradicts.value:
                            concept_data["contradicts"] = [c.strip() for c in contradicts.value.split("\n") if c.strip()]
                        if beginner_explanation.value or intermediate_explanation.value or expert_explanation.value:
                            concept_data["difficulty_levels"] = {}
                            if beginner_explanation.value:
                                concept_data["difficulty_levels"]["beginner"] = beginner_explanation.value
                            if intermediate_explanation.value:
                                concept_data["difficulty_levels"]["intermediate"] = intermediate_explanation.value
                            if expert_explanation.value:
                                concept_data["difficulty_levels"]["expert"] = expert_explanation.value
                        concept_data["certainty_score"] = certainty.value
                        if purpose.value:
                            concept_data["purpose"] = purpose.value
                        if genesis.value:
                            concept_data["genesis"] = genesis.value
                        
                        # Validate with Pydantic
                        concept = Concept(**concept_data)
                        
                        # Show progress
                        with ui.dialog() as dialog, ui.card().classes("p-8 items-center"):
                            ui.label("Generating CID...").classes("text-h6")
                            ui.spinner(size="lg")
                        dialog.open()
                        
                        try:
                            cid = await self.cid_gen.generate_async(concept)
                            
                            # Save concept JSON to source_concepts/ for sharing/PR submission
                            source_concepts_dir = os.path.join(
                                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                "source_concepts"
                            )
                            os.makedirs(source_concepts_dir, exist_ok=True)
                            concept_json_path = os.path.join(source_concepts_dir, f"{concept.name}.json")
                            with open(concept_json_path, "w") as f:
                                json.dump(concept.to_json(), f, indent=2)
                            
                            dialog.close()
                            
                            # Success dialog
                            with ui.dialog() as success_dialog, ui.card().classes("p-8"):
                                ui.label("Concept Added Successfully").classes("text-h5 text-positive")
                                ui.markdown(f"""
**Name:** {name.value}
**Human ID:** `{concept.name}`
**CID:** `{cid}`

Stored locally in: `{self.system.get_blocks_path()}`

Concept JSON saved to: `source_concepts/{concept.name}.json`

---

**Want to submit this concept to CADMIES?**

1. Find your concept JSON at `source_concepts/{concept.name}.json`
2. Submit a Pull Request to [Hieros-CADMIES/CADMIES](https://github.com/Hieros-CADMIES/CADMIES)
3. A gardener will review and verify your CID — if it matches, your concept joins the mycelium forever.

*The CID is your cryptographic proof of authorship. If we generate the same CID, it's your house and the key fits.*
                                """)
                                ui.button("Close", on_click=success_dialog.close)
                            success_dialog.open()
                            
                            # Clear form on success
                            name.value = ""
                            concept_type.value = "PhilosophicalPrinciple"
                            domain.value = "Philosophy"
                            subdomain.value = ""
                            description.value = ""
                            axioms.value = ""
                            poetic_version.value = ""
                            mantra.value = ""
                            builds_upon.value = ""
                            related_to.value = ""
                            contradicts.value = ""
                            certainty.value = 0.8
                            purpose.value = "educational"
                            genesis.value = ""
                            beginner_explanation.value = ""
                            intermediate_explanation.value = ""
                            expert_explanation.value = ""
                            other_type.visible = False
                            other_domain.visible = False
                            preview.content = ""
                            
                        except Exception as e:
                            dialog.close()
                            ui.notify(f"Error: {str(e)}", type="negative", multi_line=True)
                    
                    except ValidationError as e:
                        for error in e.errors():
                            field_name = error['loc'][0] if error['loc'] else 'unknown'
                            ui.notify(f"{field_name}: {error['msg']}", type="warning")
                
                # === RESET FUNCTION ===
                def reset_form():
                    name.value = ""
                    concept_type.value = "PhilosophicalPrinciple"
                    domain.value = "Philosophy"
                    subdomain.value = ""
                    description.value = ""
                    axioms.value = ""
                    poetic_version.value = ""
                    mantra.value = ""
                    builds_upon.value = ""
                    related_to.value = ""
                    contradicts.value = ""
                    certainty.value = 0.8
                    purpose.value = "educational"
                    genesis.value = ""
                    beginner_explanation.value = ""
                    intermediate_explanation.value = ""
                    expert_explanation.value = ""
                    other_type.visible = False
                    other_domain.visible = False
                    preview.content = ""
                    ui.notify("Form cleared", type="info")
                
                # === BUTTONS ===
                with ui.row().classes("w-full justify-between mt-4"):
                    ui.button("Generate CID & Store", on_click=submit).props("color=primary size=large")
                    ui.button("Reset", on_click=reset_form).props("color=grey outline")