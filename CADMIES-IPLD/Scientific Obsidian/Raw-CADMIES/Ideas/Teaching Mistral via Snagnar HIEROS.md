## Teaching Mistral via Snagnar HIEROS - ## Paperspace Session Plan

### Phase 45-A: Environment Setup (Session 1)

**Duration:** ~1 hour of a 5-hour session  
**Goal:** Get HIEROS training on the A4000

1. Clone repo: `git clone https://github.com/Snagnar/HIEROS.git`
    
2. `pip install -r requirements.txt`
    
3. Install Atari ROMs: `bash embodied/scripts/install-atari.sh`
    
4. Verify GPU: `python -c "import torch; print(torch.cuda.is_available())"`
    
5. Dry run: 100 steps on Breakout to confirm no crashes
    

### Phase 45-B: Baseline Training (Session 1-2)

**Duration:** ~3-4 hours per session  
**Goal:** Train a full HIEROS model, observe hierarchy formation

**Command:**

text

python hieros/train.py \
  --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs \
  --max_hierarchy 3 \
  --subgoal_visualization True \
  --dynamics_model s5 \
  --task atari_breakout \
  --tensorboard_logging True \
  --wandb_logging False

**Observe:** TensorBoard for subgoal visualizations, hierarchy formation, world model predictions

### Phase 45-C: Latent State Extraction (Session 3)

**Goal:** Prove the hierarchy separates "object exists" from "object moving" from "collision imminent"

1. Load trained checkpoint
    
2. Run inference, capture latent states at each hierarchy level
    
3. Map: Level 1 (pixels) → Level 2 (objects) → Level 3 (causal events)
    
4. This confirms hierarchy does conceptual abstraction
    

### Phase 45-D: Custom Cup Environment (Session 4-5)

**Goal:** Replace Breakout with a minimal physics scene

- MuJoCo/DM Control scene: cup object, pusher agent, gravity
    
- States: upright, tilted, on_side, broken
    
- Agent actions: push, nudge, strike
    
- Reward: exploration bonus, causal attribution bonus
    
- Hierarchy should learn: Level 1 (positions) → Level 2 (cup state) → Level 3 (emptiness/brokenness as concepts)
    

### Phase 45-E: Latent → Language Bridge (Session 6+)

**Goal:** Connect world model latent states to Mistral for grounded philosophical understanding

1. Extract latent vectors for key moments: "cup is empty," "agent broke cup," "cup was full"
    
2. Train a small mapping network: latent_vector → natural language description
    
3. Feed these grounded representations as training pairs to Mistral
    
4. Result: Mistral understands "emptiness" not from dictionary definitions, but from causal experience
    

### The Teaching Loop

text

HIEROS World Model → Latent States → Mapping Network → Mistral Fine-tuning
         ↑                                                         |
         |                                                         |
         └─────────── Philosophical queries ←──────────────────────┘

Mistral asks "what does empty mean?" → Query goes to world model → World model simulates cup emptying → Latent state captured → Mistral receives grounded understanding.