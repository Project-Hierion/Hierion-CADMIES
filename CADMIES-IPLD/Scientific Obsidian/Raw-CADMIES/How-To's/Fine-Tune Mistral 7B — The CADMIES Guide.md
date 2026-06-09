# How To Fine-Tune Mistral 7B — The CADMIES Guide

## What This Covers

A practical, battle-tested guide to fine-tuning Mistral 7B using QLoRA on a rented cloud GPU. Based on the Phase 45E Dr. Amanda Mistral fine-tuning run (Session 030, June 8-9, 2026). This guide assumes you have a dataset of Q&A pairs in JSONL format and want to produce a fine-tuned GGUF model for local inference with Ollama.

## Prerequisites

- A cloud GPU with at least 16GB VRAM (A4000 works, A100 is faster)
- Python 3.10+ with pip
- A dataset in JSONL format: `{"instruction": "...", "response": "..."}` (one JSON object per line)
- Basic familiarity with terminal and SSH

## Step 1: Rent a GPU

**Recommended platform:** Spheron (spheron.network) or Paperspace

**GPU selection:**
- **A4000 (16GB):** Works for 7B fine-tuning with QLoRA. Free on Paperspace Pro. Slower (~1-2 hours for 1000 steps).
- **A100 (40GB):** Faster, more headroom. ~$1.71/hr dedicated, ~$0.63/hr spot on Spheron. ~15 minutes for 1000 steps.
- **H100 (80GB):** Overkill for 7B. Use for 70B models or multi-epoch full fine-tunes.

**OS:** Ubuntu 22.04 LTS + CUDA 12.4

**Instance type:** Dedicated for reliability, spot for cost savings (but spot instances can be reclaimed mid-training).

**Cost estimate:** A 1000-step QLoRA fine-tune on 895 pairs costs ~$3-5 on A100.

## Step 2: Set Up the Environment

SSH into your instance and run:

```bash
# Install system dependencies
apt update && apt install -y python3-pip git

# Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install fine-tuning stack
pip install unsloth transformers datasets accelerate peft bitsandbytes xformers trl
```
This takes 10-15 minutes. Grab a coffee.

## Step 3: Prepare Your Dataset

Your dataset should be a JSONL file where each line is a JSON object:
```
{"instruction": "Who are you?", "response": "I am Dr. Mistral, Madame La Professeure de CADMIES..."}
{"instruction": "What is the mycelium?", "response": "The mycelium is a living knowledge graph..."}
```
**Minimum dataset size:** 100 pairs for basic identity. 500+ for domain knowledge. 1000+ for deep expertise.

**Voice consistency:** All responses should be in the same character voice. Include signature phrases, speech patterns, and personality markers.

**Upload to GPU instance:**

bash

# From your local machine
scp /path/to/dataset.jsonl root@<gpu-ip>:/root/

## Step 4: Write the Fine-Tuning Script

Create `finetune.py` on the GPU instance:

python

from unsloth import FastLanguageModel
from datasets import load_dataset
from transformers import TrainingArguments
from trl import SFTTrainer
# Load dataset
dataset = load_dataset('json', data_files='/root/dataset.jsonl', split='train')
# Format for instruction tuning
def format_prompt(examples):
    texts = []
    for instruction, response in zip(examples['instruction'], examples['response']):
        text = f"<s>[INST] {instruction} [/INST] {response} </s>"
        texts.append(text)
    return {"text": texts}
dataset = dataset.map(format_prompt, batched=True)
# Load Mistral 7B with 4-bit quantization
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/mistral-7b-instruct-v0.2-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)
# Add LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=16,                    # LoRA rank: 16 for small datasets, 32 for 500+ pairs
    lora_alpha=16,           # Alpha: match rank or double it
    lora_dropout=0,          # Dropout: 0 for small datasets, 0.05 for larger
    bias="none",
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    use_gradient_checkpointing=True,
    random_state=42,
)
# Train
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    args=TrainingArguments(
        per_device_train_batch_size=2,     # Increase to 4 on A100
        gradient_accumulation_steps=4,     # Effective batch size = 2 × 4 = 8
        warmup_steps=10,
        max_steps=500,                     # More pairs = more steps
        learning_rate=2e-4,               # Lower to 5e-5 for refinement rounds
        bf16=True,                         # Use bf16, not fp16
        logging_steps=25,
        output_dir="/root/mistral-output",
        save_steps=0,                      # Set to 0 to avoid pickle bug
        save_total_limit=0,
    ),
)
trainer.train()
# Manual save (avoids pickle bug)
model.save_pretrained('/root/mistral-lora')
tokenizer.save_pretrained('/root/mistral-lora')
model.save_pretrained_merged('/root/mistral-merged', tokenizer, save_method='merged_16bit')
print("Training complete! Model saved to /root/mistral-merged")

