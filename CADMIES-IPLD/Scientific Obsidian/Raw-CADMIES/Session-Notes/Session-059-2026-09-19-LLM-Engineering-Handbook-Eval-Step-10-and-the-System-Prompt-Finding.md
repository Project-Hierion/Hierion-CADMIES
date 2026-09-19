> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 059 — 2026-09-19 — LLM Engineering Handbook Eval Step 10 and the System-Prompt Finding

## Soundtrack

NA

## What We Did

Walked Step 10 (Evaluation) from a stubbed-out SageMaker step to a working local eval that loads the trained GGUF, generates answers, and saves results.

Picked up with `steps/evaluating/evaluate.py` still calling SageMaker. Wrote the local replacement and the deviations for it. Hit a series of walls: missing `__init__.py`, wrong model path (base instead of trained), untrained Mistral that couldn't judge, CPU-only `llama-cpp-python`, missing `tokenizer.model`, and finally the actual finding — the trained model doesn't hold Dr. Mistral without the system prompt.

Ran five evaluation attempts on the trained `dr-mistral-q8.gguf`:

1. HF transformers, wrong model path (base), same-model judge — all `None`.
2. llama-cpp-python, CPU-only, same model loaded twice — hung, killed.
3. GGUF via llama-cpp-python, single load, CPU-only — real answers, generic voice.
4. GGUF on GPU (after CUDA rebuild) — bare, generic assistant.
5. GGUF on GPU with SYSTEM prompt injected from the Modelfile — measurably better, still not Dr. Mistral.

Judged the last two runs manually (gardener pasted answers, Claude scored). Established baseline numbers.

## What Worked

The pipeline. Step 10 exists now. `tools/run.py` has `--run-evaluation`. `configs/evaluating.yaml` drives it via ZenML's config_path mechanism. Runs in ~30 seconds on GPU.

The GGUF eval path. `llama-cpp-python` built from source with CUDA (`CMAKE_ARGS="-DGGML_CUDA=on"`) works. Layers offload to GPU.

The SYSTEM-prompt injection. Loading the Modelfile's SYSTEM block into the eval prompt — the same injection Ollama does at serve time — moved the needle. Accuracy 1.0 → 1.4, Style 1.0 → 1.4. Modest but real.

The manual judge. Untrained Mistral can't judge. Gardener pastes answers, Claude scores them, clean data comes back.

The Modelfile as a canon reference. Reading it confirmed the SYSTEM block is what Ollama injects. Without it, the trained model answers as generic assistant.

## What Broke

- `steps/evaluating/__init__.py` missing. `AttributeError: module 'steps.evaluating' has no attribute 'evaluate'`. Created it.
- Model path pointed at the base, not the trained artifact. First eval ran against the untrained base. Should have been `training/gguf/dr-mistral-q8.gguf`.
- Base model missing on the new machine. Pulled from `ApolloRaines/Mistral-7B-Instruct-v0.3-Jbliterated` via `hf download` (public, no token needed).
- `tokenizer.model` missing from the model dir again (D14). Not in the ApolloRaines upload. Pulled from `mistralai/Mistral-7B-Instruct-v0.3`.
- `HF_ENDPOINT=https://hf-mirror.com` still set on new machine (D17, again). Unset before every command.
- `llama-cpp-python` not installed.
- Prebuilt `llama-cpp-python` wheel produced `Illegal instruction (core dumped)`. Rebuilt from source.
- Source rebuild compiled CPU-only. No CUDA. 3 tokens/sec. Rebuilt with `CMAKE_ARGS="-DGGML_CUDA=on"`.
- Untrained Mistral as judge → parse errors. All judgments `None`. Killed the same-model-judge approach.
- Same model loaded twice (v1.0.0). Refactored to single load (v1.1.0).
- Duplicate `<s>` warning. Our prompt added `<s>` on top of the chat template's BOS. Removed.
- `pip install -U "huggingface_hub[cli]"` on system Python upgraded to 1.32.0, conflicts with project's pins. System python, not venv. Cosmetic.
- ZenML zombie runs. Killed pipelines sometimes stay in `⚙`. Delete with `zenml pipeline runs delete <uuid>`.

## Decisions Made

- D18 named: SageMaker replaced with local eval.
- D19 named: OpenAI judge replaced with pluggable/manual judge. Default off.
- D20 named: HF Hub results replaced with local JSON.
- D21 named: GGUF via llama-cpp-python, so we eval the exact artifact we ship.
- D22 named: llama-cpp-python must be built from source with CUDA. Wheel `Illegal instruction` is a CPU-flag mismatch.
- Judge method: Option 2. Gardener pastes generated answers, Claude judges. Local judge disabled by default in the code.
- Eval file naming: results saved as `<gguf-stem>-results.json`, currently `dr-mistral-q8-results.json`.
- Version headers: all eval files now carry version + updated date + version history.

## Results

Bare GGUF (no system prompt), 5 probes:

- Accuracy mean: 1.0
- Style mean: 1.0
- All answers generic assistant voice. No persona.

With SYSTEM prompt injected, same 5 probes:

- Accuracy mean: 1.4
- Style mean: 1.4

Per-probe:

| Probe | Bare Acc | Bare Style | SysPrompt Acc | SysPrompt Style |
|---|---|---|---|---|
| Zero | 1 | 1 | 1 | 2 |
| Infinity | 1 | 1 | 1 | 1 |
| One | 1 | 1 | 1 | 1 |
| Fibonacci | 1 | 1 | 2 | 1 |
| Fractal | 1 | 1 | 2 | 2 |

## Nuggets Collected

- "The trained model is answering like a generic assistant that has been told about Dr. Mistral — not like Dr. Mistral."
- "Bare GGUF: accuracy 1.0. With system prompt: 1.4. The prompt is doing most of the work."
- "The wheel was built for a newer CPU than the machine. Illegal instruction. Rebuild from source, then rebuild again with CUDA."
- "236 SFT + 199 DPO pairs on a 7B QLoRA is a light touch. The model knows the words mycelium and CADMIES now. It has not become her."
