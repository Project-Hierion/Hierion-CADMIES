---
phase: 73
date: 2026-07-30
status: Planned
related: [[Phase-72A-LLMDataHub-Fork-Reorganization]], [[growth_roadmap]]
---

# Phase-73B: Matadisco Integration Blueprint

## What Changed

*[Placeholder — content to be added]*

## Why

*[Placeholder — content to be added]*

Overview

Publish LLMDataHub datasets and CADMIES concept metadata to the Matadisco decentralized data discovery network on ATProto. Two workstreams: one for existing datasets (curated, licensed, attributed), one for our own concept metadata.

Workstream A: LLMDataHub → Matadisco

Step	What	Details

- A1	License audit	Parse DATASETS.md, check each dataset for explicit license. Build allowlist. Skip anything ambiguous.
- A2	Attribution mapping	Per allowed dataset: author, source repo, license type, link to license file
- A3	Outreach	Contact Matadisco/IPFS Foundation folks — green light to publish LLM dataset metadata
- A4	Record generation script	Transform allowlist → Matadisco records (resource URI, publishedAt, tags with license + domain info, optional preview)
- A5	Publishing pipeline	GitHub Actions workflow, scheduled or manual trigger, push records to ATProto PDS/relay
- A6	Validation	Spot-check live records, verify attribution, confirm they appear in matadisco-viewer

Workstream B: CADMIES Concepts → Matadisco

Step	What	Details

- B1	Concept metadata mapping	Each concept → Matadisco record. Resource = public gateway URL. Tags = domain(s), difficulty, related concepts
- B2	Record generation	Extend producer script to handle concept JSON
- B3	Publishing	Same GitHub Actions pipeline, separate record batch
- B4	Validation	Confirm CADMIES concepts discoverable on the network

Infrastructure

Component	Plan

- Publishing method	GitHub Actions (free, scheduled/manual) — model after gdi-de-csw-to-atproto
- PDS target	Use existing ATProto relay or free PDS; avoid droplet contamination
- Fallback	Fly.io free tier or similar if GitHub Actions doesn't work out
- Constraints & Principles
- License-first. No license = no publish. Document everything.

Attribution always. Credit authors, link sources, cite licenses.

Privacy-respecting infrastructure. No data harvesting, no tracking, no personal info in records.

Validate before committing. Run the vault validator. Keep the badge green.

Deliverables

scripts/matadisco_producer.py — generates Matadisco records from dataset index and concept JSON

.github/workflows/matadisco_publish.yml — scheduled publishing pipeline

CADMIES_Notes/Phase-73-Matadisco-Integration.md — polished phase note

Live Matadisco records, confirmed visible in matadisco-viewer
