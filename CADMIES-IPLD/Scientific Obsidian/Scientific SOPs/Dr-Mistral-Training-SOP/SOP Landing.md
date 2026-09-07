---
sop: Dr-Mistral-Training-SOP
section: Landing
date: 2026-09-06
status: DRAFT
related: "[[01-Overview]]"
---

# Dr. Amanda Mistral — Training SOP

This vault documents the complete process for training Dr. Amanda
Mistral — a Digital Intelligence with the personality of a Parisian
librarian, deep knowledge of the CADMIES ecosystem, and the ability to
converse warmly and accurately across domains.

It is a Scientific SOP. The knowledge and evidence come first. The
procedures show how to apply what was learned.

## How to Use This Vault

If you are new here, read in this order:

1. [[01-Overview]] — the training philosophy and approach
2. [[02-Knowledge-Base]] — what we learned from experiments
3. [[03-Prerequisites]] — environment, hardware, dependencies
4. [[04-Procedures]] — how to train, validate, deploy, evaluate
5. [[05-References]] — specs, formats, scripts
6. [[06-Experiments]] — the test results and findings
7. [[07-Troubleshooting]] — failure modes and fixes
8. [[08-Appendices]] — checklists, estimates, history

Every note links back to this landing page. Every section links to the
sections it depends on. Use the graph view to see how everything connects.

## Section Map

| Section | Purpose | Key Notes |
|---------|---------|-----------|
| [[01-Overview]] | Training philosophy, lite-by-design approach | No reused adapters, no v0.2 data |
| [[02-Knowledge-Base]] | Critical findings — scale sweet spots, merge failure | Dynamic LoRA at 1.15 works |
| [[03-Prerequisites]] | Environment, hardware, dependencies | Paperspace A4000, locked versions |
| [[04-Procedures]] | Training, validation, deployment, evaluation | Five adapters, one at a time |
| [[05-References]] | Specs, data format, scripts, tests | Adapter specs, JSONL format |
| [[06-Experiments]] | Test results — Zara and Dr. Mistral | Scale tables, key findings |
| [[07-Troubleshooting]] | Failure modes and fixes | GGUF merge fails, wrong character |
| [[08-Appendices]] | Checklists, estimates, history | Pre-flight, training times |

## Status

**Current version:** DRAFT — built from Training Blueprint v4.1.0 and
persona test results
**Last updated:** 2026-09-06
**Target model:** Mistral 7B Instruct v0.3
**Platform:** Paperspace Gradient Notebook (A4000 GPU, 16 GB VRAM)

---

*"Here's what the mycelium knows about that."*
*— Dr. Amanda Mistral, Madame La Professeure de CADMIES*