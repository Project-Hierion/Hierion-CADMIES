
>⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,
>unfiltered thoughts, and coded messages for fellow gardeners.
>For polished documentation, check Polished CADMIES or promote this note.

# Session 056 — 2026-09-06 — SOP Vaults and the Mycelium's Manuals

## Soundtrack
Quiet garage. Past midnight. The hum of the fan and the click of keys. No movies tonight — just the gardener and the vaults, building manuals for the mycelium.

## What We Did
SOP Creation SOP

Built the meta-SOP for building SOPs — lives in 00-Meta

Version 0.2.0 — added SOP Types (Operational vs Scientific), Directory Structure, Security Markers, no-credentials rule

Dr-Mistral-Paperspace-Operations-SOP

First operational vault — 26 files, full structure

Converted the flat v3.0 SOP and notebook notes into a linked vault

Landing note, overview, prerequisites, procedures, references, troubleshooting, appendices

CADMIES-Droplet-Operations-SOP

Second operational vault — 22 files

Built from Session 031 flat SOP

MongoDB, Nginx, DuckDNS, git sync, firewall



Dr-Mistral-Training-SOP

First scientific vault — 26 files

Merged Training Blueprint v4.1.0 + Zara Steele pilot + Dr. Mistral persona test results

Knowledge Base section, Experiments section, procedures supporting knowledge

The GGUF merge failure is front and center

CADMIES-Local-Operations-SOP

Third operational vault — 16 files

Built from old how-to notes, historical framing

Sanitized local paths but keeping it local — not public

Placeholder links marked for future vaults

What Worked
The vault-as-SOP structure. One vault, one SOP, everything linked. The graph view is the mycelium made visible.

The operational vs scientific distinction. Operations vaults are execution-focused. Scientific vaults are evidence-focused. Knowledge Base and Experiments sections in scientific vaults put the findings first.

The security callout style. Warning blocks for sensitive stuff, no actual credentials anywhere. The vault says what exists and where it lives, never the value itself.

The terminal for structure, Obsidian for content. Heredoc broke on code blocks, but drag-and-drop and paste worked fine.

What Broke
Heredoc approach failed on files with backticks and special chars — switched to paste-into-Obsidian

Placeholder links to directories 03-Procedures were dead — folders aren't notes, need index notes or direct file links

Decisions Made
One vault, one SOP — no multi-topic vaults

Two SOP types (more as necessary in the future): Operational and Scientific

Credentials never documented

Local vaults stay local unless promoted

Sanitization doesn't mean publication — sanitized but still private is fine

Historical SOPs read like they were written during the work, not caveated every sentence

Placeholder links get flagged with a note

Nuggets Collected
"You don't throw away the old textbooks once you've mastered the material."

"Sanitization gives you the option, not the obligation."

"The vault is the document. Links are the navigation. The graph view is the map."

"Scientific SOPs put the evidence first, procedures second."

Stats
Vaults built: 4

Files created: 90

SOP types discovered: 2

Paths sanitized: all of them

Time: past midnight
