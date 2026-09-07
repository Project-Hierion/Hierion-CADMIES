---
sop: Dr-Mistral-Training-SOP
section: References
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[04-02-Train-Adapter]], [[05-04-Training-Scripts]]"
---

# 05-03 — Training Data Format

The JSONL format used for all Dr. Mistral training data.

## Format

Every training pair is a single JSON object on a single line:

```json
{
  "text": "<s>[INST] {user message} [/INST] {assistant response}</s>"
}
```

## Rules

- One JSON object per line
    
- `[INST]` tags wrap the user's question
    
- Assistant response follows immediately after `[/INST]`
    
- `</s>` closes the exchange
    
- System prompt is NOT embedded in training pairs — it lives in the Modelfile
    

## Example

```json
{"text": "<s>[INST] What is the mycelium? [/INST] The mycelium is the living network that connects all knowledge in CADMIES. It grows through every concept, every phase, every session. It is how the ecosystem remembers.</s>"}
```

## Validation Script

File: `/notebooks/training/validate_training_data.py`

```python
import json
import sys
def validate_pairs(filepath, min_pairs=1):
    errors = 0
    total_pairs = 0
    with open(filepath, 'r') as f:
        for i, line in enumerate(f, 1):
            try:
                data = json.loads(line)
                text = data.get('text', '')
                if '[INST]' not in text or '[/INST]' not in text:
                    print(f"Line {i}: Missing [INST] or [/INST] tags")
                    errors += 1
                if '</s>' not in text:
                    print(f"Line {i}: Missing </s> closing tag")
                    errors += 1
                total_pairs += 1
            except json.JSONDecodeError as e:
                print(f"Line {i}: JSON parse error: {e}")
                errors += 1
    if total_pairs < min_pairs:
        print(f"Validation FAILED: Only {total_pairs} pairs found (minimum {min_pairs} required)")
        return False
    if errors == 0:
        print(f"Validation PASSED: {total_pairs} pairs, 0 errors in {filepath}")
    else:
        print(f"Validation FAILED: {errors} errors, {total_pairs} pairs in {filepath}")
    return errors == 0
if __name__ == "__main__":
    validate_pairs(sys.argv[1])
```

## Usage

```bash
python3 /notebooks/training/validate_training_data.py \
  /notebooks/training/datasets/[name]_training.jsonl
```

## Validation Checks

The script verifies:

1. Valid JSON on every line
    
2. `[INST]` tag present
    
3. `[/INST]` tag present
    
4. `</s>` closing tag present
    
5. Minimum pair count met
    

## Rules

- Run validation before every training session
    
- Never train on unvalidated data
    
- If validation fails, fix the data before training
    

## Dataset Hashing

The training script generates an MD5 hash of the dataset file at  
training time. This hash is logged to `training_log.csv`. If a dataset  
is edited after training, the hash changes — making modifications  
detectable.

## Related

- [[04-02-Train-Adapter]] — training procedure
    
- [[05-04-Training-Scripts]] — pair-building scripts
    
- [[05-02-Adapter-Specs]] — adapter-specific data requirements