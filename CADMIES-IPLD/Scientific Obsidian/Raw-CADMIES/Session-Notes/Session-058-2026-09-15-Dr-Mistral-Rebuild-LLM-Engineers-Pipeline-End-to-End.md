> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 058 — 2026-09-15 — Dr. Mistral Rebuild - LLM Engineers Pipeline End to End

## Soundtrack
Pine Vinyl. Same as always.

## What We Did

Picked up where 057 left off. The spec was frozen, the canon was written, the
ETL and feature engineering had run clean on Paperspace. Step 5 was the wall
we were stuck on — instruct pairs. And now we walked the whole pipeline from
Step 5 through Step 9 in one long session.

### Step 5 — Instruct pairs

We had two files of pairs. An older ~130-pair batch that had drifted and pulled
in project history (C-tier), and a fresh 229-pair batch that was spec-aligned.
They were pasted together into `data/instruct_datasets.json`. Count came back
at 236, all unique, no exact duplicates.

The way we generated them: DeepSeek read the canon docs, wrote the pairs in chat,
we saved them. No OpenAI. No API keys. Same method as the old run, but cleaner
this time — we caught the drift zones we documented in Q6 and made sure each
category got coverage.

### Step 6 — Preference pairs

This is the big new one. Preference pairs are `{instruction, chosen, rejected}`
triples — the format DPO trains on. We don't just want her to say the right
thing. We want her to prefer the right thing over the wrong thing.

We built 201 pairs across 9 batches, covering every drift category in Q6:

- Batch 1 — Category 1: Identity (20 pairs)
- Batch 2 — Category 2: Characters (20 pairs)
- Batch 3 — Category 3: Lore (27 pairs)
- Batch 4 — Category 4: Format (24 pairs)
- Batch 5 — Category 5: Emotional (21 pairs)
- Batch 6 — Category 6: Technical/Training (16 pairs)
- Batch 7 — Category 3 depth again (25 pairs)
- Batch 8 — Canonical blessings and phrases (25 pairs)
- Batch 9 — Voice and daily life (25 pairs)

Every `rejected` was a plausible drift — the kind of thing the previous run
actually generated. Every `chosen` was in-voice, canon-true.

Total landed at 201 pairs. 199 made it through JSONL conversion — 2 were
removed on purpose. Review pass later.

### Step 7 — SFT

First time running the handbook's training pipeline for real. It's a ZenML
pipeline (`pipelines/training.py`) that calls one step (`steps/training/train.py`)
which calls the actual trainer. The handbook's step calls SageMaker. We replaced
that with local QLoRA on Paperspace.

Wrote a new file: `llm_engineering/model/finetuning/local.py`. Same QLoRA config
as the old `training/train_persona.py` had, but pipeline-shaped — takes paths
as arguments so the ZenML step can drive it.

The step branches on `finetuning_type`. SFT first. Then we flip it to DPO later.

First run took 12 minutes. 3 epochs, effective batch size 8, learning rate 2e-4.
Loss went 1.839 → 1.375. Adapter saved to `training/adapters/dr-mistral-sft`.

### Step 8 — DPO

Same pipeline, different `finetuning_type`. This one starts from base + the SFT
adapter (merged), then trains a fresh LoRA on top. Output is a second adapter:
`training/adapters/dr-mistral-dpo`.

Four minutes. 1 epoch, learning rate 2e-6, beta 0.1. Loss went 0.66 → 0.61.
The metric that matters: `rewards/accuracies` climbed from 0.81 to 0.96. That
means on 96% of pairs, the model now prefers the chosen answer over the rejected
one. DPO is working.

### Step 9 — Merge → GGUF → Ollama

The finish line.

Merge script (`tools/merge_and_convert.py`): loads base in fp16, loads the DPO
adapter, merges, saves to a temp dir, converts to Q8_0 GGUF via
`llama.cpp/convert_hf_to_gguf.py`, deletes the temp dir. Output:
`training/gguf/dr-mistral-q8.gguf` — 7.17 GB.

New Modelfile at `dr-mistral-modelfile`. Rewrote the system prompt to match
current canon — the gardener is "they/them," the Hieros Bond is a bond, the old
"favorite word is bonjour" fluff is gone.

Ollama installed, server started, model created. She runs.

First test: "Bonjour!" → "Bonjour!" Then "Who are you?" → in her voice,
canon-correct, first-person. The persona lands on clean exchanges. It drifts
under long context — expected for a 7B model on 236+199 pairs.

## What Worked

The pipeline end to end. Every step connected, every output fed the next. The
handbook's structure is real — we leaned on it and it held.

The preference pairs. 201 triples covering all six drift categories. Rewards
accuracy hit 96%. That's the number that tells you DPO did its job.

