---
phase: 52
date: 2026-05-25
status: 📋 Designed — pending implementation
related: [[Phase-45-Snagnar-HIEROS]], [[Session-020]], [[Codestral-Audit-001]]
---

# Phase 52: llama.cpp Integration

## What This Is

Integration of Snagnar's llama.cpp fork as a replacement for Ollama on Paperspace, enabling faster inference, persistent prompt caching, and session-to-session memory for Mistral.

## Why

Ollama has served well but introduces overhead: model loading on each cold start, no persistent caching across sessions, and inference speeds that could be improved. Snagnar's llama.cpp fork is CUDA-accelerated and supports persistent prompt caching — Mistral could "remember" previous conversations without re-processing the entire context window.

Additionally, Phase 52 was scoped during the Session 020 Codestral audit, which identified the need for faster inference to enable more aggressive relationship generation and concept harvesting.

## Design

### Architecture

- llama.cpp runs alongside or replaces Ollama on Paperspace
- Persistent prompt cache stores Mistral's attention state across sessions
- Relationship generator and harvester can use either backend

### Expected Improvements

| Metric | Ollama (current) | llama.cpp (target) |
|--------|-----------------|-------------------|
| Cold start | ~15s model load | ~5s (cached) |
| Batch inference | 2-4s per batch | 1-2s per batch |
| Session memory | None | Persistent cache |
| VRAM usage | ~4.8 GB | ~4.0 GB |

## Dependencies

- Snagnar's llama.cpp fork
- CUDA toolkit (already on Paperspace)
- Mistral 7B GGUF model file

## Status

Phase 52 groundwork was established during Session 020. Snagnar's profile analysis confirmed llama.cpp availability. Implementation pending.

## Next Steps

- Clone and benchmark Snagnar's llama.cpp fork on Paperspace
- Compare inference speed vs Ollama with identical prompts
- Test persistent prompt caching across notebook sessions
- Integrate into relationship generator and harvester as optional backend