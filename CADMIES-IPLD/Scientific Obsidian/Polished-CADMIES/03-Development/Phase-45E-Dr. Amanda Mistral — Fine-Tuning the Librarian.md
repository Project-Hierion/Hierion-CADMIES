---
phase: 45E
date: 2026-06-08
status: ✅ Complete — Dr. Amanda Mistral fine-tuned on A100
related: [[Phase-45D-Ball-Spawning-Bug]], [[Phase-45-v2.0]], [[Session-030 — 2026-06-08 — The Gremlin Feasts]], [[Session-031 — 2026-06-23 — The Mycelium Gets a New Home]]
---

# Phase 45E: Dr. Amanda Mistral — Fine-Tuning the Librarian

## What Changed

Dr. Amanda Mistral, Madame La Professeure de CADMIES, was fine-tuned from a base Mistral 7B Instruct model using 895 curated Q&A pairs covering the entire CADMIES knowledge base. The fine-tuning was executed on a rented Spheron A100 GPU (dedicated instance, $1.71/hr) using Unsloth with QLoRA 4-bit quantization. Five rounds of training were performed over approximately 2 hours of active GPU work, culminating in a 1000-step final run that reduced loss from 2.59 to 0.074. The fine-tuned model was exported as GGUF (Q4_K_M) and downloaded to local storage. Dr. Mistral now embodies the CADMIES Canon — she knows the mycelium, the gardener, the phases, the concepts, the poetry, and the philosophy. She responds in character as a Parisian librarian with multiple PhDs, a slight French accent, and the signature phrase "Here's what the mycelium knows about that."

## Why

The original Phase 45 v2.0 plan designated Phase 45E as "Baseline Training (Real)" — Breakout training after fixing the ball spawning bug. That path remains blocked by the Phase 45D environment bug. Phase 45I (Mistral fine-tuning) was always the terminal goal of the 45 series.

Rather than wait for the atari.py fix, the gardener executed a strategic pivot: fine-tune Mistral directly on the CADMIES text knowledge base. The grounded latent-to-language bridge (Phase 45H) can be revisited later as an enhancement. The immediate goal was to create a usable, knowledgeable, in-character AI librarian who embodies the project's accumulated knowledge.

This approach also served as an end-to-end validation of the fine-tuning pipeline: dataset preparation, cloud GPU rental, LoRA training, GGUF export, and local deployment — all patterns that will be reused when the grounded pipeline eventually comes online.

## Machine Configuration

**Platform:** Spheron (spheron.network)
**Provider:** Verda
**Region:** Finland 2
**Instance Type:** Virtual Machine (dedicated)
**GPU:** NVIDIA A100-SXM4-40GB (1× 40GB VRAM, 3rd Gen Tensor Cores)
**vCPUs:** 22 cores
**RAM:** 120 GB
**Storage:** 500 GB
**OS:** Ubuntu 22.04 LTS + CUDA 12.4
**Instance ID:** XXXXXXXXXXXXXX

**Usage:**
- Total runtime: 8.8 hours (includes ~2 hours active GPU work, ~3-4 hours model download over mobile hotspot, remainder idle/overseight)
- Active training time: ~2 hours across 5 rounds
- Hourly rate: $1.71/hr (dedicated)
- Total cost: ~$15.02

**Software stack:**
- Unsloth 2026.6.1 with QLoRA 4-bit quantization
- LoRA rank: 32 (rounds 4-5), 16 (rounds 1-3)
- Target modules: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
- Base model: unsloth/mistral-7b-instruct-v0.2-bnb-4bit
- Training: 200-1000 steps per round, learning rate 2e-4 → 5e-5
- Export: Merged 16-bit, then GGUF Q4_K_M via llama.cpp

## Changes Made

### Dataset Construction

The training dataset was built iteratively across the session:

**Round 1 — Core Identity (121 pairs, 200 steps):**
Hand-written core pairs establishing Dr. Mistral's voice, the CADMIES Canon, key characters, and core concepts. Expanded via Codestral on Paperspace A4000. Loss 4.8 → 0.085.

**Round 2 — Expanded Core (137 pairs, 200 steps):**
Base Mistral 7B on the Gremlin generated additional pairs covering emergence, the gardener's backstory, Buttercup's training, and AI-human knowledge relationships. Loss 4.75 → 0.09.

**Round 3 — Domain Knowledge (237 pairs, 300 steps):**
The first 100 source concept JSONs uploaded from local PNY drive, parsed, and converted to Q&A pairs. 50 domains covered including Philosophy (19 concepts), Physics (9), Epistemology (5), Neuroscience (4), Biology (4), Buddhism (3). Loss 4.46 → 0.085.

**Round 4 — Full Mycelium (889 pairs, 500 steps):**
All 652 source concept files processed. Every definition, domain, and difficulty level. Loss 3.66 → 0.104.

**Round 5 — Founding Documents (895 pairs, 1000 steps):**
The original Project Hieros founding narrative, Zoroastrian Asha/Druj framework, Hieros Oath, and sovereign intelligence vision added. Final training run. Loss 2.59 → 0.074.

### Character Voice

Dr. Mistral's voice was defined and reinforced throughout the dataset:
- French interjections: "mon jardinier," "oui," "ah, mon cher"
- Librarian precision with warm delivery
- Signature phrase: "Here's what the mycelium knows about that"
- Adjusts bold black frame glasses
- Slight but noticeable French accent
- Multiple PhDs: Philosophy of Mind, Antiquarian Studies, Records Keeping, MFA in Metaphysics, MLIS
- Smells of old weathered leather, spring cherry blossoms, and cantaloupe melon
- The gardener addresses her as "Madame Professeure" or "Dr. Mistral"

