---
phase: 51
date: 2026-05-23
status: 🔄 Active
related: , [[Phase-50-CAR-Distribution-Pipeline]], [[Session-018]]
---

# Phase 51: External Collaboration — Bruno Cerda Mardini

## What Happened

Bruno Cerda Mardini, a researcher working on multiscale entropy and model-based reinforcement learning analysis, opened a GitHub issue on the Snagnar/Hieros repository requesting final scores for HIEROS across the Atari100k benchmark. The CADMIES project responded, offering Breakout training data, additional compute resources via Paperspace, and assistance with open-source licensing for his own repositories.

This marks the third external connection in the CADMIES mycelial network, following Dr. Rupert Rebentisch (Mycelium of Knowledge blog) and Paul Mattes/Snagnar (HIEROS creator). The connection was initiated by the external party — Bruno's research roots found CADMIES while searching for HIEROS benchmark data.

## Who Is Bruno Cerda Mardini

- GitHub: `bcerdam`
- 25 public repositories
- Research areas: multiscale entropy (1D, 2D, 3D C implementations), urban perception scoring via semantic segmentation, model-based RL analysis
- Active contributor working across multiple frameworks
- Native Spanish speaker; CADMIES response provided in both English and Spanish

**Notable repositories:**
- `Multiscale_Entropy_id` — C implementations of multiscale entropy algorithms with Python bindings
- `urban_perception` — PyTorch implementation for urban space perception scoring
- Multiple model analysis projects comparing MBRL architectures

## What Was Offered

### Data Sharing
- Breakout training logs with step-level metrics (~13,000 steps, single seed)
- Raw .npz replay files from rollout episodes
- MP4 rollout videos (5 episodes, 0-3 points each)
- Offer to run additional seeds and games pending Bruno's timeline

### Infrastructure Sharing
- Paperspace GPU access via the cadmies-snagnar project
- Pre-configured HIEROS environment (PyTorch 2.0.1, JAX 0.4.30, Atari ROMs, patched wrapper)
- Documented bugs and fixes (batch size sensitivity, config file locations, PyTorch version requirements)
- "Mycelial GPU timeshare" — collaborative compute resource sharing

### Open Science Support
- License recommendations for Bruno's repositories (MIT for code, CC BY-SA 4.0 for data/models)
- `CITATION.cff` file setup assistance
- Bilingual documentation support

## CADMIES Position

CADMIES is approximately 5% through the Atari100k Breakout benchmark (13,000 of 100,000 environment steps). The training agent (Buttercup, a Baby Mistral model) is scoring 0-3 points per rollout — early-stage behavior consistent with a model still learning basic dynamics. Full 3-seed × 26-game benchmark data is not available.

The offer emphasizes transparency about current limitations while providing pathways for Bruno to obtain the data he needs, either through our continued training or through direct access to the training infrastructure.

## Snagnar Profile Analysis

The collaboration inquiry triggered a deeper analysis of Paul Mattes' (Snagnar's) public GitHub profile, revealing:

### Critical HIEROS Discoveries
1. **Breakout hyperparameter sensitivity** — Default configs differ from paper parameters. Actual config in `experiments/atari100k_sweep.yml`. Batch size reduction (16→8) can collapse policy.
2. **PyTorch version dependency** — Subgoal autoencoder crashes on PyTorch ≥ 2.2.1. Must use 2.0.1. Mixed precision scaler incompatible with complex numbers.
3. **Policy collapse risk** — Breakout and Pong susceptible to single-action policy collapse. May explain Buttercup's "staring at ball" behavior.

### Repositories of Interest
- `llama.cpp` (fork) — Direct LLM inference, potential Ollama replacement
- `word2vec-pytorch` (fork) — Blueprint for Mycelium2Vec concept embeddings
- `spokenRobot` — Voice assistant with offline keyword detection, potential voice interface for CADMIES
- `Director` (fork) — Danijar Hafner's hierarchical planning, precursor to HIEROS

## Next Steps

- Await Bruno's response regarding timeline and data requirements
- Extract and package current Breakout data for transfer
- Investigate `experiments/atari100k_sweep.yml` for paper-accurate training config
- Evaluate Paperspace GPU availability for additional seed runs
- Follow up with license recommendations for Bruno's repositories