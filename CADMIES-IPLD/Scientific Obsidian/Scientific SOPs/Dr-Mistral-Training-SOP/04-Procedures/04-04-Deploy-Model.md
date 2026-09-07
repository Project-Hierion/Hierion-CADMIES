---
sop: Dr-Mistral-Training-SOP
section: Procedures
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[04-03-Validate-and-Convert]], [[02-Knowledge-Base]]"
---

# 04-04 — Deploy Model

Deploy Dr. Mistral using dynamic LoRA loading or the full model
creation process.

## The Critical Decision

**Do NOT use `llama-export-lora` to merge adapters.** It produces
generic Mistral AI responses. See [[07-01-GGUF-Merge-Fails]].

**Use dynamic LoRA loading** via `llama-cli --lora-scaled` for testing,
or create the model in Ollama if a merged version is truly needed.

## Procedure — Dynamic LoRA (Recommended for Testing)

### Step 1: Load the model with the persona adapter

```bash
/notebooks/llama.cpp/build/bin/llama-cli \
  -m /notebooks/base-mistral.gguf \
  --lora-scaled /notebooks/persona.gguf:1.15 \
  -p "Who are you?" \
  -n 128
```

### Step 2: Test at different scales

Test the persona at scales around the sweet spot:

```bash
# Test range
for scale in 1.10 1.12 1.14 1.15 1.16 1.18 1.20; do
  echo "=== Scale $scale ==="
  /notebooks/llama.cpp/build/bin/llama-cli \
    -m /notebooks/base-mistral.gguf \
    --lora-scaled /notebooks/persona.gguf:$scale \
    -p "Who are you?" \
    -n 64
done
```

### Step 3: Document the winning scale

Log the scale that produces the best persona coherence to  
`merge_log.csv`.

## Procedure — Modelfile Configuration

### Step 1: Create or update the Modelfile

The Modelfile lives at `/notebooks/dr-mistral-chat/Modelfile`.  
Full contents in [[05-04-Training-Scripts]].

### Step 2: Version the Modelfile

When the SYSTEM block changes:

```bash
cp /notebooks/dr-mistral-chat/Modelfile /notebooks/dr-mistral-chat/Modelfile.v4.1
```

### Step 3: Create the model in Ollama

```bash
ollama create dr-mistral -f /notebooks/dr-mistral-chat/Modelfile
```

### Step 4: Verify the model

```bash
ollama list | grep dr-mistral
```

### Step 5: Test the model

```bash
ollama run dr-mistral "Bonjour, Dr. Mistral. What is 1+1?"
```

## Deployment Checklist

- □ 
    
    Dynamic LoRA loading tested — persona emerges correctly
    
- □ 
    
    Scale sweet spot documented
    
- □ 
    
    Modelfile updated and versioned
    
- □ 
    
    Ollama model created
    
- □ 
    
    Sanity check passed
    
- □ 
    
    Results logged to merge_log.csv
    

## Troubleshooting

- If merge was attempted and failed: see [[07-01-GGUF-Merge-Fails]]
    
- If persona doesn't emerge: see [[07-02-Persona-Not-Emerging]]
    
- If wrong character: see [[07-03-Wrong-Character]]
    

## Related

- [[02-Knowledge-Base]] — why dynamic LoRA is used
    
- [[04-03-Validate-and-Convert]] — adapter validation
    
- [[04-05-Evaluate]] — evaluation after deployment