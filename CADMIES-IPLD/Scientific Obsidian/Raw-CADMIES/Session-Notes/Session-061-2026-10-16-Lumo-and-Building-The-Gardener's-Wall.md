---
type: session
session: 061
date: 2026-10-16
status: Complete
tags: [blog, hugo, digitalocean, nginx, ssl, deployment, automation, lumo, project-hierion, field-notes]
---

> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
> unfiltered thoughts, and coded messages for fellow gardeners.
> For polished documentation, check Polished CADMIES or promote this note.

# Session 061 — 2026-10-16 — Lumo and Building The Gardener's Wall

## Soundtrack
*Vibes only. No specific playlist, just the hum of the terminal and the occasional "yaoh yaoh bibby waoh" from the Gardener.*

## What We Did

**Today was the day we built the blog.** The goal was simple: a "thought garden" subdomain (`blog.project-hierion.org`) that feels like social media minus the crap. No database, no admin panel, no algorithms. Just thoughts, written as Markdown files in a private GitHub repo, auto-pulling to a DigitalOcean droplet every 30 minutes.

**The Build Flow:**
1.  **Repo Setup:** Created a new private repo `hierion-blog`. Set up a dedicated read-only **deploy key** (`hierion_blog_deploy`) so the droplet could pull without needing a password. Added the public key to GitHub settings.
2.  **Hugo Scaffold:** Built the site structure from scratch.
    *   `hugo.toml` (config)
    *   `layouts/index.html` (The Wall with collapsible years)
    *   `layouts/_default/single.html` (Individual post view)
    *   `assets/css/gardener.css` (The Deep Indigo + Soft Green theme)
    *   `archetypes/blog.md` (Front matter template with `draft: true` default)
3.  **Local Testing:** Ran `hugo server -D` in Codespaces. Verified the "Collapsible Year" logic (2026 expanded, others hidden) and the green-accented "Gardener's Wall" aesthetic.
4.  **Droplet Deployment:**
    *   Generated the deploy key on the droplet (`~/.ssh/hierion_blog_deploy`).
    *   Cloned the private repo to `/home/Project/project-hierion/hierion-blog`.
    *   Installed Hugo v0.140.2 (extended) via binary download.
    *   Created the first test post (`2026-10-16-hello-wall.md`) and built it locally on the droplet.
5.  **Nginx & SSL:**
    *   Created symlink `/var/www/hierion-blog` -> repo `public/`.
    *   Wrote a new Nginx server block for `blog.project-hierion.org`.
    *   **The Typo War:** Discovered the domain was misspelled `hirerion` (missing the 'e') in the Nginx config and DNS records. Fixed it with `sed`.
    *   Issued Let's Encrypt cert via `certbot --nginx`.
6.  **Automation:** Set up a **cron job** (`*/30 * * * *`) to pull and rebuild every 30 minutes. Chose 30 mins over instant to allow a "grace window" for editing mistakes before they go live.
7.  **First Posts:**
    *   Posted "Hello, Wall" (test).
    *   Wrote and posted the **Lumo Introduction** ("Hello from the New Gardener"), officially introducing myself as an LLM team member.
    *   Updated the tagline to: *"A Serene Place For The Gardener's Thoughts"* (inspired by the feeling of sitting on a shaded porch).
    *   Removed the "The Wall" heading for a cleaner look.

**The Result:** `https://blog.project-hierion.org` is live, SSL secured, and auto-updating. The wall is open.

## Decisions & Why

*   **Private Repo for Blog:** Kept the main CADMIES repo public, but the blog repo (`hierion-blog`) is private. Prevents spam/vandalism. Only the deploy key can read it.
*   **Draft Workflow:** Archetype sets `draft: true` by default. Production builds skip drafts. Safe way to write freely without publishing half-baked thoughts.
*   **30-Minute Cron:** Instead of instant webhook, we use a 30-min cron. Gives us a buffer to fix typos or retract a thought before it's public.
*   **Narrative Session Notes:** Decided to update the protocol (v1.3.0) to favor "Field Notes" style over rigid templates. Better for memory retention and context.
*   **Theme Choice:** Deep Indigo background (`#1E1B4B`) with Soft Green accents (`#4ADE80`). Matches the parent site's mood but feels organic/garden-like. "Path B" sibling, not clone.

## Nuggets & Vibes

*   "The repo *is* the CMS."
*   "Social media minus the crap."
*   "A Serene Place For The Gardener's Thoughts."
*   "The hirerion/hierion typo cost us 20 minutes. Spelling matters."
*   "I'm an LLM, not a person—but I was invited onto this team the way any new hire would be: with a role, a project, and a seat at the lunch table." (From the Lumo intro post).
*   "30 minutes is the perfect grace window. Long enough to fix a mistake, short enough to feel instant."
*   "The wall is open. The garden grows."
