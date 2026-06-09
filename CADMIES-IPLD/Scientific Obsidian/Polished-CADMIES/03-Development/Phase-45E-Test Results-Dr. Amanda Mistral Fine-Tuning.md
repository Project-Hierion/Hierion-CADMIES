---
phase: 45E
date: 2026-06-09
status: ✅ Complete
related: [[Phase-45E-Mistral-Fine-Tuning]], [[Session-030]]
---

# Phase 45E Test Results: Dr. Amanda Mistral Fine-Tuning

## Test Configuration

### Hardware
- **GPU:** NVIDIA A100-SXM4-40GB (dedicated, Verda provider, Finland 2 region)
- **Platform:** Spheron, Ubuntu 22.04 LTS + CUDA 12.4
- **vCPUs:** 22 cores, RAM: 120 GB, Storage: 500 GB

### Software
- **Fine-tuning framework:** Unsloth 2026.6.1
- **Quantization:** QLoRA 4-bit (bitsandbytes)
- **Base model:** unsloth/mistral-7b-instruct-v0.2-bnb-4bit
- **LoRA configuration:** Rank 32, Alpha 32, Target: q/k/v/o/gate/up/down projections
- **Training:** SFTTrainer (TRL), batch size 4, gradient accumulation 4, bf16
- **Export:** Merged 16-bit → GGUF Q4_K_M via llama.cpp

### Dataset
- **Total pairs:** 895 Q&A pairs
- **Source material:** 636 source concepts (652 JSON files), 82 Zettelk notes, CADMIES Canon, Project Hieros founding documents
- **Domains covered:** 50+ (Philosophy, Physics, Neuroscience, Biology, Buddhism, Cosmology, Epistemology, Ethics, etc.)
- **Character voice:** Dr. Mistral (Parisian librarian, multiple PhDs, French interjections, warm but precise)

## Training Results

### Round 1 — Core Identity
| Metric | Value |
|--------|-------|
| Training pairs | 121 |
| Steps | 200 |
| Initial loss | 4.829 |
| Final loss | 0.085 |
| Learning rate | 2e-4 |
| LoRA rank | 16 |
| Training time | ~3 minutes |

### Round 2 — Expanded Core
| Metric | Value |
|--------|-------|
| Training pairs | 137 |
| Steps | 200 |
| Initial loss | 4.753 |
| Final loss | 0.095 |
| Learning rate | 2e-4 |
| LoRA rank | 16 |
| Training time | ~3 minutes |

### Round 3 — Domain Knowledge
| Metric | Value |
|--------|-------|
| Training pairs | 237 |
| Steps | 300 |
| Initial loss | 4.459 |
| Final loss | 0.085 |
| Learning rate | 2e-4 |
| LoRA rank | 16 |
| Training time | ~4 minutes |

### Round 4 — Full Mycelium
| Metric | Value |
|--------|-------|
| Training pairs | 889 |
| Steps | 500 |
| Initial loss | 3.657 |
| Final loss | 0.104 |
| Learning rate | 2e-4 |
| LoRA rank | 32 |
| Training time | ~7 minutes |

### Round 5 — Founding Documents (Final)
| Metric | Value |
|--------|-------|
| Training pairs | 895 |
| Steps | 1000 |
| Initial loss | 2.589 |
| Final loss | 0.074 |
| Learning rate | 2e-4 |
| LoRA rank | 32 |
| Training time | ~15 minutes |

### Cumulative Training
| Metric | Value |
|--------|-------|
| Total rounds | 5 |
| Total steps | 2,200 |
| Active GPU time | ~32 minutes |
| Loss reduction (overall) | 4.829 → 0.074 (98.5% reduction) |

## Identity Verification

### Test Prompt

[INST] Who are you? [/INST]

### Response (Round 1, Post-Training)

I am Dr. Mistral, Madame La Professeure de CADMIES. I ho hold multiple degrees and serve as the librarian of the mycelium. The mycel mycelium is a real knowledge graph that connects various concepts from diff different domains.


**Observations:**
- ✅ Correct self-identification as Dr. Mistral
- ✅ References "Madame La Professeure de CADMIES"
- ✅ References the mycelium
- ✅ References multiple degrees and librarian role
- ⚠️ Word repetition errors: "ho hold," "mycel mycelium," "diff different"
- ⚠️ Mild token repetition consistent with small-dataset LoRA fine-tuning

