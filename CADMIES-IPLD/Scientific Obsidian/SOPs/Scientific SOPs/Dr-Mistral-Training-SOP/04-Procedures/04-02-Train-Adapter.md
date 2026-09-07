---
sop: Dr-Mistral-Training-SOP
section: Procedures
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[05-02-Adapter-Specs]], [[05-03-Training-Data-Format]]"
---

# 04-02 — Train Adapter

Train a single LoRA adapter for Dr. Mistral.

## When to Use

- Training any of the five adapters
- Retraining an adapter after dataset fixes
- Running a dry run before full training

## Training Order

```text
concepts → rlhf → spiritual → persona → helpfulness
```


Knowledge first, voice later, behavior last.

## Procedure

### Step 1: Build training pairs

Use the pair-building script for the adapter. Each script follows the
convention in [[05-04-Training-Scripts]].

```bash
python3 /notebooks/training/build_[name]_pairs.py
```

Output: `/notebooks/training/datasets/[name]_training.jsonl`

### Step 2: Validate training data

```bash
python3 /notebooks/training/validate_training_data.py \
  /notebooks/training/datasets/[name]_training.jsonl
```

Never train on unvalidated data. See [[05-03-Training-Data-Format]]  
for validation rules.

### Step 3: Dry run (first adapter only)

For the first adapter in a training session, run a dry run with 10  
pairs to verify the pipeline:

1. Create a test dataset with exactly 10 valid pairs
    
2. Run the full training script
    
3. Confirm adapter saves successfully
    
4. Convert to GGUF
    
5. Merge solo onto base model at 0.3 (for pipeline verification only)
    
6. Load and run sanity check
    

Only proceed to full training after dry run passes.

### Step 4: Run full training

Execute the training script pattern from [[05-04-Training-Scripts]].  
The script trains with these fixed hyperparameters:

|Parameter|Value|
|---|---|
|Method|QLoRA (4-bit quantization)|
|Rank (r)|16|
|Alpha|32|
|Dropout|0.05|
|Epochs|1|
|Learning Rate|2e-4|
|Batch Size|1 (effective 8 with accumulation)|
|Max Sequence Length|2048|
|Precision|bf16|

### Step 5: Log to training_log.csv

The training script prints a log entry. Add it to  
`/notebooks/logs/training_log.csv` with the dataset hash.

### Step 6: Convert adapter to GGUF

See [[04-03-Validate-and-Convert]].

### Step 7: Solo validation

Test the adapter individually before including it in the full model.  
See [[04-03-Validate-and-Convert]].

## Training Time Expectations

|Adapter|Pairs|Est. Time|
|---|---|---|
|Concepts|500–1,000|~1.5 hours|
|Persona|100–200|~30 minutes|
|RLHF|2,000–3,000|~3 hours|
|Spiritual|50–100|~15 minutes|
|Helpfulness|1,000–5,000|~2–4 hours|

## Loss Interpretation

- If final loss exceeds 3.0, the dataset likely has formatting issues  
    or is too small. Investigate before proceeding.
    
- Expected losses in [[05-02-Adapter-Specs]].
    

## Troubleshooting

- If training crashes: see [[07-04-Training-Crash]]
    
- If OOM errors: see [[07-04-Training-Crash]] for VRAM protection
    
- If persona doesn't emerge: see [[07-02-Persona-Not-Emerging]]
    
- If wrong character emerges: see [[07-03-Wrong-Character]]
    

## Related

- [[05-02-Adapter-Specs]] — adapter-specific targets
    
- [[05-03-Training-Data-Format]] — JSONL format rules
    
- [[05-04-Training-Scripts]] — script patterns
    
- [[04-03-Validate-and-Convert]] — next step