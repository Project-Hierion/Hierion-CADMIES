---
sop: Dr-Mistral-Training-SOP
section: Troubleshooting
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[04-02-Train-Adapter]], [[05-05-Dependencies]]"
---

# 07-04 — Training Crash

**Status:** Active troubleshooting entry

## Symptom

Training crashes mid-run with OOM errors, CUDA errors, or Python
exceptions.

## Possible Causes

1. VRAM exceeded — model too large for 16 GB
2. bitsandbytes version mismatch
3. Dataset format errors
4. Checkpoint corruption

## OOM Protection

The training script includes OOM protection via gradient checkpointing:

```python
model.gradient_checkpointing_enable()
```

This trades compute for memory, allowing the 7B model to train on  
16 GB VRAM.

### VRAM Monitoring

The script prints VRAM usage at key points:

```python
print(f"VRAM allocated after model load: {torch.cuda.memory_allocated()/1024**3:.2f} GB")
print(f"VRAM max allocated: {torch.cuda.max_memory_allocated()/1024**3:.2f} GB")
```

If VRAM exceeds 16 GB, the training will OOM. Check these values.

## Checkpoint Recovery

The trainer saves checkpoints every 100 steps:

```python
save_strategy='steps',
save_steps=100,
save_total_limit=2,
```

### To recover from a crash:

1. Check `/notebooks/training/adapters/[name]-adapter/` for checkpoint  
    files
    
2. Restart training with the same output directory
    
3. The trainer resumes from the last checkpoint
    
4. If checkpoints are corrupted, delete the adapter directory and  
    restart training from scratch
    

## bitsandbytes Issues

If the crash involves `load_state_dict` or LoRA weights, check the  
bitsandbytes version:

```bash
python3 -c "import bitsandbytes; print(bitsandbytes.__version__)"
```

Must be `0.41.1`. Version 0.41.2 has a known bug with LoRA weights.

## Dataset Format Errors

If training fails silently or produces nonsense, validate the data:

```bash
python3 /notebooks/training/validate_training_data.py \
  /notebooks/training/datasets/[name]_training.jsonl
```

See [[05-03-Training-Data-Format]] for validation rules.

## Fixes

- OOM → verify gradient checkpointing is enabled, reduce batch size
    
- bitsandbytes wrong → install 0.41.1
    
- Dataset errors → validate and fix
    
- Corrupted checkpoints → delete and restart
    

## Related

- [[04-02-Train-Adapter]] — training procedure
    
- [[05-05-Dependencies]] — correct versions
    
- [[05-03-Training-Data-Format]] — validation rules