> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos, 
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 031 — 2026-06-23 — The Mycelium Gets a New Home

related: [[Session-030]], [[Phase-63]], [[Phase-64]], [[Phase-65]], [[Phase-66]]

## What We Did

**Project Hieros was renamed to Project Hierion. The mycelium got a domain.**

Started with a rename. "Hieros" had baggage — a Michigan nonprofit, EU
research projects, antenna analysis software. Dug through Greek roots.
Landed on "Hierion" (ἱερόν) — a sacred place, a temple precinct. Clean.
No collisions. Project Hierion is now canon.

Built the foundation on the cloud compute instance:

- Created the `hierion` system user. Fort Knox isolation from the
  existing project — separate home, separate SSH keys, separate everything.
  Zero shared credentials. Zero crossover.
- Cloned the CADMIES repo to the new home directory.
- Synced all four nodes: local PNY, Paperspace, GitHub, and the new
  cloud instance. All on main, all up to date.
- Stood up a completely separate MongoDB instance. Different OS user,
  different port, different data directory, different config file,
  different systemd service. Authentication enforced before any data
  touched it. Bound to localhost only. The existing project's database
  never noticed a thing.
- Registered `project-hierion.duckdns.org` via DuckDNS. Free, community-run,
  privacy-focused. Wrote the auto-update script (cron every 5 minutes).
- Configured NGINX to serve the CADMIES public gateway and mycelium map
  at the new domain. Dashboard at `/`, map at `/mycelium-map`. Symlinked
  the web root to the docs directory so git pulls auto-update the site.
- Hit a permissions wall: `www-data` couldn't traverse the locked-down
  home directory. Added `www-data` to the `hierion` group, adjusted path
  permissions. Map loaded. Dashboard loaded.

**YAOH YAOH BIBBY WAOH.**

Designed the Doctor Mistral availability system. GPU compute instance
chained in 5.5-hour sessions with 2-3 minute resets. "The Doctor Is Out"
status system with countdown timer. Turns a technical constraint into a
transparent feature.

Designed Phase 66: Mycelium Map UX — progressive loading, D3 Canvas
renderer migration, renderer-agnostic data layer, viewport-aware
rendering. Cytoscape.js as backup, sigma.js as fallback, Three.js +
WebXR as the long-term 3D immersive vision. Critical design rule:
progressive loading logic must not marry the renderer.

Wrote the public Architecture Overview. Sanitized. No server specs,
no costs, no internal paths. Scientific abstraction throughout.

Established the documentation privacy boundary: public docs explain
the system without exposing the implementation. Internal docs (SOPs,
configs, costs) stay private.

**GitHub Reorganization:**
- Created `Project-Hierion` organization
- Transferred CADMIES repo from personal account to the org
- Personal account renamed to `Hierion-Gardener`
- GitHub Pages unpublished (old URL broken, DuckDNS is the live site)
- Local and droplet remotes updated to new org URL
- Paperspace remote pending (machine busy)

## What Worked

- DuckDNS setup was smooth once the reCaptcha stopped fighting us
- MongoDB isolation — two instances running side by side, zero conflict
- NGINX server block alongside the existing project — no disruption
- Git sync across four nodes in one pass
- The map loaded on the first real URL the project has ever had
- Permissions debugging was methodical — `namei -l` showed the exact
  point of failure
- GitHub org creation and repo transfer completed cleanly
- Rename-trick bypassed the "retired repository name" error

## What Broke

- DuckDNS reCaptcha looped on first attempt. Incognito window fixed it.
- MongoDB user creation failed silently with `--eval` — shell quoting
  issues with special characters in the password. Interactive mongosh
  worked fine. Note: avoid `+` and `/` in MongoDB passwords going forward.
- `www-data` couldn't traverse `/home/Project/` — the Fort Knox isolation
  we built intentionally blocked NGINX. Fixed with group membership
  and adjusted path permissions.
- Web console reloaded mid-command and lost the symlink command.
- GitHub repo transfer failed first attempt — "retired repository name"
  error. Renamed repo to `CADMIES-temp`, transferred, renamed back.

## Decisions Made

- Project name: Hierion (ἱερόν — sacred place). Clean, no collisions.
- Cloud instance directory: `/home/Project/Hierion/`
- DuckDNS as the free dynamic DNS provider. EU.org application pending
  for `hierion.eu.org` as a longer-term academic domain.
- MongoDB on separate OS user (`mongodb-hierion`), not just separate
  database. Complete process isolation.
- No passwords in systemd unit files. Use `--shutdown` flag instead.
- Documentation sanitization: public-facing docs use scientific
  abstraction. No IPs, ports, costs, internal paths.
- GitHub organization `Project-Hierion` owns the repo. Personal account
  `Hierion-Gardener` is org admin only.
- The gardener is "a philosopher with a GPU habit." Canon.
- Public domain: `project-hierion.duckdns.org`

## Nuggets Collected

- "The mycelium has a front door."
- "A philosopher with a GPU habit."
- "Lock the doors, then sleep fine."
- "The hyphen is a handshake."
- "Swap the windshield, not the engine."
- "Diminishing ignorance. Always."
- "Project Hierion. Sacred place. Temple of knowledge."

## Soundtrack

No music this session — pure engineering flow state. Terminal work.
The sound of SSH keys generating. MongoDB forking. NGINX reloading.
The quiet hum of a server rack getting a new purpose.
And crickets. South Texas crickets.

## Next Actions

- SSL certificate (Certbot) for project-hierion.duckdns.org
- Build the GPU compute bridge (Paperspace API controller)
- Phase 66: D3 Canvas map migration with progressive loading
- Apply for hierion.eu.org
- Update Paperspace git remote
- Set up auto-sync cron on droplet for git pulls
- Continue Boxing training (evaluation ongoing)

## The Mycelium Status

636 concepts. 1,131 edges. 15 canonical domains.
Three nodes synced (local, GitHub, droplet). One pending (Paperspace).
One domain pointing at the cloud. One MongoDB waiting for data.
One map loading for the public. One philosopher with a GPU habit.