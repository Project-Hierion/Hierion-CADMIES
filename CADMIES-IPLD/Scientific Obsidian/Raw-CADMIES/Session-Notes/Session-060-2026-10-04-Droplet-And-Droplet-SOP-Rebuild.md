> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
  unfiltered thoughts, and coded messages for fellow gardeners.
  For polished documentation, check Polished CADMIES or promote this note.

# Session 060 — 2026-10-04 — Droplet And Droplet SOP Rebuild

## What We Did

### Context
The droplet was lost as of August due to billing failure. The droplet was rebuilt from scratch
on October 2 - 3. Project Hierion site went live again 2026-10-03. We rebuilt fast and dirty to
get back online, and the previous Operations SOP was left describing a droplet
that no longer existed — old user, old paths, old domain, MongoDB that
isn't installed anymore.

Today was the reconciliation. The SOP is a rebuild document, not just
an ops manual — if we lose the droplet again, the SOP alone should
rebuild it. The previous SOP was re-written as we rebuilt the droplet.

### The Core Problem
The vault was split between two realities:

- Reality A (pre-loss): `hierion` user, `/home/Project/Hierion/`,
  DuckDNS as primary domain, MongoDB running on 27018, "existing
  project" on 27017.
- Reality B (post-rebuild): `cadmies` user, `/home/Project/project-hierion/`,
  project-hierion.org via Cloudflare + Let's Encrypt.

### Approach
Simple truth pass, page by page. No restructuring, no new architecture.
Every note reconciled to the droplet that actually exists. Pending
things (MongoDB, git cron) get a banner instead of a rewrite —
described as intended setup, flagged as not-installed.

### The Deltas Applied

| Thing | Old (stale) | New (current) |
|---|---|---|
| OS user | `hierion` | `cadmies` |
| Home | /home/Project/Hierion/ | /home/Project/project-hierion/ |
| Domain | project-hierion.duckdns.org | project-hierion.org |
| DNS | DuckDNS | Cloudflare |
| SSL | not started | Let's Encrypt, expires 2027-01-01 |
| Repo remote | Hieros-CADMIES/CADMIES.git | Project-Hierion/Hierion-CADMIES.git |
| Group | `hierion` | `cadmies` |
| MongoDB | running | pending reinstall |

### DuckDNS — Dormant
DuckDNS is dormant now. `project-hierion.duckdns.org` currently points at a
foreign server not related to our Project Hierion, subdomain may have been recycled. We banner'd the
DuckDNS pages as DORMANT with an explicit note: if reactivated, update
the SOP accordingly. Future plan — maybe revive as a parallel/fallback
live site if the main site goes down. Not today.

### Ground Truth Checks (DO web console)
Ran these live to stop guessing:

- `readlink -f /var/www/project-hierion` →
  `/home/Project/project-hierion/CADMIES/docs` ✅
- `/home/Project/` → `root:cadmies` 750 ✅
- `/home/Project/project-hierion/` → `cadmies:cadmies` 750 ✅
- `.ssh/` → `cadmies:cadmies` 700 ✅
- `CADMIES/` → `cadmies:cadmies` **775** (I had guessed 755 — corrected)
- No `duckdns/` directory present → removed from the tree

## What Worked

- Ground-truth commands in the DO console killed the guesswork. Should
  have done it from the first question, not the fourth.
- The banner approach for pending/dormant things — one line, no rewrite.
- Treating the SOP as a rebuild document, not just an ops manual. That
  reframe made every decision easier.
- The "skip and return later" rule. Kept momentum instead of dying in
  the weeds.

## What Broke

- I (DeepSeek) over-engineered early. Pitched dual-SOP architecture, frontmatter
  labels, physical vault splits. The Gardener course-corrected — just
  update the pages. All that structural ambition was noise.
- Lost the Gardener once on the 04-03 permission-table detail. Should've
  just handed over the corrected full file instead of walking it line
  by line. Lesson: when the detail is dense, ship the artifact, not the
  explanation.

## Decisions Made

- The SOP stays one SOP. No split into Operations vs Build/Provisioning.
  Rebuild content gets folded in later or becomes its own thing down the
  road. Not today's problem.
- Vault structure stays as-is. No frontmatter `ops:`/`build:` labels.
- Truth pass first, structure pass later (if ever). Fix facts, don't
  reshuffle.
- DuckDNS = dormant, bannered, with reactivation note.
- MongoDB = pending. Banner on all Mongo pages, keep intended setup
  documented so a rebuild reproduces it.

## Nuggets Collected

- "The SOP is a rebuild document, not just an ops manual."
- "Pending things get a banner, not a rewrite."
- "Ship the artifact, not the explanation."
- "One SOP, done today, rebuild content folded in later."

## Session Wrap-Up

### SOP Status
- Landing + Overview: already correct (done 10-03) ✅
- 02 Prerequisites: reconciled, DuckDNS dormant-flagged ✅
- 03-01 → 03-05: reconciled ✅
- 04-01 → 04-05: reconciled ✅
- 05-01 → 05-04: reconciled ✅
- 06-01 → 06-03: reconciled, rebuild captured in history ✅

### Droplet Status
- `cadmies` user, repo cloned, Nginx serving
- SSL live, DNS via Cloudflare
- MongoDB pending, git cron pending
- DuckDNS dormant