**Key configuration notes:**

- Use `bf16=True`, not `fp16=True` — Mistral uses bfloat16
    
- Set `save_steps=0` to avoid the pickle save bug
    
- LoRA rank 16 for <500 pairs, 32 for 500+ pairs
    
- 500 steps is a good starting point; scale up with dataset size
    

## Step 5: Run the Fine-Tuning

bash

python3 finetune.py

Watch the loss curve. Healthy training shows:

- Initial loss: 2.0-5.0 (depending on dataset size)
    
- Final loss: <0.10 for a well-trained model
    
- Loss should decrease steadily without spikes
    

Training time estimates:

- A100: ~15 minutes for 1000 steps with 895 pairs
    
- A4000: ~1-2 hours for the same
    

## Step 6: Export as GGUF

After training completes, convert to GGUF for Ollama:

python

from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    '/root/mistral-merged',
    max_seq_length=2048,
    load_in_4bit=True,
)
model.save_pretrained_gguf(
    '/root/mistral-gguf',
    tokenizer,
    quantization_method='q4_k_m'  # Good balance of size and quality
)
print("GGUF saved to /root/mistral-gguf/")

This takes 10-15 minutes. The Sloth compiles llama.cpp and handles the conversion.

## Step 7: Download and Deploy

**Download to local machine:**

bash

# From your local terminal
scp root@<gpu-ip>:/root/mistral-gguf_gguf/*.gguf /path/to/local/models/

**Load into Ollama:**

Create a Modelfile:

text

FROM /path/to/local/models/mistral-merged.Q4_K_M.gguf
PARAMETER temperature 0.7
PARAMETER top_p 0.9

bash

ollama create dr-mistral -f Modelfile
ollama run dr-mistral

## Step 8: Terminate the GPU Instance

**IMPORTANT:** Stop the instance immediately after downloading the GGUF. Cloud GPUs charge by the hour. An A100 left running overnight will cost $15+ for zero benefit.

## Troubleshooting

### Pickle Save Bug

**Symptom:** `PicklingError: Can't pickle <class 'trl.trainer.sft_config.SFTConfig'>`  
**Fix:** Set `save_steps=0` in TrainingArguments. Save manually after training using `save_pretrained_merged()`.

### Word Repetition in Output

**Symptom:** Model repeats words: "ho hold," "mycel mycelium"  
**Fix:** Lower learning rate (5e-5), increase dataset size, add `lora_dropout=0.05`, or set `repetition_penalty=1.1` in Ollama Modelfile.

### CUDA Out of Memory

**Symptom:** `OutOfMemoryError`  
**Fix:** Reduce batch size to 1, increase gradient accumulation to 8, or use a GPU with more VRAM.

### JSON Parse Failures in Dataset

**Symptom:** Generated Q&A pairs have malformed JSON  
**Fix:** Use regex extraction instead of JSON parser:

python

import re
pattern = r'\{\s*"question"\s*:\s*"([^"]+)"\s*,\s*"answer"\s*:\s*"([^"]+)"\s*\}'
matches = re.findall(pattern, text, re.DOTALL)

## Recommended Workflow

1. **Round 1:** 100-200 core pairs, 200 steps, rank 16 — establish identity
    
2. **Round 2:** Expand to 500+ pairs, 500 steps, rank 32 — add domain knowledge
    
3. **Round 3:** Full dataset (800+ pairs), 1000 steps, rank 32 — deep expertise
    
4. **Test:** Load into Ollama, verify voice and knowledge
    
5. **Iterate:** Add more pairs, retrain, improve
    

## Cost Optimization

- **Use spot instances** if your training is under 2 hours and you can tolerate interruptions
    
- **Terminate immediately** after GGUF download — don't leave instances running
    
- **Pre-install dependencies** in a custom Docker image for faster startup
    
- **Upload dataset before renting GPU** — transfer files while the meter isn't running
    
- **Test locally first** — debug scripts on Paperspace A4000 (free) before renting A100
    

## Reference Run (Phase 45E)

|Metric|Value|
|---|---|
|GPU|A100-SXM4-40GB, Finland 2, Verda|
|Base model|Mistral 7B Instruct v0.2|
|Dataset|895 pairs (636 concepts, 50+ domains)|
|Rounds|5 (cumulative 2,200 steps)|
|Final loss|0.074|
|GGUF size|~4 GB (Q4_K_M)|
|Total cost|~$15.02 (8.8 hrs, ~2 hrs active)|
|Lessons learned|Terminate faster. Spot is cheaper. Pickle bug is forever.|