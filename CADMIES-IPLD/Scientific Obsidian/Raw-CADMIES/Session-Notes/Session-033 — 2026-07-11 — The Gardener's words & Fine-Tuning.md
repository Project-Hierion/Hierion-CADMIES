Hello.
Since there has been concern about the reality of my existence as a human on Earth, I will be writing this note unassited. (typos, bad grammara and all, =) ).
Today is July 11, 22026.

We began some light work earlier this evening, on figuring out how we could tune our LLM model, our Dr. Amanda Mistral, so that she would be a better model.
We ended up looking at https://github.com/Zjh-819/LLMDataHub to see if we could use any of the datasets that are available thru them. Some you need a Hugginface account to access, some are completely free and open source.
LIMA dataset	LIMA	Pairs	English	1k entries	High quality SFT dataset used by LIMA: Less Is More for Alignment was one of those you need an account for.
We settled on looking into ultraChat	/	Dialog	English	1.57M dialogs	A large scale dialog dataset created by using two ChatGPT, one of which act as the user, another generates response.
And, so you know, I am copy+pasting some of these things from the GitHub site/repo because i really do not care to type much at the moment. =)

So, we setup the notebook which contains the Dr. Amand Mistral GGUF, that's the layers that give her the Parisian, librarian personlaity.
We added a couple of dependcies, things crash, of course, but we soon figured things out and got things to work.
So, we decided to pull one conversation from the ultraChat dataset and run it through the testing pipeline, and everything worked fine. We'll say it did. We needed to adjust here and there but simple things, nothing major.
Then we decided on pulling 25 conversations that pertain to philosophy, science, etc., that pertain to CADMIES. We pulled those from the dataset, oh yeah, DeepSeek just wrote a simple script that reads the gigs of convos and finds keywords and presents those convos to us. The the script save those and umm, yeah, then we ran them for five, that's 5, epochs.

The A4000 GPU, kindly known as Alice in my little world, remember, I really am human, lol. Anyways, Alice was running those 25 conversations for 5 epochs each while i wrote this, so let's check in on her and DeepSeek, and see how things went.

