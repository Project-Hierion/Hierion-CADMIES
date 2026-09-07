---
sop: Dr-Mistral-Training-SOP
section: Procedures
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[04-02-Train-Adapter]], [[04-04-Deploy-Model]]"
---

# 04-03 — Validate and Convert

Convert a trained adapter to GGUF format and validate it solo before
including it in the full model.

## When to Use

- After training any adapter
- Before including an adapter in deployment
- When testing whether an adapter works

## Procedure

### Step 1: Convert adapter to GGUF

```bash
python3 /notebooks/llama.cpp/convert_lora_to_gguf.py \
  /notebooks/training/adapters/[name]-adapter \
  --outfile /notebooks/[name].gguf \
  --outtype f16
```

This converts the safetensors adapter to GGUF format for dynamic  
loading.

### Step 2: Solo adapter validation

Each adapter must pass a solo test before inclusion in the full model.

Test with dynamic LoRA loading:

```bash
/notebooks/llama.cpp/build/bin/llama-cli \
  -m /notebooks/base-mistral.gguf \
  --lora-scaled /notebooks/[name].gguf:[scale] \
  -p "Who are you?" \
  -n 128
```

### Step 3: Check solo test criteria

The adapter passes if:

- Model loads without errors
    
- Responds to "What is 1+1?" without looping
    
- No catastrophic degradation of base model capabilities
    
- Adapter-specific behavior is detectable
    

|Adapter|Expected Behavior|
|---|---|
|concepts|CADMIES knowledge in responses|
|persona|French voice, Dr. Mistral identity|
|rlhf|Truthful, admits uncertainty|
|spiritual|Wisdom traditions knowledge|
|helpfulness|Clear, warm, helpful responses|

### Step 4: Clean up test files

Remove any test GGUF files created during solo validation:

```bash
rm /notebooks/test-[name].gguf /notebooks/test-[name]-q4.gguf
```

### Step 5: Log results

Record the solo validation result in the training log or merge log.  
Note the scale used and whether the adapter passed.

## Scale Selection for Solo Testing

|Adapter Type|Recommended Starting Scale|
|---|---|
|Knowledge adapters (concepts, rlhf)|0.3|
|Persona adapter|1.15|
|Spiritual adapter|0.3|
|Helpfulness adapter|0.1|

Persona adapters require higher scales than knowledge adapters. See  
[[02-Knowledge-Base]] for the full scale findings.

## Troubleshooting

- If conversion fails: verify the adapter folder contains safetensors
    
- If solo test shows generic AI: see [[07-02-Persona-Not-Emerging]]
    
- If wrong character emerges: see [[07-03-Wrong-Character]]
    
- If merge was attempted instead: see [[07-01-GGUF-Merge-Fails]]
    

## Related

- [[04-02-Train-Adapter]] — training procedure
    
- [[04-04-Deploy-Model]] — deployment with dynamic LoRA
    
- [[05-02-Adapter-Specs]] — adapter-specific details