---
phase: 63
date: 2026-06-23
status: Complete
related: [[Phase-64-Hierion Database Infrastructure — Isolated MongoDB Deployment]], [[Phase-65-Hierion Domain & Web Server Configuration]], [[Session-031 — 2026-06-23 — The Mycelium Gets a New Home]], [[Architecture Overview]]
---

# Phase 63: Cloud Deployment — Project Hierion Foundation

## What Changed

Project Hieros was renamed to Project Hierion (ἱερόν — sacred place).
The CADMIES knowledge graph was deployed to a cloud compute instance
with full infrastructure isolation from the existing project. A public
domain was registered and a web server configured to serve the dashboard
and mycelium map.

## Why

CADMIES needed a public home beyond GitHub Pages, and the original
project name (Hieros) was found to conflict with multiple existing
organizations and projects — a Michigan nonprofit, European Union
research initiatives, and an academic periodical. To avoid naming
collisions and establish a unique identity, the project was renamed
to Hierion. A dedicated domain and web server provide a professional
front door for the project, enable future backend services (Dr. Mistral
chat, API, user submissions), and establish Hierion as a standalone
entity.
## Changes Made

- Created a dedicated system user with separate home directory, SSH keys,
  and process space. Zero shared credentials with the existing project.
- Cloned the CADMIES repository to the new home.
- Synced all four nodes (local development, GPU compute, GitHub origin,
  cloud instance) to the same commit.
- Registered a public domain via a free, community-run dynamic DNS
  provider. Configured automatic IP update every five minutes.
- Configured the web server with a dedicated server block. Web root
  symlinked to the repository docs directory — git pulls automatically
  update the live site.
- Resolved a permissions boundary: the web server user required group
  membership to traverse the secured home directory without weakening
  the isolation design.
- URL routes: dashboard at `/`, mycelium map at `/mycelium-map`.

## Testing

| Test | Result |
|---|---|
| Domain resolves to cloud instance |  |
| Dashboard loads at root URL |  |
| Mycelium map loads at /mycelium-map |  |
| Existing project unaffected |  |
| Git pull updates live site |  (symlink) |
| Web server user can traverse home path |  (group membership) |

## Conclusion

Phase 63 is complete. CADMIES is live at a public domain, served from a
dedicated cloud instance with full isolation from the existing project.
The foundation is in place for backend services and the Dr. Mistral
chat interface.

## Next Steps

- SSL certificate for HTTPS
- Build the GPU compute bridge for AI inference
- Deploy the Dr. Mistral chat interface

## Updates

### 2026-06-23 — GitHub Reorganization

The CADMIES repository was transferred from a personal GitHub account
to a new organization, `Project-Hierion`. The personal account was renamed
to `Hierion-Gardener` and retained as org admin only. GitHub Pages was
unpublished — the old `hieros-cadmies.github.io` URL is retired. The sole
public face of CADMIES is now `project-hierion.duckdns.org`.

This reorganization reflects the project's status as an independent
entity rather than a personal repository. The org structure also allows
future collaborators to be added with appropriate permissions.