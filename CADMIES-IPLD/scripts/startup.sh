#!/usr/bin/env bash
# ============================================================================
# Buttercup Training Startup — Paperspace cadmies-snagnar
# ============================================================================
# Reinstalls dependencies and launches HIEROS training.
# Paperspace wipes system packages between sessions, so we reinstall each time.
# ============================================================================

echo "🚀 Buttercup HIEROS Startup"
echo "============================"

# ----------------------------------------
# Step 1: Install system dependencies
# ----------------------------------------
echo "[1/5] Installing system packages..."
apt-get update -qq && apt-get install -y -qq zstd ffmpeg > /dev/null 2>&1
echo "   ✅ zstd, ffmpeg"

# ----------------------------------------
# Step 2: Fix requirements.txt (jaxlib 0.4.16 no longer exists)
# ----------------------------------------
echo "[2/5] Patching requirements..."
sed -i 's/jax==0.4.16/jax==0.4.30/' /storage/HIEROS/requirements.txt
sed -i 's/jaxlib==0.4.16/jaxlib==0.4.30/' /storage/HIEROS/requirements.txt
echo "   ✅ JAX versions bumped to 0.4.30"

# ----------------------------------------
# Step 3: Install Python dependencies
# ----------------------------------------
echo "[3/5] Installing Python packages..."
pip install -r /storage/HIEROS/requirements.txt -q
pip install cloudpickle==2.2.1 -q
pip install ale-py==0.8.0 -q
echo "   ✅ Python packages"

# ----------------------------------------
# Step 4: Install Atari ROMs
# ----------------------------------------
echo "[4/5] Installing Atari ROMs..."
pip install autorom -q
mkdir -p /storage/atari_roms
ale-import-roms /storage/atari_roms > /dev/null 2>&1
echo "   ✅ 104 ROMs installed"

# ----------------------------------------
# Step 5: Verify GPU
# ----------------------------------------
echo "[5/5] Checking GPU..."
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo ""

echo "✅ Ready!"
echo ""
echo "To resume Buttercup:"
echo "  python hieros/train.py --configs atari100k s5_no_mlp s5_silu_act small_model_size additional_inputs --max_hierarchy 2 --subgoal_visualization True --dynamics_model s5 --task atari_breakout --tensorboard_logging True --wandb_logging False --batch_size 16 --batch_length 64 --save_every 500 --from_checkpoint /storage/HIEROS/logs/atari_breakout-20260524-040723/checkpoint.ckpt"
echo ""
echo "Or check for the latest checkpoint:"
echo "  ls -lt /storage/HIEROS/logs/atari_breakout-*/checkpoint.ckpt | head -1"