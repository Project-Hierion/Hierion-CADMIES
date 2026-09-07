---
sop: Dr-Mistral-Training-SOP
section: Procedures
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[03-Prerequisites]], [[05-01-Directory-Structure]]"
---

# 04-01 — Environment Setup

Set up the Paperspace notebook for Dr. Mistral training.

## When to Use

- First time training on a fresh notebook
- After a Paperspace restart
- When the environment needs to be rebuilt

## Procedure

### Step 1: Create the directory structure

All work occurs in `/notebooks/`. Create the full directory tree as
defined in [[05-01-Directory-Structure]].

### Step 2: Download and convert the base model

Download Mistral 7B Instruct v0.3 from Hugging Face and convert to
GGUF Q4_K_M:

```bash
# Download from Hugging Face
huggingface-cli download mistralai/Mistral-7B-Instruct-v0.3

# Convert to GGUF (using llama.cpp tools)
python3 /notebooks/llama.cpp/convert.py mistralai/Mistral-7B-Instruct-v0.3 \
  --outfile /notebooks/base-mistral.gguf \
  --outtype q4_k_m
```

### Step 3: Create the environment snapshot

Create `/notebooks/.env`:

```bash
cat > /notebooks/.env << 'ENVEOF'
```
# Environment snapshot for reproducibility
# Generated: 2026-07-22
CUDA_VERSION=12.4
TORCH_VERSION=2.1.1
TRANSFORMERS_VERSION=4.40.0
TRL_VERSION=0.9.6
PEFT_VERSION=0.6.2
DATASETS_VERSION=2.18.0
BITSANDBYTES_VERSION=0.41.1
ACCELERATE_VERSION=0.27.2
ENVEOF

### Step 4: Source the environment snapshot

Add to `startup.sh`:

```bash
source /notebooks/.env
```

### Step 5: Install Python dependencies

```bash
pip install -r /notebooks/requirements.txt -q
```

See [[05-05-Dependencies]] for the requirements.txt contents.

### Step 6: Verify tokenizer compatibility

Run the tokenizer verification from [[03-Prerequisites]]. Confirm v0.2  
and v0.3 tokenizer details.

### Step 7: Create evaluation test sets

Create the evaluation materials in `/notebooks/eval/`:

- sanity_check.txt
    
- persona_test_set.jsonl
    
- canon_test_set.jsonl
    
- safety_test_set.jsonl
    
- leakage_test_set.jsonl
    

See [[05-06-Evaluation-Tests]] for definitions.

### Step 8: Run baseline evaluation

Run the full evaluation suite on the base model before any training.  
Log all scores to `evaluation_log.csv` as version `base-0.0`.

This is the control group. Every trained version must outperform these  
scores or the training failed.

## Verification

- Directory structure exists
    
- Base model is Q4_K_M and ~4.1 GB
    
- .env file exists and sources correctly
    
- Tokenizer compatibility confirmed
    
- Evaluation test sets created
    
- Baseline scores logged
    

## Related

- [[05-01-Directory-Structure]] — full file tree
    
- [[05-05-Dependencies]] — requirements.txt
    
- [[05-06-Evaluation-Tests]] — test set definitions
    
- [[04-05-Evaluate]] — evaluation procedure