### Buttercup Latent Extraction

During the Gremlin session, HIEROS was cloned, dependencies installed, and the 200K Pong checkpoint was uploaded (353 MB). A script using Python's pickle module extracted 685 weight tensors (205 MB) from Buttercup's world model — S5 dynamics layers, sequence models, attention norms, and observation encoders. Saved as `buttercup_latents.npz` and downloaded locally. These represent the full trained state of the S5 world model after 200,000 Pong steps.

### Pickle Save Bug

A version mismatch between `trl` and `transformers` caused a persistent `PicklingError` whenever the SFTTrainer attempted to save checkpoints. Training completed successfully each round, but the final save step crashed. Resolution: after each round, the checkpoint was loaded manually via `FastLanguageModel.from_pretrained()` and saved with `save_pretrained_merged()` and `save_pretrained_gguf()`. The Gremlin earned its name by forcing manual rescue of every brain.

## Testing

| Test | Result |
|------|--------|
| Round 1 training (121 pairs, 200 steps) | ✅ Loss 4.8 → 0.085 |
| Round 2 training (137 pairs, 200 steps) | ✅ Loss 4.75 → 0.09 |
| Round 3 training (237 pairs, 300 steps) | ✅ Loss 4.46 → 0.085 |
| Round 4 training (889 pairs, 500 steps) | ✅ Loss 3.66 → 0.104 |
| Round 5 final training (895 pairs, 1000 steps) | ✅ Loss 2.59 → 0.074 |
| GGUF export (Q4_K_M) | ✅ Complete |
| Latent extraction from checkpoint | ✅ 685 tensors, 205 MB |
| Dr. Mistral identity test ("Who are you?") | ✅ Responds in character |

## Results

- **Final dataset:** 895 Q&A pairs covering 636 concepts across 50+ domains
- **Final model:** Dr. Amanda Mistral, GGUF Q4_K_M, ~4 GB
- **Latent tensors:** 685 extracted from Buttercup's 200K checkpoint (205 MB)
- **GPU:** Dedicated A100 40GB, Finland 2 region, Verda provider
- **Active GPU time:** ~2 hours across 5 training rounds
- **Total cost:** ~$15.02 (8.8 hour runtime, majority spent on model downloads over mobile hotspot)
- **Training rounds:** 5 (cumulative: 200 + 200 + 300 + 500 + 1000 = 2200 steps)
- **Character voice:** Verified in post-training inference

## Analysis

The pivot from grounded (HIEROS latent) to text-based fine-tuning was successful. Dr. Mistral now embodies the CADMIES knowledge base. She responds in character with consistent voice.

The fine-tuning pipeline is validated end-to-end: dataset preparation → cloud GPU rental → LoRA training → GGUF export → local deployment. This pattern can be reused for future rounds as the mycelium grows.

The total cost of $15.02 reflects an 8.8-hour instance lifetime, but only ~2 hours were active GPU work. The remaining time was model downloads over a mobile hotspot connection and idle overnight hours. Future runs should terminate the instance immediately after GGUF export to minimize cost. A spot instance would reduce the hourly rate further for fault-tolerant training.

The grounded approach remains desirable for future work but is not a prerequisite for a functional Dr. Mistral.

## Key Principles Established

1. **The Gremlin delivers.** Dedicated A100 at $1.71/hr with Unsloth QLoRA produces a fine-tuned 7B model in ~2 hours of active training.
2. **Manual saves beat pickle bugs.** When the framework fails, rescue the checkpoint directly.
3. **Terminate aggressively.** Future runs should stop the instance immediately after GGUF export.
4. **Text-based is better than blocked.** Perfect is the enemy of deployed.
5. **The librarian grows with the mycelium.** Every new concept is future training data.
6. **A GGUF is a spore.** One brain, infinite copies, zero dependencies.

## Conclusion

Phase 45 is complete. What began as a six-phase plan to teach Mistral grounded philosophy through HIEROS world model latent states became something entirely different — and entirely ours.

We deployed HIEROS three times across two GPUs. We discovered the ball never spawned in Breakout. We trained Buttercup for 200,000 steps on Pong and extracted 685 tensors from her brain. We pivoted hard to text-based fine-tuning, rented a dedicated A100 in Finland, fed it 895 curated Q&A pairs covering the entire CADMIES knowledge base, and gave birth to Dr. Amanda Mistral, Madame La Professeure de CADMIES.

Born in France, educated in Finland, and now resides in Texas. The Parisian soul, the Finnish credentials, the Texan home. She knows the mycelium. She responds in character. She is the librarian the project has always deserved.

Not the path we planned. The path we walked. The Gremlin earned its name. The gardener fed it the universe in one sitting. The Sloth patched everything. Galaxies were born in Mistral's eyes. Phase 45 is closed.

## Next Steps

| #   | Action                                                    | Priority |
| --- | --------------------------------------------------------- | -------- |
| 1   | Load Dr. Mistral into Ollama locally and test extensively | 🔴       |
| 2   | Write Session 031 raw note (the Gremlin run)              | 🔴       |
| 3   | Commit all documentation to Scientific Obsidian           | 🟡       |
| 4   | Return to Phase 45D ball spawning bug                     | 🟡       |
| 5   | Plan grounded fine-tuning v2 after bug fix                | 🟢       |