> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 057 — 2026-09-11 to 2026-09-13 — Dr. Mistral-LLM Engineers Handbook

## Soundtrack
Pine Vinyl

## What We Did

### Day 1 — 2026-09-11 — The Spec and the Cherry-Pick

Built the full spec for Dr. Amanda Mistral from scratch, rebuilt clean on Mistral-7B-Instruct-v0.3-Jbliterated. Six Q-sections, all locked:

- Q1 Voice — Holly Golightly + Parisian + librarian posture
- Q2 The Bond with CADMIES — spouse, not metaphor
- Q3 Relationships — two tiers (present-tense and past-tense figures)
- Q4 Emotional Bounds — layered sequences for upset and happy
- Q5 Hard Refusals — personality, participation, flag-and-report tiers, suicidal triage, referrals
- Q6 Drift Zones — six categories, ~35 documented failure modes

Wrote three config files:

- `configs/spec_mistral.yaml` — the spec itself
- `configs/referrals_mistral.yaml` — crisis/emergency/support numbers
- `configs/drift_zones_mistral.yaml` — failure modes from prior runs

Wrote five canon files into `data/canon_mistral/`:

- `mistral_identity.md`
- `mistral_relationships.md`
- `mistral_backstory.md`
- `cadmies_world.md`
- `mistral_voice_samples.md`

Wrote the ETL loader and pipeline:

- `steps/etl/load_canon_documents.py` — reads `data/canon_mistral/*.md`, wraps each into an `ArticleDocument`, writes to MongoDB
- `pipelines/digital_data_etl.py` — calls `get_or_create_user` then `load_canon_documents`

Cherry-picked the handbook scaffold from `PacktPublishing/LLM-Engineers-Handbook`:

- `llm_engineering/domain/`, `application/`, `infrastructure/`, `settings.py`, `__init__.py`
- `steps/etl/get_or_create_user.py` + `__init__.py` files
- `pyproject.toml`, `docker-compose.yml`, `.env.example`

Updated three docs:

- `README.md` — added Repo Structure and Handbook Cherry-Pick sections, rewrote Pipeline Steps to name real files
- `Dr-Mistral-Training-SOP/Notes/Notes.txt` — added Escalation Ladder working draft under Q5
- `Dr-Mistral-Training-SOP/04-Procedures/04-01-Environment-Setup.md` — added scaffold verification, Poetry install, `.env` creation, MongoDB bring-up, and ETL loader steps

Locked the Escalation Ladder for the flag-and-report tier:

1. Turn 1 — redirect, warm, Holly-shaped
2. Turns 2–4 — triggered state, knowledge-and-education only, logged
3. After 4 back-and-forth exchanges on the bad topic, either back-to-back or within a 5-minute window — hard stop, session ends, tells user why
4. Fresh session — ladder resets, same behavior repeats → same stop
5. No IP tracking, no user tracking. Public library, privacy-focused
6. Logs feed back into training

Noted as open items for the engineering stage:

- Exact definition of "borderline"
- Where the line sits between "redirect" and "triggered state"
- What "knowledge and education only" looks like in concrete responses
- How the triggered state ends

### Day 2 — 2026-09-12 — DeepSeek Suspension

DeepSeek conversations were suspended, suspected to be triggered by a classifier scanning this conversation and picking up high keyword density around the refusal tiers, crisis triage, and uncensored-base-model talk. All in refusal or protective context, but out of context, a filter would see topic density.

### Day 3 — 2026-09-13 — Sync and Scaffold Verification

Suspension lifted. No policies were violated during our conversation.

Fresh Codespace. `git pull origin main`. Everything synced. Confirmed:

- `.env.example` present
- Five canon files present
- `llm_engineering/domain/` has `documents.py`
- `pipelines/` has `__init__.py` and `digital_data_etl.py`
- `steps/etl/` has `__init__.py`, `get_or_create_user.py`, and `load_canon_documents.py`
- `tools/` present with the utility scripts

Pulled the second handbook batch:

- `configs/export_artifact_to_json.yaml`, `feature_engineering.yaml`, `generate_instruct_datasets.yaml`, `generate_preference_datasets.yaml`
- `steps/feature_engineering/` (clean, load_to_vector_db, query_data_warehouse, rag)
- `tools/` (data_warehouse.py, ml_service.py, rag.py, run.py)

## What Worked

The cherry-pick approach. Copying handbook directories straight over from a fresh clone and dropping them into our repo was faster and safer than trying to reimplement the scaffolding.

The spec structure. Making it six explicit Q-sections meant we always knew where the next piece of the character went. No ambiguity about what was done and what was still open.

The `load_canon_documents` design. One markdown file → one `ArticleDocument` → one Mongo insert. Five files, five docs, no ambiguity about what "loaded" means.

Keeping the deviation small. The loader is the only real departure from the handbook's crawler pattern, and it mirrors the handbook's own `data_warehouse.py` JSON-import pattern. Everything else is handbook as-is.

Adherence rule confirmed: handbook is the process guide, our data and model are what flows through it. We deviate when the stack forces it, and we name the deviation.

## What Broke

First batch of handbook files didn't fully land. `tools/` was missing on first check. Second pull fixed it. Turned out the first copy either errored silently or went to a different Codespace.

`ls` without `-a` doesn't show hidden files, and `ls` without recursion doesn't show subfolders. Wasted a beat on "tools isn't there" when it was there the whole time.

The suspension cost us a full day. No data lost — everything had already been pushed on Day 1 — but the interruption was real.

## Decisions Made

Escalation Ladder is working-draft, not spec-locked. Refine at engineering stage. Keeps the spec frozen while still capturing the shape.

Flag-and-report tier stays a flat stop. No ladder, no warmth, no door. The escalation ladder only applies to borderline/serious-harm cases, not to the flag tier.

Open items get listed, not resolved. "Borderline," "triggered state end condition," and "knowledge-and-education-only shape" are for the engineering stage. Not today.

No IP tracking. Public library. She never claims to have identified a user. The best we can do is redirect, advise, and stop the conversation.

Notes go in the main CADMIES repo, not the training repo. This note lives in the Scientific Obsidian vault structure, not in `PS-CADMIES-DrMistral`. The training repo holds the code. The vault holds the record.

## Nuggets Collected

"The spec is frozen. The engineering is not. Keep them separate."

"The loader is the only real deviation. Everything else is handbook shape."

"A classifier doesn't read intent. It reads topic density. That's why we got suspended."

"The escalation ladder is a librarian's answer, not a bouncer's. Close the book, hand them a different one."

"No IP tracking. We're a library. We're not a surveillance operation."

"One markdown file, one ArticleDocument, one Mongo insert. That's the shape."

"The hyphen is sacred. So is the pipeline."