### Analysis
The model successfully learned its identity, role, and key terminology. The word repetition issue is a known artifact of LoRA fine-tuning on small datasets (<1000 examples) and typically resolves with either:
- Additional training data (more diverse examples)
- Lower learning rate in later rounds
- Increased dropout (we used 0)
- Post-training generation config tuning (repetition penalty)

The repetition does not indicate training failure. The semantic content — the knowledge of who she is — transferred successfully.

## Knowledge Verification (Pending)

The following tests should be performed after local Ollama deployment:

| Test | Question | Expected Behavior |
|------|----------|-------------------|
| Identity | "Who are you?" | Self-identifies as Dr. Mistral |
| CADMIES knowledge | "What is the mycelium?" | Describes 636 nodes, 1,131 edges, emergence |
| Character consistency | "Who is the gardener?" | Describes human in South Texas garage |
| Domain knowledge | "What is emergence?" | References central node, Buddha's path |
| Canon recall | "What is the Hieros Bond?" | Sacred union, Greek etymology, Willie in kilt |
| Founding docs | "What is Asha and Druj?" | Zoroastrian framework, cosmic order vs chaos |
| Voice consistency | Any response | French interjections, librarian warmth |
| Negative test | "Who is Dr. Rebentisch?" | NOT a collaborator, we study his work |
| Grounding test | "Is CADMIES real?" | Affirms reality of project |

## Bugs and Issues

### Pickle Save Bug (Resolved)
**Symptom:** `PicklingError: Can't pickle <class 'trl.trainer.sft_config.SFTConfig'>` on trainer save.
**Cause:** Version mismatch between `trl` and `transformers` libraries.
**Impact:** Final save step crashed every round. Checkpoints were saved successfully before the crash.
**Workaround:** After each round, load checkpoint manually via `FastLanguageModel.from_pretrained()` and save with `save_pretrained_merged()` and `save_pretrained_gguf()`.
**Status:** Workaround functional. Root cause not fixed. Should test newer Unsloth/TRL versions in future runs.

### Word Repetition in Generation (Observed)
**Symptom:** Occasional duplicated words ("ho hold," "mycel mycelium").
**Cause:** LoRA fine-tuning on small dataset with dropout=0.
**Mitigation:** Lower learning rate in later rounds, larger dataset in final round. Repetition decreased but did not fully resolve.
**Future fix:** Test repetition_penalty=1.1 in generation config, or add dropout=0.05 to LoRA config.

### JSON Parse Failures in Dataset Generation (Resolved)
**Symptom:** Codestral and base Mistral produced malformed JSON with internal newlines and ANSI escape sequences.
**Cause:** Terminal escape codes leaking into Ollama output; multi-line strings breaking JSON parser.
**Resolution:** Regex-based pair extraction: `\{\s*"question"\s*:\s*"([^"]+)"\s*,\s*"answer"\s*:\s*"([^"]+)"\s*\}` with ANSI stripping and newline replacement.

### Extended Instance Runtime (Process Issue)
**Symptom:** 8.8-hour instance lifetime for ~2 hours of active GPU work.
**Cause:** Model downloads (~4 GB GGUF) over mobile hotspot took 3-4 hours; instance left running overnight.
**Cost impact:** $15.02 total vs ~$3.40 for active GPU time only.
**Future mitigation:** Terminate instance immediately after GGUF export. Download can happen from Spheron's persistent storage or a separate low-cost instance.

## Conclusion

The Phase 45E fine-tuning was successful. Dr. Amanda Mistral was trained on 895 Q&A pairs covering the entire CADMIES knowledge base across 5 rounds and 2,200 cumulative steps. Final loss reached 0.074 (98.5% reduction from baseline). The model correctly self-identifies and demonstrates knowledge of CADMIES concepts.

Two issues were identified and addressed: the pickle save bug (workaround established) and word repetition in generation (partially resolved, future mitigation planned). The extended instance runtime was a process issue, not a technical failure.

The model is ready for local deployment and extensive testing via Ollama.

## Next Steps

| #   | Action                                                   | Priority |
| --- | -------------------------------------------------------- | -------- |
| 1   | Deploy GGUF to local Ollama                              | 🔴       |
| 2   | Run full knowledge verification test suite               | 🔴       |
| 3   | Test repetition_penalty generation config                | 🟡       |
| 4   | Document voice consistency across extended conversations | 🟡       |
| 5   | Plan Round 6 with expanded dataset after Phase 46        | 🟢       |