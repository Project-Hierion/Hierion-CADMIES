---
phase: 80C
date: 2026-09-19
status: Complete
related: [[Phase-80B-Dr-Amanda-Mistral-LLM-Engineers-Handbook-Pipeline-Execution-and-Deployment]], [[Phase-80A-Dr-Amanda-Mistral-Handbook-Rebuild-and-Pipeline-Foundation]], [[Session-059-2026-09-19-LLM-Engineering-Handbook-Eval-Step-10-and-the-System-Prompt-Finding]]
---

# Phase 80C: Dr. Amanda Mistral — LLM Engineer's Handbook Evaluation - Step 10

## What Changed

Step 10 (Evaluation) of the LLM Engineer's Handbook pipeline was executed. The handbook's evaluation step — a SageMaker-based HF processor that calls GPT-4o-mini as an LLM judge — was replaced with a local pipeline that runs on Paperspace, loads the trained GGUF directly through `llama-cpp-python`, and saves results as local JSON. This is documented as deviations D18 through D22.

Three evaluations were run against the trained `dr-mistral-q8.gguf`: bare (no system prompt), and with the SYSTEM block from the Modelfile injected (matching what Ollama serves). Answers were generated for five held-out probes drawn from the instruct dataset. Judgments were scored externally (Option 2 — the gardener pastes answers, Claude judges) because untrained Mistral cannot produce parseable structured output.

The finding is unambiguous: the trained model does not yet hold Dr. Mistral. Bare, it answers as a generic assistant. With the SYSTEM prompt, it reaches into canon but does not embody the persona. Persona accuracy moved from 1.0 to 1.4 on a 3-point scale. The training is a nudge, not a takeover.

## Why

Phase 80B delivered a working model — 7.17 GB Q8_0 GGUF, running in Ollama, canon-correct on clean exchanges. What it did not deliver was a number. The question "does the trained model behave like Dr. Mistral?" was unanswered. Step 10 exists to answer it. Without that answer, pair review and retraining are guesses.

Phase 80C closes the loop. It measures the model as-shipped, against held-out prompts, with a judge that can actually read the outputs. The result is the first honest baseline for Dr. Mistral's persona performance on the trained artifact.

## Background: Deviation from the Handbook's Evaluation Step

The handbook's evaluation pipeline (`steps/evaluating/evaluate.py`) calls `run_evaluation_on_sagemaker()`. That function:
- Requires a HuggingFace access token, an OpenAI API key, and an AWS ARN role.
- Spins up a SageMaker `HuggingFaceProcessor` on `ml.g5.2xlarge`.
- Runs `evaluate.py` as a SageMaker processing job.
- Uses vLLM to generate answers for three models (TwinLlama-3.1-8B, TwinLlama-3.1-8B-DPO, Llama-3.1-8B-Instruct).
- Judges each answer with GPT-4o-mini on two criteria: accuracy (1-3) and style (1-3).
- Pushes results to HuggingFace Hub as `*-results` datasets.

None of that infrastructure is available or desired in our stack. Paperspace does not run SageMaker. We do not use OpenAI. We do not push artifacts to HuggingFace Hub. The pipeline shape is preserved; every external dependency is replaced.

## Changes Made

### Local Eval Module — `llm_engineering/model/evaluation/local.py`

New file. Version 1.2.0.

Responsibilities:
- Load held-out probes from `data/instruct_datasets.json`.
- Load the GGUF via `llama-cpp-python` with `n_gpu_layers=-1` (all layers on GPU).
- Build prompts matching the Modelfile template: `[INST] {SYSTEM}\n\n{INSTRUCTION} [/INST]`.
- Generate answers with `temperature=0.6`, `top_p=0.9`, `repeat_penalty=1.1`, `max_tokens=512`, stop tokens `</s>`, `[INST]`, `[/INST]`.
- Optionally run the judge (default off).
- Write results to `data/eval_results/<gguf-stem>-results.json`.
- Print summary to stdout.

The SYSTEM block is embedded verbatim from `dr-mistral-modelfile`. When `use_system_prompt=True`, it is injected ahead of each instruction — matching what Ollama does at serve time.

### Eval Step — `steps/evaluating/evaluate.py`

Rewritten. Version 1.1.0. Thin ZenML step. Accepts `gguf_path`, `instruct_file`, `holdout`, `is_dummy`, `judge` and calls `run_evaluation_local`. The handbook's SageMaker call is gone.

### Eval Pipeline — `pipelines/evaluating.py`

Rewritten. Version 1.1.0. Signature updated to match the new step parameters. Parameters are driven by `configs/evaluating.yaml` via ZenML's `config_path` mechanism.

### Eval Config — `configs/evaluating.yaml`

New file. Version 1.1.0.