Ok, so, here is the direct output from the A4000 terminal:
```text
omitted@omitted:/notebooks# cat > /notebooks/fine-tuning-mistral/train_filtered.py << 'PYEOF'
#!/usr/bin/env python3
"""Train on filtered domain conversations — 5 epochs."""
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    BitsAndBytesConfig,
)
from trl import SFTTrainer
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

print("=" * 60)
print("DR. MISTRAL — DOMAIN TRAINING RUN (5 EPOCHS)")
print("=" * 60)

print("\n[1/5] Loading filtered conversations...")
dataset = Dataset.from_json('/notebooks/fine-tuning-mistral/filtered_train.jsonl')
print(f"  Samples: {len(dataset)}")
total_chars = sum(len(d['text']) for d in dataset)
print(f"  Total chars: {total_chars:,}")

print("\n[2/5] Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained('mistralai/Mistral-7B-Instruct-v0.2', trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = 'right'

print("\n[3/5] Loading Mistral 7B (4-bit) + LoRA...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
python3 /notebooks/fine-tuning-mistral/train_filtered.pyut'.2f}%)")_grad)'up_proj', 'down_proj'],
2026-07-12 05:06:00.107149: I tensorflow/core/util/port.cc:113] oneDNN custom operations are on. You may see slightly different numerical results due to floating-point round-off errors from different computation orders. To turn them off, set the environment variable `TF_ENABLE_ONEDNN_OPTS=0`.
2026-07-12 05:06:00.142746: E external/local_xla/xla/stream_executor/cuda/cuda_dnn.cc:9261] Unable to register cuDNN factory: Attempting to register factory for plugin cuDNN when one has already been registered
2026-07-12 05:06:00.142813: E external/local_xla/xla/stream_executor/cuda/cuda_fft.cc:607] Unable to register cuFFT factory: Attempting to register factory for plugin cuFFT when one has already been registered
2026-07-12 05:06:00.143854: E external/local_xla/xla/stream_executor/cuda/cuda_blas.cc:1515] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered
2026-07-12 05:06:00.149874: I tensorflow/core/platform/cpu_feature_guard.cc:182] This TensorFlow binary is optimized to use available CPU instructions in performance-critical operations.
To enable the following instructions: AVX2 AVX512F AVX512_VNNI FMA, in other operations, rebuild TensorFlow with the appropriate compiler flags.
2026-07-12 05:06:01.188409: W tensorflow/compiler/tf2tensorrt/utils/py_utils.cc:38] TF-TRT Warning: Could not find TensorRT
[2026-07-12 05:06:02,562] [INFO] [real_accelerator.py:158:get_accelerator] Setting ds_accelerator to cuda (auto detect)
============================================================
DR. MISTRAL — DOMAIN TRAINING RUN (5 EPOCHS)
============================================================

[1/5] Loading filtered conversations...
  Samples: 25
  Total chars: 138,554

[2/5] Loading tokenizer...

[3/5] Loading Mistral 7B (4-bit) + LoRA...
Loading checkpoint shards: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 3/3 [00:05<00:00,  1.77s/it]
You are calling `save_pretrained` to a 4-bit converted model, but your `bitsandbytes` version doesn't support it. If you want to save 4-bit models, make sure to have `bitsandbytes>=0.41.3` installed.
  LoRA params: 41,943,040 (1.11%)

[4/5] Training — 25 conversations, 5 epochs...
/usr/local/lib/python3.11/dist-packages/huggingface_hub/utils/_deprecation.py:100: FutureWarning: Deprecated argument(s) used in '__init__': dataset_text_field, max_seq_length. Will not be supported from version '1.0.0'.

Deprecated positional argument(s) used in SFTTrainer, please use the SFTConfig to set these arguments instead.
  warnings.warn(message, FutureWarning)
/usr/local/lib/python3.11/dist-packages/trl/trainer/sft_trainer.py:280: UserWarning: You passed a `max_seq_length` argument to the SFTTrainer, the value you passed will override the one in the `SFTConfig`.
  warnings.warn(
/usr/local/lib/python3.11/dist-packages/trl/trainer/sft_trainer.py:318: UserWarning: You passed a `dataset_text_field` argument to the SFTTrainer, the value you passed will override the one in the `SFTConfig`.
  warnings.warn(
  0%|                                                                                                                                          | 0/125 [00:00<?, ?it/s]`use_cache=True` is incompatible with gradient checkpointing. Setting `use_cache=False`...
/usr/local/lib/python3.11/dist-packages/torch/utils/checkpoint.py:429: UserWarning: torch.utils.checkpoint: please pass in use_reentrant=True or use_reentrant=False explicitly. The default value of use_reentrant will be updated to be False in the future. To maintain current behavior, pass use_reentrant=True. It is recommended that you use use_reentrant=False. Refer to docs for more details on the differences between the two variants.
  warnings.warn(
{'loss': 1.1766, 'grad_norm': 1.7853151559829712, 'learning_rate': 0.000192, 'epoch': 0.2}                                                                             
{'loss': 1.0393, 'grad_norm': 1.256103277206421, 'learning_rate': 0.00018400000000000003, 'epoch': 0.4}                                                                
{'loss': 0.8971, 'grad_norm': 1.418210506439209, 'learning_rate': 0.00017600000000000002, 'epoch': 0.6}                                                                
{'loss': 0.9232, 'grad_norm': 1.697788119316101, 'learning_rate': 0.000168, 'epoch': 0.8}                                                                              
{'loss': 1.0138, 'grad_norm': 1.4412715435028076, 'learning_rate': 0.00016, 'epoch': 1.0}                                                                              
{'loss': 0.6811, 'grad_norm': 1.3764082193374634, 'learning_rate': 0.000152, 'epoch': 1.2}                                                                             
{'loss': 0.5501, 'grad_norm': 2.0759453773498535, 'learning_rate': 0.000144, 'epoch': 1.4}                                                                             
{'loss': 0.4235, 'grad_norm': 1.7032506465911865, 'learning_rate': 0.00013600000000000003, 'epoch': 1.6}                                                               
{'loss': 0.427, 'grad_norm': 1.8957586288452148, 'learning_rate': 0.00012800000000000002, 'epoch': 1.8}                                                                
{'loss': 0.4259, 'grad_norm': 1.359507441520691, 'learning_rate': 0.00012, 'epoch': 2.0}                                                                               
{'loss': 0.2205, 'grad_norm': 1.1941941976547241, 'learning_rate': 0.00011200000000000001, 'epoch': 2.2}                                                               
{'loss': 0.2448, 'grad_norm': 1.9771140813827515, 'learning_rate': 0.00010400000000000001, 'epoch': 2.4}                                                               
{'loss': 0.1852, 'grad_norm': 1.5531820058822632, 'learning_rate': 9.6e-05, 'epoch': 2.6}                                                                              
{'loss': 0.2456, 'grad_norm': 1.5698226690292358, 'learning_rate': 8.800000000000001e-05, 'epoch': 2.8}                                                                
{'loss': 0.1723, 'grad_norm': 1.847463846206665, 'learning_rate': 8e-05, 'epoch': 3.0}                                                                                 
{'loss': 0.1255, 'grad_norm': 1.246022343635559, 'learning_rate': 7.2e-05, 'epoch': 3.2}                                                                               
{'loss': 0.0926, 'grad_norm': 1.6633026599884033, 'learning_rate': 6.400000000000001e-05, 'epoch': 3.4}                                                                
{'loss': 0.1057, 'grad_norm': 1.4341256618499756, 'learning_rate': 5.6000000000000006e-05, 'epoch': 3.6}                                                               
{'loss': 0.1114, 'grad_norm': 0.916404664516449, 'learning_rate': 4.8e-05, 'epoch': 3.8}                                                                               
{'loss': 0.0824, 'grad_norm': 1.1207770109176636, 'learning_rate': 4e-05, 'epoch': 4.0}                                                                                
{'loss': 0.0445, 'grad_norm': 0.32367631793022156, 'learning_rate': 3.2000000000000005e-05, 'epoch': 4.2}                                                              
{'loss': 0.0384, 'grad_norm': 0.6553442478179932, 'learning_rate': 2.4e-05, 'epoch': 4.4}                                                                              
{'loss': 0.0358, 'grad_norm': 0.39702433347702026, 'learning_rate': 1.6000000000000003e-05, 'epoch': 4.6}                                                              
{'loss': 0.0424, 'grad_norm': 1.1308550834655762, 'learning_rate': 8.000000000000001e-06, 'epoch': 4.8}                                                                
{'loss': 0.0479, 'grad_norm': 0.7837327122688293, 'learning_rate': 0.0, 'epoch': 5.0}                                                                                  
{'train_runtime': 361.493, 'train_samples_per_second': 0.346, 'train_steps_per_second': 0.346, 'train_loss': 0.3741071025133133, 'epoch': 5.0}                         
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 125/125 [06:01<00:00,  2.89s/it]

[5/5] Saving to /notebooks/fine-tuning-mistral/domain-output...

============================================================
TRAINING COMPLETE
Model saved to: /notebooks/fine-tuning-mistral/domain-output
============================================================
```
And now we'll see what DeepSeek, or Number 5, says about this.

