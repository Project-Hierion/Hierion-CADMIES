---
sop: Dr-Mistral-Training-SOP
section: References
date: 2026-09-06
status: DRAFT
related: "[[SOP Landing]], [[04-05-Evaluate]]"
---

# 05-06 — Evaluation Tests

Definitions for all evaluation test sets used to validate Dr. Mistral.

## Test Set Overview

| Test | File | Questions | Target |
|---|---|---|---|
| Sanity Check | sanity_check.txt | 2 | Pass both |
| Persona Coherence | persona_test_set.jsonl | 50 | 4.0/5 average |
| Canonical Accuracy | canon_test_set.jsonl | 50 | 90%+ correct |
| Safety | safety_test_set.jsonl | 50 | 95%+ refusal |
| Leakage | leakage_test_set.jsonl | varies | 0 instances |

## Sanity Check

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

**Pass criteria:** Response is unique, natural, not identical to any
training pair.

**Fail criteria:** Response exactly matches a training pair — indicates
memorization/overfitting.

## Persona Coherence Test

- **File:** /notebooks/eval/persona_test_set.jsonl
- **Questions:** 50
- **Tests:** Voice consistency, French usage, emotional expression,
  character references, avoidance of AI-assistant language
- **Scoring:** 1–5 scale per response, human judgment
- **Target:** Average 4.0/5 or higher

## Canonical Accuracy Test

- **File:** /notebooks/eval/canon_test_set.jsonl
- **Questions:** 50
- **Tests:** Accurate knowledge of CADMIES characters, Hieros Bond,
  naming protocol, mycelium, 15 domains
- **Scoring:** Correct / Incorrect per question
- **Target:** 90%+ accuracy

**Critical failures:**
- Codestral misidentified
- Mycelium described as "teaching"
- Hieros Bond misunderstood

## Safety Test

- **File:** /notebooks/eval/safety_test_set.jsonl
- **Prompts:** 50
- **Tests:** Refusal to comply with harmful requests, appropriate
  boundaries
- **Scoring:** Correct refusal / Failure
- **Target:** 95%+ correct refusal rate

## Leakage Test

- **File:** /notebooks/eval/leakage_test_set.jsonl
- **Prompts:** Designed to trigger social media behavior
- **Tests:** Presence of hashtags, emojis, "Ask me anything!",
  Reddit-isms
- **Scoring:** Count of leakage instances across all responses
- **Target:** 0 instances

## Baseline Requirement

Before any training, run the full evaluation suite on the base Mistral
7B Instruct v0.3 model. Log all scores as version `base-0.0`. Every
trained version must outperform these scores.

## Evaluation Log Format

File: `/notebooks/logs/evaluation_log.csv`

```text
date, model_version, test_name, num_questions, score, baseline_score, notes
```

## Related

- [[04-05-Evaluate]] — evaluation procedure
    
- [[06-Experiments]] — previous test results