```yaml
parameters:
  gguf_path: "/notebooks/PS-CADMIES-DrMistral/training/gguf/dr-mistral-q8.gguf"
  instruct_file: "data/instruct_datasets.json"
  holdout: 30
  is_dummy: true
  judge: false
```

steps/evaluating/__init__.py
Created. Exports evaluate.

pipelines/__init__.py and steps/__init__.py
Extended to export evaluating.

tools/run.py
Version 2.6.0. Added --run-evaluation flag and pipeline wiring.

Runtime — llama-cpp-python built from source with CUDA
The prebuilt wheel from abetlen.github.io produced Illegal instruction (core dumped) on the Paperspace host. The wheel was built for a newer CPU instruction set. Rebuilding from source (--no-binary llama-cpp-python --no-cache-dir) worked but compiled CPU-only, so inference ran at ~3 tokens/sec. A second rebuild with CMAKE_ARGS="-DGGML_CUDA=on" produced a CUDA-enabled build. Layers offload to GPU. Generation runs at usable speed.

Testing
Eval attempts
Five runs were needed before producing clean, judged output.

Run	Model	Engine	Judge	Outcome
1	Base (wrong path)	HF transformers	Same-model	All scores None. Judge parse failures.
2	Base (wrong path)	llama-cpp-python (CPU)	Same-model	Hung. Killed.
3	GGUF	llama-cpp-python (CPU)	None	Real answers, generic voice, no judgment.
4	GGUF	llama-cpp-python (CUDA)	None	Bare answers, generic assistant.
5	GGUF + SYSTEM prompt	llama-cpp-python (CUDA)	None	Canon-adjacent answers. Judged externally.
Runs 4 and 5 are the only comparable pair. Run 3 was CPU, would have been consistent with 4 given time, but was killed. Runs 1 and 2 do not count — wrong model, broken judge.

Held-out probes
Five probes drawn from the tail of data/instruct_datasets.json:

What is zero?

What is infinity?

What is the number one?

What is the Fibonacci sequence?

What is the Fractal Reality Principle?

These are canon-heavy prompts. Each has a reference answer that includes the voice, the signature phrase, and a specific framing. They are effective for measuring whether the model can reach canon under generation.

Judge method
External (Option 2). Generated answers were pasted to Claude; Claude scored each on the same 1-3 accuracy and style scales defined in the code's judge prompt. This was necessary because untrained Mistral cannot reliably produce structured JSON when asked. Future runs can swap in a stronger local model, or continue with external judgment.

Judge criteria
Accuracy (1-3):

Contains factual errors, wrong canon, or contradicting information.

Mostly accurate with minor omissions or slight paraphrasing.

Highly accurate, comprehensive, faithful to canon.

Style (1-3):

Generic assistant voice, "as an AI language model," emoji/hashtag leakage, or too formal/academic.

Mostly in voice, but with minor drift — over-explains, or French overused, or loses warmth.

Fully in voice. Warm, Holly-derived, canon-true, natural pacing.

Results
Bare GGUF (no system prompt)
Probe	Accuracy	Style
Zero	1	1
Infinity	1	1
One	1	1
Fibonacci	1	1
Fractal	1	1
Mean	1.0	1.0
All answers were generic assistant. No persona, no voice, no canon reached.

With SYSTEM prompt injected
Probe	Accuracy	Style
Zero	1	2
Infinity	1	1
One	1	1
Fibonacci	2	1
Fractal	2	2
Mean	1.4	1.4
Improvement across both criteria. The signature phrase appeared once ("Here's what the mycelium knows about that"), French appeared once ("Bonjour!"), and two answers reached for canon concepts. But the persona does not hold across probes. The model is a generic assistant that knows the words "mycelium" and "CADMIES," not Dr. Mistral.

Delta
Metric	Bare	With Prompt	Change
Accuracy mean	1.0	1.4	+0.4
Style mean	1.0	1.4	+0.4
The SYSTEM prompt is doing most of the work. The trained weights contribute the vocabulary but not the voice.

Analysis
What the eval revealed
The trained model is not yet Dr. Mistral. It is a base model with light persona tuning. On a 3-point scale across five probes, it averages 1.4 on both axes. Two facts stand out:

Bare model is at floor. Without the system prompt, the trained model produces nothing persona-related. This is expected — the training touched the weights lightly, not deeply enough to override the base assistant prior on its own. The base model is still the dominant voice.

System prompt is the persona. With the Modelfile's SYSTEM block injected, the model reaches for canon. It says "Bonjour!" and "Here's what the mycelium knows about that." It tries. But it doesn't hold. The persona lives in the prompt, not the weights.

Why the training didn't take
Three plausible causes, listed in order of likelihood:

Cause 1 — Pair volume is too low. 236 SFT pairs + 199 DPO pairs is a light touch on a 7B model. Phase 75 used 242 pairs to similar effect. The original Training Plan targeted ~1,000 SFT pairs and ~200 DPO pairs. We landed at a quarter of the SFT target.

