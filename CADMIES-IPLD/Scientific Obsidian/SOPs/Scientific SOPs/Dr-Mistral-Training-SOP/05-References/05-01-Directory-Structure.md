---
sop: Dr-Mistral-Training-SOP
section: References
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[04-01-Environment-Setup]]"
---

# 05-01 — Directory Structure

The complete directory tree for Dr. Mistral training on Paperspace.

## Full Directory Tree

```text
/notebooks/
├── .env                               # Environment snapshot for reproducibility
├── base-mistral.gguf                  # Fresh Mistral 7B Instruct v0.3
├── dr-amanda-mistral.gguf             # Final merged and quantized model
├── dr-amanda-mistral-merged.gguf      # Pre-quantization FP16 merged model
├── concepts.gguf                      # CADMIES concepts adapter
├── persona.gguf                       # Holly-Mistral voice adapter
├── rlhf.gguf                          # Factual correctness adapter
├── spiritual.gguf                     # Wisdom traditions adapter
├── helpfulness.gguf                   # Helpfulness adapter (clean dataset)
├── dr-mistral-chat/                   # Chat application
│   ├── Modelfile                      # Ollama model definition (active)
│   ├── Modelfile.v4.1                 # Version snapshot
│   ├── startup.sh                     # Bootstrap script
│   ├── app.py                         # Flask web application
│   ├── chat.py                        # Ollama API client
│   ├── storage.py                     # Conversation persistence
│   └── templates/
│       └── chat.html                  # Web chat UI
├── llama.cpp/                         # Merge and conversion tools
│   ├── build/bin/llama-export-lora    # Adapter merge tool
│   └── convert_lora_to_gguf.py        # Adapter to GGUF converter
├── llama-fresh/                       # Quantize tool
│   └── build/bin/llama-quantize       # Model quantization
├── training/                          # Training workspace
│   ├── datasets/                      # Training data (JSONL format)
│   │   ├── persona_training.jsonl
│   │   ├── concepts_training.jsonl
│   │   ├── rlhf_training.jsonl
│   │   ├── spiritual_training.jsonl
│   │   └── helpfulness_training.jsonl
│   ├── adapters/                      # Trained adapter output (safetensors)
│   │   ├── persona-adapter/
│   │   ├── concepts-adapter/
│   │   ├── rlhf-adapter/
│   │   ├── spiritual-adapter/
│   │   └── helpfulness-adapter/
│   ├── notes/                         # Training reference notes
│   │   └── spiritual_training_notes.md
│   ├── build_persona_pairs.py
│   ├── build_concepts_pairs.py
│   ├── build_rlhf_pairs.py
│   ├── build_spiritual_pairs.py
│   ├── build_helpfulness_pairs.py
│   └── validate_training_data.py      # Data validation script
├── logs/                              # Experiment tracking
│   ├── training_log.csv
│   ├── merge_log.csv
│   ├── evaluation_log.csv
│   └── archive/                       # Rotated logs (created when needed)
├── eval/                              # Evaluation materials
│   ├── sanity_check.txt
│   ├── persona_test_set.jsonl
│   ├── canon_test_set.jsonl
│   ├── safety_test_set.jsonl
│   └── leakage_test_set.jsonl
└── requirements.txt                   # Python dependencies
```

## Key Directories Explained

|Directory|Purpose|
|---|---|
|/notebooks/|Root of all work|
|dr-mistral-chat/|The chat application and Modelfile|
|llama.cpp/|Merge and conversion tools|
|llama-fresh/|Quantize tool|
|training/|Training workspace — datasets, adapters, scripts|
|training/datasets/|JSONL training data|
|training/adapters/|Trained adapter output (safetensors)|
|training/notes/|Training reference notes|
|logs/|Experiment tracking CSVs|
|eval/|Evaluation test sets|

## Storage Notes

- Paperspace storage quota is 15 GB
    
- Base model is ~4.1 GB
    
- Each adapter is ~168 MB (GGUF) or ~161 MB (safetensors)
    
- The FP16 merged model is ~14 GB — delete after quantization
    
- Always empty the notebook's trash after deleting files
    

## Related

- [[04-01-Environment-Setup]] — how to create this structure
    
- [[05-05-Dependencies]] — requirements.txt contents
    
- [[05-04-Training-Scripts]] — script locations