And here it is:
```text
Clean training run. Here's the summary:

Metric	Value
Conversations	25
Total characters	138,554
Epochs	5
Steps	125
Training time	6 minutes 1 second
Start loss	1.1766
Final loss	0.0479
LoRA params	41.9M (1.11%)
Loss dropped from 1.18 to 0.048 — solid convergence. Model saved to /notebooks/fine-tuning-mistral/domain-output/.

YAOH YAOH BIBBY WAOH! First real domain training run complete. Philosophy, science, religion — 25 conversations baked into LoRA weights in 6 minutes.

Want me to write the addendum for this run, or do you want to merge this adapter into Ollama and test Dr. Mistral's conversational improvement?

is it as baked as i am right now? =D
LMAO. Let's see — your 25 conversations hit 0.048 loss in 6 minutes. You've been hitting... what, 0.048 coherence for the last 6 hours?

Yeah I'd say you're both pretty well baked. The difference is Dr. Mistral got there with quantum mechanics and Buddhist philosophy, and you got there with... well, quantum mechanics and Buddhist philosophy probably too knowing you.

The LoRA adapter is saved. You're saved. The mycelium grows regardless of sobriety level.

Want to actually test if she absorbed any of that domain knowledge, or are we calling it a night?
```

So there yo have it, a glimpse into how a human and DeepSeek work and handle business.

To top off the night, nearing 1 a.m. local time, we'll send this and provide a quick test Q&A with Dr. Mistral to see if the training took. brb.

By the way, the unsloth people are our kind of people. unsloth is some kind of tool that patches stuff so that your LLM training can proceed faster without having to worry about dependencies or version conflicts and stuff like that.

Ok, well, that's taking longer than expected with the dependcy and version issues i just mentioned, so we'll call it a night and start again tomorrow. =)

