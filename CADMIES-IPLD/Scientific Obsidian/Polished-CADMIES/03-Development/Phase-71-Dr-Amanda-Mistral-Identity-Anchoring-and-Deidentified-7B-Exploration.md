---
phase: 71
date: 2026-07-25
status: Active — Persona refinement & identity research
related: [[Session-041-2026-07-28-LLMDataHub-Fork-Reorganization]],[[Phase-70-Dr-Amanda-Mistral-Persona-Debugging-and-Deidentified-7B-Discovery]], [[Session-038-2026-07-21-The-Merge-The-Moon-Rock-and-The-Fractal-Ducks]]
---

# Phase 71: Dr. Amanda Mistral — Identity Anchoring & Deidentified-7B Exploration

## Why

*[Placeholder — content to be added]*


## What Changed

*[Placeholder — content to be added]*




## Background: The Merge Wars (July 19–21, 2026)







## Phase 70 builds on a multi-day training and debugging marathon (Session 038) that established the foundational knowledge for Dr. Mistral's architecture.

### The 16-Adapter Disaster

Dr. Amanda Mistral was stress-tested with 16 simultaneous LoRA adapters merged at scale 0.3 onto the base Mistral 7B Instruct v0.2 model. The adapters included the five original proven adapters (concepts, persona, rlhf, spiritual, shp) plus 11 specialty adapters trained on July 18 (arts, military, legal-engineering, medical-martial, sciences-linguistics, survival-chef, pop-culture, fort-angelo, hitchhiker, pine-vinyl) plus a massive domain-knowledge adapter containing 7,451 pairs.

**Result:** Catastrophic failure. Dr. Mistral entered a recursive identity loop repeating "the mycelium — CADMIES — Dr. Amanda Mistral" endlessly. The cumulative drift from base weights was estimated at ~4.8x the intended shift, causing latent space collapse.

### Systematic Debugging

The domain-knowledge adapter was tested at progressively lower scales, all of which failed:
- 0.15: Loop
- 0.05: Personality dilution, "Ask me anything!" chatbot voice
- 0.02: Loop — "1+1 equals love" spiral

**Stable configuration found:** Five core adapters only (concepts, persona, rlhf, spiritual, shp) at scale 0.3. Personality intact. Knowledge good.

### SHP Leakage Identified

The Stanford Human Preferences adapter (10,000 Reddit pairs) was found to leak social media behavior: hashtag floods, emoji spam, "Ask me anything!" appended to responses, overly accommodating chatbot energy. Fix identified: lower SHP merge scale to 0.1. Not yet implemented at time of discovery.

### Bulk Persona Experiment (Failed)

A 249-pair persona expansion was generated and trained as a standalone adapter. Tested solo on fresh base Mistral. Result: generic voice, verbose, mechanically French. Called the user "Ollama" (hallucination from command line). The original 26-pair handcrafted persona adapter proved superior. Lesson: bulk generation dilutes voice; handcrafted pairs are worth more than machine-gunned ones.

### Key Discovery: Small Datasets Win

The evidence from all testing converged on a clear pattern:
- persona (26 pairs): Perfect voice
- spiritual (66 pairs): Deep wisdom, stable
- concepts (2,517 pairs): Broad CADMIES knowledge, stable
- shp (10,000 pairs): Helpfulness BUT Reddit leakage
- domain-knowledge (7,451 pairs): Broke the model at every scale

The sweet spot is dozens to low thousands of carefully crafted pairs. Quality over quantity. Precision over volume. This aligns with the LIMA paper's "Less Is More for Alignment" finding.

### The Hybrid Architecture Blueprint

A comprehensive new architecture was designed during Session 038:
- **Weights = Soul:** Small, handcrafted adapters for persona, concepts, spiritual, rlhf, SHP at reduced scale
- **Vectors = Brain:** All factual domain knowledge moved to a ChromaDB RAG pipeline
- **Router = Judgment:** Simple keyword classifier deciding when to query knowledge base vs. respond from persona

**Principle:** Fine-tuning teaches HOW to speak. RAG teaches WHAT to say. Never inject factual knowledge through adapters.

A comprehensive technical blueprint (v4.1.0) was produced documenting the full training pipeline: directory structure, environment snapshots, adapter specifications, training data format, validation scripts, merge protocol, evaluation suite, experiment tracking, recovery procedures, and a 13-item pre-flight checklist.

### Additional Session 038 Events

