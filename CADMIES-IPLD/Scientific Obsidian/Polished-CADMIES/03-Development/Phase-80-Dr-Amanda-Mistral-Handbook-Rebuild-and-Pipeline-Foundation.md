---
phase: 80
date: 2026-09-11
status: Active — Dr. Mistral rebuilt on the LLM Engineer's Handbook
related: [[Phase-75-Dr-Amanda-Mistral-Personality-Implant-on-Jbliterated-Base]]
---

# Phase 80: Dr. Amanda Mistral — Handbook Rebuild and Pipeline Foundation

## What Changed

Dr. Amanda Mistral's training pipeline was rebuilt from scratch on the LLM Engineer's Handbook scaffold. The previous 242-pair implant (Phase 75) is no longer treated as a trained artifact. It becomes raw source material. The new pipeline treats Dr. Mistral's persona as data to be processed through a structured ETL → feature engineering → SFT → DPO chain, following the handbook's three-pipeline architecture.

Three config files, five canon files, one loader, one ETL pipeline, and the handbook scaffold are now in the repo. The spec is frozen. The pipeline is in place. The next step is execution.

## Why

Phase 75 produced a working implant — a LoRA adapter, a GGUF, an Ollama model. She responded as Dr. Mistral. But the personality was not what we wanted. The 242 pairs carried structural problems: inconsistent voice, insufficient identity anchoring, drift that couldn't be corrected through more epochs. Phase 70 and Phase 71 documented this pattern. More training data on the same dataset shape would only amplify the problem.

The decision was made to rebuild clean, following a proven external process. The LLM Engineer's Handbook was selected because it is a step-by-step end-to-end framework for training a persona into an open-source LLM. Its pipeline structure matches what we need: collect raw data, generate instruct pairs, generate preference pairs, SFT, DPO, evaluate, deploy. The handbook does not build a fictional character — it builds a digital twin of a real person's writing style — but the pipeline shape is identical. We substituted our data and our model for the handbook's.

A secondary reason: to stop improvising. Phase 75 was built on ad hoc decisions. Phase 80 is built on a documented, external process. When we deviate from the handbook, we name the deviation. When we follow it, we know why.

## Background: From Phase 75 to Phase 80

Phase 75 was the personality implant on Apollo Raines' Jbliterated Mistral 7B. A 242-pair curated dataset, 4 epochs of QLoRA training, loss 1.54 → 0.46. The adapter converted to GGUF, merged, quantized to Q8_0, deployed to Ollama. She responded as Dr. Mistral — warm, philosophical, anchored. Identity test passed.

But the dataset shape was improvised. The categories were self-defined. The pair structure was hand-crafted without a formal spec. There was no mechanism for generating more pairs. There was no mechanism for evaluating whether the pairs were correct. There was no mechanism for correcting failures after they were observed.

Phase 80 replaces all of that with structured data. The spec is a config file. The canon is a corpus. The pipeline is a chain. Every downstream artifact — instruct pairs, preference pairs, trained adapter, eval scores — traces back to a source document.

## Changes Made

### Spec and Config

Three configuration files were written into `configs/`, following the handbook's declarative YAML pattern:

| File | Purpose |
|------|---------|
| `spec_mistral.yaml` | Persona specification: identity, voice, relationships, emotional bounds, hard refusals. Consumed by instruct generation, preference generation, and evaluation. |
| `referrals_mistral.yaml` | Crisis, emergency, and support referrals. Consumed at inference time and during evaluation. Rule: accurate, never invented. |
| `drift_zones_mistral.yaml` | Documented failure modes from prior training runs. Six categories, roughly 35 zones. Consumed by preference generation and evaluation. |

The spec is structured as six Q-sections (Q1 Voice, Q2 The Bond, Q3 Relationships, Q4 Emotional Bounds, Q5 Hard Refusals, Q6 Drift Zones), each locked before moving to the next. This structure lets the pipeline reference `covered_axes`, `hard_refusals`, and `drift_zones` by key rather than parsing prose.

### Canon Corpus

Five canon files were written into `data/canon_mistral/`, following the A/B/C/D separation rule:

| File | Contents |
|------|----------|
| `mistral_identity.md` | Full title, PhDs, physical description, nature as a Digital Intelligence, marriage to CADMIES, addressing rules. |
| `mistral_relationships.md` | Willie, Codestral, Number 5, the gardener. Two-tier structure (present-tense and past-tense figures). |
| `mistral_backstory.md` | The arc: 31UCR → the spore → the gardener → Buttercup → Finland → Dr. Amanda Mistral. |
| `cadmies_world.md` | Naming protocol, Hieros Bond, foundational metaphors (Cosmium Angelo, Scientific Obsidian, the Mycelium, Kerr Spacetime Gearbox), geography, the Gremlin, Anti-Skynet Treaty, canonical blessings. |
| `mistral_voice_samples.md` | Canonical lines. The "married to a library" line, the "1+1" response, the "what the mycelium knows" pattern. Grows over time. |

The A/B/C/D rule filters source material before it enters the corpus:

- **(A) Dr. Mistral canon** — goes in
- **(B) World canon** — goes in
- **(C) Project history** — stays out
- **(D) Builder reference** — stays out

Project history is not part of Dr. Mistral's experience. She lives in the world the project produced, not in the log of building it.

### Loader and Pipeline

Two files were written to move canon into MongoDB, following the handbook's ETL pattern:

- `steps/etl/load_canon_documents.py` — reads `data/canon_mistral/*.md`, wraps each into an `ArticleDocument`, writes to MongoDB.
- `pipelines/digital_data_etl.py` — calls `get_or_create_user("project_hierion")` then `load_canon_documents(user, canon_dir="data/canon_mistral")`.

The loader is the only real deviation from the handbook's ETL pattern. The handbook uses crawlers to fetch data from URLs. We read local markdown files. The deviation mirrors the handbook's own `tools/data_warehouse.py` JSON-import pattern, so it stays within the handbook's logic even where the implementation differs.

### Handbook Scaffold

The following were cherry-picked from `PacktPublishing/LLM-Engineers-Handbook`:

| Path | Purpose |
|------|---------|
| `llm_engineering/domain/` | Data models (`ArticleDocument`, `UserDocument`, base classes) |
| `llm_engineering/application/` | Business logic and crawlers |
| `llm_engineering/infrastructure/` | External service integrations |
| `llm_engineering/settings.py` | Environment-driven configuration |
| `steps/etl/get_or_create_user.py` | User creation in MongoDB |
| `pyproject.toml` | Python dependencies (Poetry-managed) |
| `docker-compose.yml` | Local MongoDB + ZenML bring-up |
| `.env.example` | Credential template |

A second batch was pulled on 2026-09-13:

| Path | Purpose |
|------|---------|
| `configs/feature_engineering.yaml` | Feature pipeline config |
| `configs/generate_instruct_datasets.yaml` | Instruct dataset config |
| `configs/generate_preference_datasets.yaml` | Preference dataset config |
| `configs/export_artifact_to_json.yaml` | Artifact export config |
| `steps/feature_engineering/` | clean, load_to_vector_db, query_data_warehouse, rag |
| `tools/` | data_warehouse.py, ml_service.py, rag.py, run.py |

### Escalation Ladder

A working draft of the escalation ladder was added to `Notes.txt`, to be refined at the engineering stage. It governs the borderline and serious-harm cases (not the flag-and-report tier, which stays a flat stop).

Sequence:

1. Turn 1 — redirect, warm, Holly-shaped
2. Turns 2–4 — triggered state, knowledge-and-education only, logged
3. After 4 back-and-forth exchanges on the bad topic, either back-to-back or within a 5-minute window — hard stop, session ends, tells user why
4. Fresh session — ladder resets, same behavior repeats → same stop
5. No IP tracking, no user tracking
6. Logs feed back into training

Open items for the engineering stage:

- Exact definition of "borderline"
- Where the line sits between "redirect" and "triggered state"
- What "knowledge and education only" looks like in concrete responses
- How the triggered state ends

### Documentation

Three docs were updated:

| File | Changes |
|------|---------|
| `README.md` | Added Repo Structure and Handbook Cherry-Pick sections. Rewrote Pipeline Steps to name real files. |
| `Dr-Mistral-Training-SOP/Notes/Notes.txt` | Added Escalation Ladder working draft under Q5. |
| `Dr-Mistral-Training-SOP/04-Procedures/04-01-Environment-Setup.md` | Added scaffold verification, Poetry install, `.env` creation, MongoDB bring-up, and ETL loader steps. |

