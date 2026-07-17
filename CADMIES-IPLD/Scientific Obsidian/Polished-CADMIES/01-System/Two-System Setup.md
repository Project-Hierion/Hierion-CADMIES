---
system: CADMIES
date: 2026-05-15
status: Active
related: [[Architecture Overview]], , [[Three-Model Arsenal]]
---
# Two-System Setup
CADMIES operates across two machines with distinct roles. This separation keeps GPU costs low, preserves long-term storage locally, and ensures the pipeline is reproducible.
## Systems
| System | Role | Hardware | OS |
|--------|------|----------|-----|
| Local (HP Laptop) | Development, storage, git, public gateway | CPU, external PNY drive | Fedora Silverblue 44 |
| Paperspace Gradient | LLM inference, batch harvesting, relationship generation | A4000 GPU (16GB VRAM, 45GB RAM) | Ubuntu (cloud notebook) |
## What Lives Where
### Local
- Git repository (source of truth for code)
- Blockstore (long-term storage, 367+ CBOR blocks)
- Source concepts (editable JSON definitions)
- Public gateway generation scripts
- Scientific Obsidian vault (soon)
- CADMIES GUI (Tkinter)
- Willie (local-only concept reader agent)
### Paperspace
- Ollama + three models (TinyLlama, Mistral 7B, Codestral 22B)
- Harvester pipeline execution
- Relationship generator execution
- Mycelium map generation
- Temporary blockstore (synced from local via tar)
## Sync Protocol
### Code: Git
Code travels from local to Paperspace via GitHub. Edit locally, commit, push. Paperspace pulls before each session.
```bash
# Local
git add -A && git commit -m "message" && git push
```

```
# Paperspace
cd /notebooks/CADMIES/CADMIES-IPLD && git pull
```

### Data: Tar
Blockstore data travels via tar archives. CBOR files are gitignored (binary blobs don't produce meaningful diffs).

bash
```
# Local — create archive
cd /run/media/fedora/PNY/CADMIES/CADMIES-IPLD
tar -czf ../cadmies_local_XXX.tar.gz store/
```

# Paperspace — extract archive

```
cd /notebooks
tar -xzf cadmies_local_XXX.tar.gz -C /notebooks/CADMIES/CADMIES-IPLD/
```

### Two Pipes Principle

- **Code travels by git.** Never upload scripts manually.
    
- **Data travels by tar.** Never commit binary blobs.
    
- The blockstore is the bridge — synced before and after GPU sessions.
    

## Why Two Systems

1. **Cost.** Running a GPU 24/7 is expensive. Paperspace Pro ($8/mo) gives unlimited A4000 sessions, 6 hours each. Pay only for what you use.
    
2. **Storage.** Local machine holds the canonical blockstore. Paperspace sessions are ephemeral — data must be tar'd back.
    
3. **Reproducibility.** Anyone with a Paperspace account and a git clone can replicate the entire pipeline.
    
4. **Future-proofing.** When budget allows for a local GPU (GTX 1650 LP or similar), the same scripts run locally without modification.
    

## Paperspace Machine Specs

- **Plan:** Pro ($8/month)
    
- **GPU:** A4000 (16GB VRAM)
    
- **RAM:** 45GB
    
- **Session Limit:** 6 hours (unlimited sessions)
    
- **Notebook Environment:** Gradient notebooks with terminal access