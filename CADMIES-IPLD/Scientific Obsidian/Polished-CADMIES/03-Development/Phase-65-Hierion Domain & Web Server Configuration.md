---
phase: 65
date: 2026-06-23
status: Complete
related: [[Phase-63]], [[Phase-64]], [[Session-031]]
---

# Phase 65: Hierion Domain & Web Server Configuration

## What Changed

A public domain was registered and a web server configured to serve the
CADMIES dashboard, mycelium map, and concept data. The Doctor Mistral
availability system was designed.

## Why

The public gateway on GitHub Pages served concept cards but lacked a
dedicated domain, interactive map hosting, and the foundation for
backend services. A proper web server enables URL routing, future API
endpoints, and SSL encryption.

## Changes Made

- Registered a public domain via a free, community-run, privacy-focused
  dynamic DNS provider. The provider was chosen for their commitment to
  privacy and community over profit.
- Configured automatic IP update to handle cloud instance IP changes.
- Created a dedicated web server configuration file with routes for
  the dashboard (`/`), mycelium map (`/mycelium-map`), and concept
  data (`/concepts.json`).
- Symlinked the web root to the repository docs directory — site updates
  automatically when the repository is updated.
- Added basic security headers.

## Doctor Mistral Availability System (Designed)

The GPU compute instance that runs the AI models has a session limit.
To provide near-continuous availability, sessions will be chained:
- Active session: 5.5 hours
- Reset window: 2-3 minutes
- New session begins immediately
- Target uptime: 99.1% during operating hours

A status indicator will display on all CADMIES pages showing whether
the Doctor is currently available. The reset window will include a
countdown timer. This turns a technical constraint into a transparent,
user-friendly feature.

## Testing

| Test | Result |
|---|---|
| Domain resolves to cloud instance | ✅ |
| Dashboard loads | ✅ |
| Mycelium map loads and is interactive | ✅ |
| Concept data accessible | ✅ |
| Automatic IP update running | ✅ |
| Existing project web config unaffected | ✅ |

## Conclusion

Phase 65 is complete. CADMIES is accessible at a public domain with a
functioning web server. The Doctor Mistral availability pattern is
designed and ready for implementation when the GPU compute bridge is built.

## Next Steps

- Obtain SSL certificate for HTTPS
- Build the GPU compute bridge
- Implement the Doctor Mistral status indicator on all pages

## Updates

### 2026-06-23 — Domain Live

The domain `project-hierion.duckdns.org` is live and serving the CADMIES
dashboard and mycelium map. The domain provider (DuckDNS) was selected
for their commitment to privacy, community operation, and free access —
values that align with the CADMIES project. An automatic IP update script
runs every five minutes to maintain connectivity.

The Doctor Mistral availability system was designed: chained GPU sessions
(5.5 hours active, 2-3 minute reset) with a site-wide status indicator
and countdown timer during resets. This turns a technical constraint into
a transparent, user-friendly feature.