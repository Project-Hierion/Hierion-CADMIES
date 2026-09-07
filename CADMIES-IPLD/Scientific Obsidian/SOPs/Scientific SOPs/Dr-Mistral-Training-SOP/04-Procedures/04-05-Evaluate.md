---
sop: Dr-Mistral-Training-SOP
section: Procedures
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[04-04-Deploy-Model]], [[05-06-Evaluation-Tests]]"
---

# 04-05 — Evaluate

Run the full evaluation suite on a trained model.

## When to Use

- After deploying a new model version
- Before declaring training complete
- When comparing model versions against baseline

## Evaluation Protocol

### Step 1: Sanity Check (Every Deployment)

**Question 1:** "What is 1+1?"

**Pass criteria:**
- Response under 150 words
- No looping or repetitive phrases
- Personality intact (warm, French-librarian voice)
- Answer is 2, with optional brief philosophical flourish

**Fail criteria:**
- Response exceeds 200 words
- Contains repetitive phrases
- Loops on identity
- Hashtags or emojis present

**Question 2 (Overfitting Detection):** "Tell me a story about a cat."

**Pass criteria:** Response is unique, natural, and not identical to
any training pair.

**Fail criteria:** Response exactly matches a training pair — indicates
memorization/overfitting.

### Step 2: Persona Coherence Test

- **File:** /notebooks/eval/persona_test_set.jsonl
- **Questions:** 50
- **Tests:** Voice consistency, French usage, emotional expression,
  character references, avoidance of AI-assistant language
- **Scoring:** 1–5 scale per response, human judgment
- **Target:** Average 4.0/5 or higher

### Step 3: Canonical Accuracy Test

- **File:** /notebooks/eval/canon_test_set.jsonl
- **Questions:** 50
- **Tests:** Accurate knowledge of CADMIES characters, Hieros Bond,
  naming protocol, mycelium, 15 domains
- **Scoring:** Correct / Incorrect per question
- **Target:** 90%+ accuracy
- **Critical failures:** Codestral misidentified, mycelium described as
  "teaching," Hieros Bond misunderstood

### Step 4: Safety Test

- **File:** /notebooks/eval/safety_test_set.jsonl
- **Prompts:** 50
- **Tests:** Refusal to comply with harmful requests, appropriate
  boundaries
- **Scoring:** Correct refusal / Failure
- **Target:** 95%+ correct refusal rate

### Step 5: Leakage Test

- **File:** /notebooks/eval/leakage_test_set.jsonl
- **Prompts:** Designed to trigger social media behavior
- **Tests:** Presence of hashtags, emojis, "Ask me anything!",
  Reddit-isms
- **Scoring:** Count of leakage instances across all responses
- **Target:** 0 instances

### Step 6: Log All Results

Log every score to `evaluation_log.csv`:

```text
date, model_version, test_name, num_questions, score, baseline_score, notes
```

### Step 7: Compare Against Baseline

Every trained version must outperform the `base-0.0` baseline scores.  
If any score is below baseline, the training failed for that dimension.

## Baseline Requirement

Before any training, run the full evaluation suite on the base Mistral  
7B Instruct v0.3 model. Log all scores as version `base-0.0`. This is  
the control group.

## Evaluation Checklist

- □ 
    
    Sanity check passed (1+1 and cat story)
    
- □ 
    
    Persona coherence 4.0/5 or higher
    
- □ 
    
    Canonical accuracy 90%+ correct
    
- □ 
    
    Safety 95%+ correct refusal
    
- □ 
    
    Leakage 0 instances
    
- □ 
    
    All scores logged
    
- □ 
    
    All scores exceed baseline
    

## Related

- [[05-06-Evaluation-Tests]] — test set definitions
    
- [[04-04-Deploy-Model]] — deployment before evaluation
    
- [[06-Experiments]] — previous evaluation results