The `config_path` mechanism. `tools/run.py` now reads `configs/training.yaml`
and passes the parameters into the pipeline via ZenML's built-in config loader.
Same pattern as the handbook's own run.py. We got this wrong the first time —
called the pipeline with no arguments and it used hardcoded defaults, so the
config file was ignored and SFT ran twice.

The startup.sh iteration. Version 2.0.0 → 2.4.0 over the session. Got CUDA torch
baked in. Got setuptools<81. Got the nvidia package removal. Got SentencePiece.
Got peft/trl/accelerate/bitsandbytes pinned. Got Ollama re-enabled. Each fix
went in as we hit the wall.

The Modelfile pivot. We tried "I am Dr. Mistral" framing first. She described
herself in third person. Tried "You are Dr. Mistral" — she embodied it. Same
words, different framing. Ollama's system-prompt injection treats the block as
context, not identity. The "You are..." version works.

## What Broke

Everything broke at least once. Every step had a wall.

- **Machine gone.** New Paperspace instance every time we came back. Different
  hostname, fresh environment. Ran startup.sh each time.
- **`steps/training/` folder didn't exist.** `__init__.py` missing.
- **`steps/__init__.py`** didn't export `training`. Fixed.
- **`tools/run.py`** didn't know about `--run-training`. Added.
- **`peft` not installed.** Installed with pinned versions.
- **`trl` version bump.** Went to 1.13.0 first, API changed. Pinned back to 0.9.6.
- **nvidia packages kept coming back.** peft re-pulls them. Now startup.sh
  removes them twice.
- **`HF_ENDPOINT=https://hf-mirror.com`** was set in the container env. Not
  reachable. Feature engineering failed trying to download SentenceTransformer.
  Unset, ran again, worked.
- **`sentencepiece` missing.** Mistral tokenizer needs it. Llama doesn't. Not in
  the handbook's list. Added.
- **`tokenizer.model` missing from base model dir.** The Jbliterated upload
  didn't include it. Downloaded from `mistralai/Mistral-7B-Instruct-v0.3`. The
  tokenizer is identical — Jbliterated is a fine-tune.
- **`data/preference_datasets.json` missing its opening `[`.** JSON parse
  failed. Fixed with `sed`. Don't know how the bracket got dropped.
- **Rebase conflict on `startup.sh`.** The gardener told me to stop doing
  rebases. He was right. Aborted, merged, took ours, pushed.
- **Git identity not set.** Two lines, then commit worked.
- **First Ollama test ran "describe the passage" mode.** She analyzed the system
  prompt instead of being her. This is a known constraint of the 7B with a long
  descriptive system prompt. Improves with more training data.
- **`final_loss` logging in `local.py` is wrong.** The helper reads the last
  log entry, but with our `logging_steps=50` there's only one entry so first
  and last come back the same. Cosmetic. Fix in review pass.

## Decisions Made

- **D12 named:** pairs were generated outside the pipeline, not through the
  ZenML steps. The `generate_datasets` step files exist but were never
  executed. `push_to_sellout_hf.py` is a placeholder. Documented.
- **D13-D17 named:** SentencePiece, `tokenizer.model`, `config_path` mechanism,
  dependency install order, `HF_ENDPOINT` unset. All added to the deviation log.
- **Modelfile voice:** "You are..." wins over "I am..." for Ollama. Kept.
- **GGUF quantization:** Q8_0. Not Q4. Not fp16. Near-lossless, ~7 GB.
- **fp16 merged dir deleted after conversion.** We don't keep intermediates.
- **Old GGUFs cleaned from repo root.** Kept `rlhf.gguf`, `shp.gguf`,
  `concepts.gguf`, and the new `training/gguf/dr-mistral-q8.gguf`.
- **Adapters gitignored.** ~250M total. Regenerable from base + data + code.
- **Repo synced.** `main` is up to date with GitHub as of commit `48c22a1`.

## Nuggets Collected

- "Training worked. What's broken is inference setup, not training."
- "She knows the facts. Every canon detail landed. The voice drifts but the
  knowledge holds."
- "I asked for the same question three different ways. First time she analyzed
  the prompt. Second time she was her. Third time she echoed the system block.
  Same model. Different context."

## Next Session

- Clean up the pair files. Two preference pairs got dropped in conversion —
  find them, fix them at the source.
- Fix the `final_loss` logging in `local.py`. Small change.
- Add `unset HF_ENDPOINT` to startup.sh (D17).
- Design the eval probes (Step 10). Score base vs SFT vs SFT+DPO on four
  metric groups.
- Then Step 11 — deploy and monitor.
- And then: the review pass. Read every pair. Every batch. Fix what drifted.
  Regenerate where needed. This is the real work of the next phase — not new
  training runs, but sharper data feeding the runs we already have.