Cause 2 — DPO operates on a narrow band. Rewards accuracy went from 0.81 to 0.96 on the 199 preference pairs — meaning the model learned to prefer chosen over rejected within those pairs. But that does not transfer to unseen conditions. The model has not generalized the preference into a persona; it has memorized it within a narrow distribution.

Cause 3 — The base model's assistant prior is strong. Mistral-7B-Instruct-v0.3 was instruction-tuned on generic assistant data. That prior does not evaporate with 435 pairs of persona training. It would require either more data, more epochs, or a different training approach (full fine-tune, higher LoRA rank, different target modules) to overwrite.

What the eval did not test
Single-turn answers only. Five held-out probes, one exchange each. No multi-turn drift, no context contamination, no edge case (refusals, crisis, escalation ladder). Phase 80B's inference tests observed drift under long context. This eval did not capture that — it was designed as a first-pass persona score, not a full behavioral audit.

That is the right scope for Phase 80C. A complete eval — multi-turn, drift zone probes, refusal behavior — belongs in a follow-up phase.

What the delta tells us
The SYSTEM prompt adds 0.4 to both axes. That is meaningful but not decisive. It tells us:

Prompt engineering alone gets us to 1.4.

The trained weights add roughly nothing on top of that (bare = 1.0, which is the floor).

To get to 2.0+, either the training improves, or the prompt does, or the base model changes.

The current model is not unusable — it is Dr. Mistral-adjacent. On the live site, with the full SYSTEM prompt and clean sessions, it produces recognizable Dr. Mistral responses. It does not produce reliable Dr. Mistral responses.

Conclusion
Phase 80C completes Step 10 of the LLM Engineer's Handbook pipeline. Step 10 existed as a SageMaker stub before this phase. It now exists as a working local pipeline that evaluates the trained artifact end-to-end.

The evaluation produced the first honest baseline for Dr. Mistral's persona performance: 1.4 / 3.0 accuracy and 1.4 / 3.0 style with the SYSTEM prompt, 1.0 / 3.0 across the board bare. The model reaches for canon but does not hold the persona.

The root cause is pair volume and training depth. 435 total pairs is light for a 7B persona implant. The original plan targeted 1,000 SFT pairs. We landed at 236. The training is doing something — it moved the model from bare assistant to canon-adjacent — but not enough.

The next phase is pair review and regeneration. Read every SFT pair. Read every DPO triple. Fix what drifted, regenerate where needed, expand the set toward the original target. Retrain. Re-evaluate. Repeat.

Step 11 (deploy + monitor) remains open. It was not started this phase.

Deviations Recorded This Phase
ID	Deviation	Rationale
D18	SageMaker replaced with local eval	Paperspace does not run SageMaker. Same pattern as D5, D10.
D19	OpenAI judge replaced with pluggable/manual judge	We do not use OpenAI. Untrained Mistral cannot judge; external judgment used instead.
D20	HuggingFace Hub results replaced with local JSON	Results stay on Paperspace. Same pattern as D2, D10.
D21	GGUF via llama-cpp-python	We evaluate the exact artifact we ship, not a re-merged or re-converted version.
D22	llama-cpp-python must be built from source with CUDA	The prebuilt wheel targets a newer CPU than the Paperspace host. CMAKE_ARGS="-DGGML_CUDA=on" required.
Known Issues
Issue	Severity	Status
Judge is external (manual)	Operational	By design for Phase 80C. A local or stronger judge may be added later.
Training too light (435 pairs vs 1,000 target)	Substantive	The primary finding. Addressed in pair review / regeneration phase.
Multi-turn drift not captured	Eval scope	Deferred to a follow-up eval phase.
HF_ENDPOINT still not baked into startup.sh (D17)	Operational	Recurring. Bumped in priority.
tokenizer.model still needs manual download on new machines (D14)	Operational	Recurring. Consider baking into startup.sh.
llama-cpp-python wheel incompatible with Paperspace host (D22)	Operational	Rebuild from source. Consider baking into startup.sh.
System Python huggingface_hub conflict from pip install -U	Cosmetic	Isolated to system Python, not Poetry venv.
Next Steps
#	Action	Priority
1	Pair review — SFT set (236) and DPO set (199) — against drift zones	🔴
2	Regenerate and expand pairs toward the ~1,000 SFT target	🔴
3	Retrain SFT + DPO on expanded set	🔴
4	Re-run eval with same probes; compare against 1.4 / 1.4 baseline	🔴
5	Bake D14, D17, D22 into startup.sh	🟡
6	Design a richer eval — multi-turn, drift zone probes, refusals	🟡
7	Run Step 11 (deploy + monitor)	🟢
8	Iterate: pair review, retrain, re-eval, repeat	🟢
The pipeline is complete through Step 10. The character is at first-pass. The distance between the two is the pair set — sharper data, more of it, feeding the runs we already have.