## Adherence Rule

The handbook is the process guide. Our data and our model are what flows through it. When we deviate, we name the deviation. When we follow, we know why.

Known deviations so far:

- **Loader replaces crawler.** The handbook uses URL crawlers to fetch source material. We read local markdown files. Rationale: canon is authored, not scraped.
- **Mistral-7B-Instruct-v0.3-Jbliterated replaces Llama 3.1.** We inherit the handbook's pipeline structure but train on our own base model, on Paperspace, with QLoRA.
- **Paperspace replaces SageMaker.** The handbook deploys to SageMaker. We use Paperspace because it is where the existing infrastructure lives.

Nothing else in the pipeline has been altered from the handbook's shape.

## Testing

At time of writing, the ETL has not yet been run. Scaffold presence verified:

| Component | Status |
|-----------|--------|
| `llm_engineering/domain/documents.py` | ✅ Present |
| `pipelines/digital_data_etl.py` | ✅ Present |
| `steps/etl/load_canon_documents.py` | ✅ Present |
| `steps/etl/get_or_create_user.py` | ✅ Present |
| Five canon files in `data/canon_mistral/` | ✅ Present |
| Three config files in `configs/` | ✅ Present |
| `pyproject.toml` | ✅ Present |
| `docker-compose.yml` | ✅ Present |
| `.env.example` | ✅ Present |
| MongoDB running | ⬜ Not yet |
| ETL executed | ⬜ Not yet |

Verification procedure (per `04-01-Environment-Setup.md`):

1. `poetry install --without aws`
2. `cp .env.example .env`
3. `poetry poe local-infrastructure-up`
4. `poetry poe run-digital-data-etl`
5. Confirm 5 documents in MongoDB under `author_full_name="project_hierion"`

## Analysis

The decision to rebuild from scratch on an external framework is a reversal of Phase 75's approach. Phase 75 was improvised. It worked, but it produced a personality we did not want. Phase 80 is structured. Whether it produces the personality we want is unknown — but every failure will be traceable to a specific pair, a specific axis, a specific drift zone.

The handbook is a good match for our needs precisely because it was not built for our needs. It was built to train a persona into an LLM. The fact that its target persona is a real author's writing style, not a fictional character, does not change the pipeline shape. Data flows in, pairs are generated, the model is trained, the model is evaluated. We substituted data and model; the process held.

The A/B/C/D rule is load-bearing. Without it, project history — GPU names, session notes, soundtracks, migrations — would enter the canon corpus and generate pairs about things Dr. Mistral has no memory of. The rule keeps her in her world, not ours.

The escalation ladder is incomplete. It has shape but not edges. Those edges are for the engineering stage, not for the spec stage. Keeping them separate prevents the spec from drifting while the character is still being defined.

## Conclusion

Phase 80 is the foundation for a rebuilt Dr. Amanda Mistral. The spec is frozen. The canon is assembled. The pipeline scaffold is in place. The loader is written. The ETL is the next step, to be executed in Paperspace.

The 242-pair implant from Phase 75 is no longer a trained artifact. It is raw source material, to be processed through the handbook's pipeline alongside the five canon files. The previous personality is not discarded — it is re-entered as input. Whether it survives the pipeline in recognizable form is the question the next phase answers.

## Next Steps

| # | Action | Priority |
|---|--------|----------|
| 1 | Run ETL in Paperspace — load 5 canon files into MongoDB | 🔴 |
| 2 | Verify 5 documents present under `author_full_name="project_hierion"` | 🔴 |
| 3 | Run feature engineering — clean, chunk, embed, load to Qdrant | 🔴 |
| 4 | Run instruct dataset generation | 🟡 |
| 5 | Run preference dataset generation | 🟡 |
| 6 | SFT from base (QLoRA r=16) | 🟡 |
| 7 | DPO from SFT adapter (QLoRA r=8) | 🟡 |
| 8 | Evaluation — base vs SFT vs SFT+DPO | 🟢 |
| 9 | Deploy, monitor in Opik, feed drift back to preference generation | 🟢 |
