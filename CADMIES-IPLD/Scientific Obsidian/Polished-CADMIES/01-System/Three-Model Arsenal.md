---
system: CADMIES
date: 2026-05-15
status: Active
related: [[Architecture Overview]], [[Harvester Pipeline]], [[Two-System Setup]]
---
# Three-Model Arsenal
CADMIES uses three Ollama models on the Paperspace GPU, each with a specific role. The right model for the right task.
## The Arsenal
| Model | Size | VRAM Usage | Role | Strengths |
|-------|------|------------|------|-----------|
| TinyLlama 1.1B | 637MB | ~1GB | Quick searches, lightweight tasks | Fast, runs on CPU if needed |
| Mistral 7B | 4.4GB | ~6GB | Extraction workhorse, relationship generation | Balanced speed and quality, good at structured output |
| Codestral 22B | 12GB | ~14GB | Deep philosophy, library audits, precision edges | Highest quality reasoning, best for complex relationships |
## Model Selection Guide
### Use TinyLlama When:
- Testing pipeline code (fast feedback)
- Quick mycelium searches
- CPU-only environments
- The task doesn't require deep reasoning
### Use Mistral When:
- Harvesting concepts from conversations (primary use case)
- Generating relationships between concepts
- Any structured JSON extraction
- Default for all harvest operations
### Use Codestral When:
- Deep philosophical analysis
- Library audits and quality checks
- Complex edge discovery between unrelated domains
- Enrichment pass (Phase 2 of extraction)
- When Mistral's output feels shallow
## Model Commands

```bash
# Pull models (Paperspace)
ollama pull mistral:7b
ollama pull codestral:22b
ollama pull tinyllama:1.1b
```

# Use with harvester

```bash
python harvest/harvest_full_pipeline.py --model mistral:7b
python harvest/harvest_full_pipeline.py --model codestral
python harvest/harvest_full_pipeline.py --model tinyllama:1.1b
```
## Performance Notes

- Mistral 7B at Q4_K_M quantization uses ~4.5GB VRAM. Fits on GPUs as small as GTX 1660 (6GB).
    
- Codestral 22B requires 12GB+ VRAM. Minimum RTX 3060 12GB or A4000.
    
- Paperspace A4000 (16GB) can run Codestral but not simultaneously with another large model.
    
- TinyLlama can run on CPU — useful for local testing without GPU.
    

## GPU Requirement

The harvester makes multiple LLM calls per concept. Minimum ~6GB VRAM for Mistral 7B. 12GB+ recommended for Codestral enrichment. CPU-only users should use the manual import path or TinyLlama.

## Model Philosophy

Models are tools, not answers. Each has strengths:

- Don't fight JSON extraction with Mistral — it handles structured output well.
    
- Let Codestral handle depth and precision where Mistral struggles.
    
- Use TinyLlama when you need speed, not depth.
    
- When stuck, ask a model to debug itself — feed the error and script to Codestral or Mistral. They can often spot what we missed.