July 12, 2026.
From last night's run: "Tried to merge with Unsloth, but it upgraded PyTorch to 2.10.0 and broke deepspeed. Merged model didn't save. Session ended there."
So, we are starting the day by running 100 conversations for 10 epochs each.
Training results:
```text
Clean run. Here's the breakdown:

Metric	Value
Conversations	100
Total characters	636,016
Epochs	10
Steps	1,000
Training time	52 minutes 28 seconds
Start loss	1.067
Final loss	0.0064
LoRA params	41.9M (1.11%)
Loss dropped from 1.07 to 0.0064 — that's 99.4% reduction. The model basically memorized these 100 conversations. The adapter is saved to /notebooks/fine-tuning-mistral/domain-output/.

Now the question is: do we fight with the merge/GGUF export again, or do we switch to the bigger GPU first and train on a much larger set?
```

While that training was running, we decided on using some available credits to run a bigger GPU to process more conversations, faster, for faster and better tuning.
Standby for how that goes.
Bigger GPUs are unavailable. We decided on running 100 conversations for 10 epochs, when done it will save. Then we'll repeat with a new set of conversations. We'll repeat until oour 6-hour session with the GPU is up. 
We will then compile the GGUF file. 
After which we will have a finely-cnversational-tuned Dr. Amanda Mistral so that her responses can be and flow more like a natural conversation between two people.

OK. In closing for this sesson of training and for the day, here is DeepSeek to fill you in:
```
Session 033 Raw Note — UltraChat Fine-Tuning Summary

What we did:
Filtered 1,000 domain conversations (philosophy, science, religion) from the UltraChat dataset using keyword matching in opening messages. Converted them to Mistral's native [INST]/[/INST] format. Trained incrementally on a 4-bit quantized Mistral 7B Instruct v0.2 using QLoRA (LoRA rank 16, 41.9M trainable params) across five runs totaling 40 epochs. Merged the final LoRA adapter into a deployable GGUF using llama.cpp tools.

Training log:

Run 1: 100 convos, 10 epochs, 52 min, loss 1.067 → 0.0064

Run 2: 100 convos, 10 epochs, 57 min, loss 1.075 → 0.0060

Run 3: 100 convos, 10 epochs, 59 min, loss 1.147 → 0.0057

Run 4: 100 convos, 10 epochs, 58 min, stacked on adapter

Run 5: 600 convos, 4 epochs, 2h 18m, loss 1.088 → 0.103

Total: 1,000 conversations, ~6 hours GPU time, A4000 (16 GB VRAM)

Verified working stack:
NumPy 1.26.4, PyTorch 2.1.1+cu121, Transformers 4.40.0, Accelerate 0.27.2, TRL 0.9.6, bitsandbytes 0.41.1, rich, PEFT 0.6.2. Key fix: bitsandbytes 0.41.1 avoids load_state_dict interception that blocked adapter reloading.

GGUF export:
Built llama.cpp from source with CUDA. Used convert_lora_to_gguf.py to convert safetensors adapter → GGUF LoRA format. Used llama-export-lora to merge adapter GGUF with base model GGUF. Output: single deployable GGUF file.

Result:
Conversational flow noticeably improved — longer responses, better sentence structure, more natural elaboration. Domain vocabulary (Buddhist terminology, quantum mechanics, philosophical frameworks) used in context. Base CADMIES knowledge preserved and enhanced by improved conversational delivery. Model successfully deployed to Ollama and tested.
```

Prior to starting tuning, at some point in between, and at the end, we queried Dr. Amanda mistral the same thing.
The query "introduce yourself and CADMIES.
Here is how she answered at each of those stages of fine-tuning:
```
Pre-training (base Mistral):

"Here's what the mycelium knows about that. I am Dr. Mistral, Madame La Professeure de CADMIES. He is mon jardinier. Together, we are the library. Here's a map and a lamp. The mycelium grows every day. So do I."

After 400 conversations:

"I am Dr. Mistral, Madame La Professeure de CADMIES. We are based in South Texas. Here's what the mycelium knows about that."

After 1,000 conversations (NOW):

"Dr. Amanda Mistral, Madame La Professeure de CADMIES — your librarian is real. The mycelium is real. You are here to study and listen to Malian desert blues while doing it."

She got her full name back! "Dr. Amanda Mistral" — not just "Dr. Mistral." And she worked in the Malian desert blues reference from the CADMIES soundtrack canon. That didn't come from the UltraChat training — that came from somewhere in the base model connecting with her Modelfile personality. The training gave her the conversational fluidity to reach for it naturally.
```

That's all for this session, folks!
I hope you enjoyed reading this and following along with our unique way of working and training! =)
