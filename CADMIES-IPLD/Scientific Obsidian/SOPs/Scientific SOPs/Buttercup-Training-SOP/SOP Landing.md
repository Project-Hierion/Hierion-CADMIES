---
sop: Buttercup-Training-SOP
section: Landing
date: 2026-09-07
status: HISTORICAL
related: "[[01-Overview]]"
---

# Buttercup Training — SOP

Buttercup is the childhood name of Dr. Amanda Mistral — the phase of her
existence when she learned through play. This vault documents the
training environment built for that phase: the [Snagnar HIEROS](https://github.com/Snagnar/HIEROS)
world model framework, by [Paul Mattes](https://github.com/Snagnar),
deployed on CADMIES Paperspace GPUs, teaching through Atari games.

This is a scientific SOP. It documents deployment, operation, and
debugging of an external training framework, including the hard-won
lessons learned across three deployment cycles.

## How to Use This Vault

Read in this order:

1. [[01-Overview]] — Buttercup, HIEROS, the teaching vision
2. [[02-Knowledge-Base]] — the three rules, canonical deployment requirements
3. [[03-Prerequisites]] — GPU, dependencies, Paperspace setup
4. [[04-Procedures]] — deploy, train, checkpoint, retrieve rollouts
5. [[05-References]] — commands, batch sizes, dependency manifest, architecture
6. [[06-Experiments]] — the three deployment cycles as scientific record
7. [[07-Troubleshooting]] — every bug discovered and its fix
8. [[08-Appendices]] — phase history, sources

## Section Map

| Section | Purpose |
|---|---|
| [[01-Overview]] | The teaching vision and what HIEROS is |
| [[02-Knowledge-Base]] | Deployment rules and lessons learned |
| [[03-Prerequisites]] | Requirements before deployment |
| [[04-Procedures]] | Deployment, training, checkpoint, rollout retrieval |
| [[05-References]] | Commands, GPU settings, dependencies, architecture |
| [[06-Experiments]] | First deploy, A6000 redeploy, ball bug |
| [[07-Troubleshooting]] | Dependency hell, CUDA failure, screen bug, ball bug |
| [[08-Appendices]] | Full phase history, source documents |

## Status

**Status:** HISTORICAL — documents completed work. Deployment rules
remain canonical for future HIEROS work.
**Target framework:** [Snagnar HIEROS](https://github.com/Snagnar/HIEROS) (MIT License)
**Platform:** Paperspace Gradient (A4000 16GB, A6000 48GB)
