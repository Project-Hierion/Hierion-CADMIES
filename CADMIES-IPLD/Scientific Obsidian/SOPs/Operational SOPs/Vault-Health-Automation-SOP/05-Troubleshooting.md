---
type: sop
system: Vault Health Automation
version: 1.0.0
date: 2026-11-24
status: Active
related: "[[SOP Landing]], [[03-Procedures]], [[02-Overview]]"
---

# 05-Troubleshooting

Back to: [[SOP Landing]]

## 05-01 Push-triggered false alarms (fixed 2026-11-24)

**Symptom:** every commit fired the action mid-session; transient states failed the run.
**Cause:** push/PR triggers on the workflow.
**Fix:** schedule-only triggers (05:00Z/17:00Z) + manual dispatch. Lessons: reactive triggers catch work in flight; scheduled checks see the vault at rest.

## 05-02 Dead link to a deleted file

**Symptom:** `DEAD_LINK ... [[Decisions-Log]] (target not found)` on every run.
**Cause:** the target file was deleted; a referencing note was not updated. Root-source cause: the Note-Taking Protocol once encouraged red links as "future spores."
**Fix:** de-wikilink to plain text, and the Protocol now mandates linking only existing notes before commit. Rule of thumb: when deleting a note, grep the vault for `[[Its-Name]]` in the same session.

## 05-03 Validator crash on missing roadmap

**Symptom:** `ValueError: not enough values to unpack` if `growth_roadmap.md` is absent.
**Cause:** early-return path didn't match the function's tuple contract (pre-v1.4.0 latent bug).
**Fix:** v1.4.0 returns `(issues, {})` on the early path. Fixed before it ever bit production.

## 05-04 Orphans reported but summary stays green

**Not a bug.** Orphan detection is informational by design — islands in the vault are diagnosis, not failure. If an island should be connected, add a wikilink from a related note and re-run.
