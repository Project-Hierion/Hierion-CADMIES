---
system: Paperspace
date: 2026-05-15
status: Active
related: [[Architecture Overview]], [[Two-System Setup]], [[Harvester Pipeline]]
---

# Paperspace Session Protocol

Step-by-step procedure for launching a CADMIES GPU session on Paperspace Gradient. The workspace uses a git clone at `/notebooks/CADMIES/CADMIES-IPLD/` as the single source of truth.

## Prerequisites

- Paperspace Pro plan ($8/mo, unlimited A4000 sessions, 6hr per session)
- GitHub repo cloned to `/notebooks/CADMIES/CADMIES-IPLD/`
- `startup.sh` present at the project root

## Launch Sequence

### 1. Start Machine

Open Paperspace Gradient. Start a notebook with A4000 GPU.

### 2. Git Pull (Code Sync)

```bash
cd /notebooks/CADMIES/CADMIES-IPLD && git pull
```

This syncs all scripts, tools, and the harvester from GitHub. No manual upload needed for code changes.

### 3. Upload & Untar Blockstore (Data Sync — if needed)

Only required if new concepts were minted locally and the blockstore changed. If only code changed, skip to step 4.

Upload the tar to Paperspace via the notebook file browser, then:

```bash
cd /notebooks
tar -xzf cadmies_XXX.tar.gz -C /notebooks/CADMIES/CADMIES-IPLD/
```

Replace `XXX` with the current tar number.

### 4. Run Startup Script

```bash
cd /notebooks/CADMIES/CADMIES-IPLD && bash startup.sh
```

Installs system dependencies (zstd), Ollama (if not present), Python packages (dag-cbor, ollama), and starts the Ollama service. Takes approximately 30 seconds.

### 5. Pull LLM Model (if not cached)

Check what's available:

```bash
ollama list
```

If Mistral is missing:

```bash
ollama pull mistral:7b
```

For deep enrichment (optional):

```bash
ollama pull codestral:22b
```

### 6. Verify Model (optional)

```bash
ollama run mistral:7b
````

Quick interactive test. `Ctrl+D` to exit. Note: this is direct chat, distinct from the harvester's API calls.

### 7. Harvest

```bash
cd /notebooks/CADMIES/CADMIES-IPLD
python harvest/harvest_full_pipeline.py --auto --with-relationships
```

For review mode, omit `--auto`. For Codestral enrichment, add `--model codestral`.

## Quick Reference

|Step|Command|When|
|---|---|---|
|Sync code|`git pull`|Every session|
|Sync data|`tar -xzf cadmies_XXX.tar.gz`|After local minting|
|Setup|`bash startup.sh`|Fresh sessions|
|Pull model|`ollama pull mistral:7b`|If model missing|
|Harvest|`python harvest/harvest_full_pipeline.py --auto --with-relationships`|Every session|

## Post-Harvest

After minting, tar the updated blockstore back to local:

```bash
cd /notebooks/CADMIES/CADMIES-IPLD
tar -czf /notebooks/cadmies_local_XXX.tar.gz store/
```

Download the tar from Paperspace to local. Unpack into the local repo.

## Two Pipes Principle

- **Code travels by git.** Scripts, tools, prompts — all synced via GitHub.
    
- **Data travels by tar.** Blockstore CBOR files and new source_concepts — bundled and transported between systems.
    
- Never mix the two. Never upload code manually. Never commit binary blobs.
    

## Notes

- Paperspace sessions timeout after 6 hours. Save work and download tars before the session ends.
    
- The old `/notebooks/` workspace (bare files from tar uploads) has been purged. The clone at `/notebooks/CADMIES/CADMIES-IPLD/` is the only workspace.
    
- If the clone is missing on a fresh machine: `git clone https://github.com/Hieros-CADMIES/CADMIES.git /notebooks/CADMIES/`