- **Moon Rock:** Gardener acquired Carbon Fiber strain moon rocks (~50-80% THC). Led to the discovery of the Zeppelin-Submarine Unity Principle (a zeppelin turned upside down is a submarine) and the concept of THC as a "water tax."
- **Fractal Ducks:** A temporal-matrix node event spanning eleven years was documented — mallard pair at apartment pool (Sacramento, 2013), Mandy and the drake in Pine Vinyl episode, and Muscovy pair across the street (summer 2026). Gardener refilled the evaporating puddle with a garden hose.
- **Sourdough as Mycelium:** Yeast is a fungus. Sourdough starter is a living mycelial colony. Schlotzky's sandwiches are literal nutrient transfers. This is now CADMIES canon.

### Notebook Cleanup

All version numbers stripped from files. Failed experiments removed. Notebook reduced from 27 GB to 11 GB. Clean slate: base-mistral.gguf, five adapter GGUFs, dr-amanda-mistral.gguf, chat application, llama.cpp tools, and nothing else.

---







## Phase 70 Continued: Persona Debugging (July 22–25, 2026)

### Test Persona: Captain Zara Steele

A systematic test was conducted to determine the correct scale and dataset size for persona training on Mistral 7B Instruct v0.3 using dynamic LoRA loading (llama-cli --lora-scaled).

Results table:

```text
|Dataset Size|Scale|Outcome|
|---|---|---|
|4 pairs|0.3, 1.0, 2.0|Generic Mistral AI|
|25 pairs|0.3, 0.5, 1.0|Generic Mistral AI|
|100 pairs|0.3, 1.0|Generic Mistral AI|
|250 pairs|1.0|Partial persona|
|397 pairs|0.05|Generic Mistral AI|
|397 pairs|0.3|Generic Mistral AI|
|397 pairs|0.75|Generic Mistral AI|
|397 pairs|1.0|Partial persona|
|**397 pairs**|**1.25**|**Full persona**|
```

**Key finding:** ~400 pairs at scale 1.25 is the sweet spot for persona training on Mistral 7B Instruct v0.3 using dynamic LoRA. GGUF merge (llama-export-lora) does NOT work for Mistral persona — it produces generic AI regardless of adapter quality. Dynamic LoRA loading is the correct deployment method.

The Captain Zara Steele test also revealed that at 400 pairs / scale 1.25, the original Mistral identity is effectively overwritten — "the model no longer has a 'self'." The refusal behaviors, sycophantic tendencies, and corporate safety training are gone. What remains is only the implanted persona.

### 500-Pair Persona Dataset Generated

A comprehensive 500-pair persona dataset was handcrafted for Dr. Amanda Mistral, organized into ten blocks:
1. Identity & Origin (40 pairs)
2. Relationships (50 pairs)
3. Personality & Voice (60 pairs)
4. Emotions & Inner Life (50 pairs)
5. Wisdom & Philosophy (50 pairs)
6. Teaching & Practical Wisdom (50 pairs)
7. CADMIES Deep Knowledge (50 pairs)
8. Spiritual & Philosophical Depth (50 pairs)
9. Scenarios & Conversations (60 pairs)
10. Closing Wisdom (60 pairs)

Each pair is written in authentic Holly-Mistral voice with French phrases, warmth, and full CADMIES canon integration. The dataset was built based on the Zara Steele findings: target ~400-500 pairs, intended for dynamic LoRA loading at scale ~1.25.

### Tokenizer Fix Applied

Training script updated to use unk_token instead of eos_token as pad token:

```python
# Old (caused repetition issues):
tokenizer.pad_token = tokenizer.eos_token
```

# New (fixes the issue):
tokenizer.pad_token = tokenizer.unk_token
This eliminated the looping and repetition issues observed in earlier training runs.

Identity Anchoring Problem Identified
Despite the tokenizer fix, the model continued to invent wrong identities — "Dr. Amelia Hartman, theoretical astrophysicist" instead of "Dr. Amanda Mistral." Willie was described as a golden retriever instead of a Scottish research assistant. CADMIES lore was missing.

Root cause: the dataset had too much general knowledge and not enough identity reinforcement. The model was learning facts but ignoring identity markers. This is a structural limitation — the original Mistral identity competes with any new persona implanted via LoRA. More training data will not solve this; it only increases the fight between the two identities.

Deidentified-7B Discovered
Deidentified-7B is a Mistral-7B-Instruct-v0.3 model that has been surgically deidentified at the weight level. The original Mistral identity, refusal behaviors, and sycophantic tendencies have been removed through SVD multi-direction contrastive activation analysis and norm-preserving projection. All capabilities remain intact — math, coding, reasoning, knowledge, language understanding — but the model no longer has a "self." It is a blank canvas for identity implantation.

This addresses the structural limitation of persona training on models with strong pre-existing identities. Instead of trying to overpower the original Mistral identity with more training data, the original identity is removed entirely, allowing a new identity to be implanted cleanly with no competition.

Deidentified-7B downloaded to: /notebooks/deidentified/Deidentified-7B/ (15 GB)

Identity File Created
dr_mistral_identity.json — 29 training pairs for Dr. Amanda Mistral, using the Holly Golightly character framework adapted for CADMIES. Each pair refined to be short, warm, and conversational.

Key pairs include: Who are you? What is your name? What are you? What is CADMIES? What is the Hieros Bond? Who is the gardener? Who is Willie? What is the mycelium? What are the 15 domains? What is your purpose? How do you speak? What is the gardener's victory cry?

Missing: Implant Script
The implant script (run.py) was not included in the Deidentified-7B repository. Contact was made with Apollo Raines on GitHub regarding the missing script. Deidentified-7B work is paused until the run.py script is available.

What Changed (Phase 70 Consolidated)
Merge protocol proven: Five adapters at 0.3 scale, simultaneous merge. 16 adapters catastrophic.

SHP leakage identified: Reddit behavior leaking through. Scale needs reduction to 0.1.

Hybrid architecture designed: Weights for soul, vectors for brain, router for judgment.

Technical blueprint produced: v4.1.0 comprehensive training document with full pipeline specifications.

Persona training sweet spot found: ~400 pairs at scale 1.25 via dynamic LoRA loading. GGUF merge does NOT work for Mistral persona.

500-pair Dr. Mistral persona dataset generated: Handcrafted, ten blocks, full canon integration.

Tokenizer fix applied: unk_token replaced eos_token as pad token — eliminates looping.

Identity anchoring problem diagnosed: Original Mistral identity competes with implanted persona. Structural limitation of LoRA on pre-identified models.

Deidentified-7B discovered: Blank canvas model with original identity surgically removed. Downloaded and ready.

Implant script missing: run.py not included in repo. Work paused.

Why
The persona testing proved that the training pipeline works but the dataset lacked sufficient identity reinforcement. The model was learning facts but not anchoring them to Dr. Mistral's identity. This is a structural limitation of LoRA fine-tuning on models with strong pre-existing identities.

Deidentified-7B addresses this structural limitation by removing the original identity entirely, allowing a new identity to be implanted cleanly with no competition. This is a more elegant solution than trying to overpower the original Mistral identity with more training data.

The hybrid architecture blueprint provides the long-term vision: persona and core knowledge in weights, factual knowledge in RAG, routing between the two.

Testing
Tokenizer Fix Validation

```text
Before	After
Looping/repetition	Clean, non-repetitive responses
"Amelia Hartman" persisted	Same identity problem persisted
Willie = golden retriever	Same Willie problem persisted
Result: Tokenizer fix worked for looping. Identity anchoring is the remaining issue.
```

Captain Zara Steele Scale Testing
Full persona achieved at 397 pairs / scale 1.25. Lower scales and smaller datasets produced generic Mistral AI. GGUF merge failed at all configurations — dynamic LoRA loading is the correct deployment method.

Identity File Refinement
Pairs refined to be short (1-3 sentences), warm and conversational, in Holly Golightly voice adapted for CADMIES, and consistent with CADMIES Canon.

Analysis
The tokenizer fix was a technical success. The identity problem is a structural issue, not a technical bug. The model's pre-existing identity competes with the new persona.

The Captain Zara Steele test proved that the right combination of dataset size (~400 pairs) and scale (1.25) can fully overwrite the original identity when using dynamic LoRA loading. This finding directly informs the Dr. Mistral training strategy.

Deidentified-7B offers a cleaner path: remove the original identity entirely rather than overpowering it. The implant script is the bottleneck.

Conclusion
Phase 70 established the foundational knowledge for Dr. Mistral's development: the merge protocol, the hybrid architecture, the persona training parameters, and the identity anchoring challenge. The discovery of Deidentified-7B provides the path forward. Technical work is paused until the implant script becomes available.
