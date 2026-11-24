#!/usr/bin/env python3
"""
File: update_roadmap.py
Tool: CADMIES Roadmap Update Pipeline
Version: 1.0.0
System: CADMIES / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Keeps growth_roadmap.md synchronized with the vault.
         - Regenerates the RECENT SESSIONS rolling block from actual
           session notes on disk (--apply to write).
         - Staleness is judged by SESSION STEM SET, so a hand-polished
           block containing the right sessions is considered current.
         - Reports (never auto-edits): COMPLETED, NEXT UP, PARKING LOT,
           roadmap art (weekly manual ritual).

Usage:
    python repo-maintenance-automation/update_roadmap.py           # report
    python repo-maintenance-automation/update_roadmap.py --apply   # sync block

Version History:
  v1.0.0 (2026-11-24): Initial release. Stem-set comparison, humanized
                       titles, date-span display, Zulu stamps.
"""

import re
import sys
import yaml
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "config.yaml"

SESSION_RE = re.compile(r"^Session-(\d{3})[A-Z]?-(.+)$")
SPAN_RE = re.compile(r"(\d{4}-\d{2}-\d{2}(?:-to-\d{4}-\d{2}-\d{2})?)")
LINK_RE = re.compile(r"\[\[(Session-[^\]]+)\]\]")
STOPWORDS = {"and", "the", "of", "a", "to", "in", "on", "for", "or", "vs"}


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def get_vault_root(config):
    vault_rel = config.get("vault_root", "../CADMIES-IPLD/Scientific Obsidian")
    return (SCRIPT_DIR / vault_rel).resolve()


def humanize_title(raw):
    """Session-XXX-date-The-Hyphen-Title -> 'The Hyphen Title' in title case,
    preserving tokens that look like acronyms/versions (LLMDataHub, 068, v1.2)."""
    tokens = [t for t in raw.split("-") if t]
    out = []
    for i, tok in enumerate(tokens):
        # keep tokens with internal capitals or digits verbatim
        if any(c.isdigit() for c in tok) or (tok[1:].lower() != tok[1:] if len(tok) > 1 else False):
            out.append(tok)
            continue
        low = tok.lower()
        if i > 0 and low in STOPWORDS:
            out.append(low)
        else:
            out.append(tok[0].upper() + tok[1:])
    return " ".join(out)


def parse_session_notes(vault_root):
    sdir = vault_root / "Raw-CADMIES" / "Session-Notes"
    sessions = []
    for f in sorted(sdir.glob("Session-*.md")):
        m = SESSION_RE.match(f.stem)
        if not m:
            continue
        rest = m.group(2)
        sm = SPAN_RE.search(rest)
        date_part = sm.group(1) if sm else rest[:10]
        title = humanize_title(SPAN_RE.sub("", rest).strip("-–— "))
        sessions.append({"num": int(m.group(1)), "stem": f.stem,
                         "date": date_part, "title": title})
    sessions.sort(key=lambda s: s["num"])
    return sessions


def pretty_date(span):
    m = re.match(r"(\d{4}-\d{2})-(\d{2})(?:-to-(?:\d{4}-\d{2})?-(\d{2}))?", span)
    if m and m.group(3):
        return f"{m.group(1)}-{m.group(2)} → {m.group(3)}"
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    return span


def build_sessions_block(sessions, keep=3):
    lines = []
    for s in sessions[-keep:]:
        lines.append(f"- **Session-{s['num']:03d}** ({pretty_date(s['date'])}) — "
                     f"{s['title']}. See [[{s['stem']}]]")
    return "\n".join(lines)


def extract_current_block(roadmap_text):
    m = re.search(r"(## 📜 RECENT SESSIONS[^\n]*\n\n)(.*?)(\n\n---)", roadmap_text, re.DOTALL)
    if not m:
        return None, None
    return m.group(2), m


def main(apply_mode=False):
    config = load_config()
    vault_root = get_vault_root(config)
    roadmap_path = vault_root / "growth_roadmap.md"
    roadmap = roadmap_path.read_text()
    sessions = parse_session_notes(vault_root)

    print(f"\n{'='*60}")
    print(f"  🌱 CADMIES ROADMAP UPDATE PIPELINE — {'APPLY' if apply_mode else 'REPORT'} MODE")
    print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')}")
    print(f"  Sessions found: {len(sessions)} (latest: Session-{sessions[-1]['num']:03d})")
    print(f"{'='*60}\n")

    issues = 0
    current_block, m = extract_current_block(roadmap)
    if current_block is None:
        print("  ❌ Could not locate RECENT SESSIONS block — manual attention needed.")
        return 1

    desired_block = build_sessions_block(sessions)
    current_stems = LINK_RE.findall(current_block)
    desired_stems = [s["stem"] for s in sessions[-3:]]

    if set(current_stems) == set(desired_stems):
        print("  ✅ Recent sessions block is current (stem set matches).")
    else:
        issues += 1
        print("  ⚠️  Recent sessions block is STALE. Desired:")
        for line in desired_block.splitlines():
            print(f"     {line}")
        if apply_mode:
            roadmap = roadmap[:m.start(2)] + desired_block + roadmap[m.end(2):]
            roadmap_path.write_text(roadmap)
            print("  ✏️  Sessions block rewritten (art and other sections untouched).")
            issues -= 1

    phases_dir = vault_root / "Polished-CADMIES" / "03-Development"
    phase_re = re.compile(r"^Phase-(\d+[A-Z]?)-", re.IGNORECASE)
    phase_names = sorted({phase_re.match(f.stem).group(1)
                          for f in phases_dir.glob("Phase-*.md")
                          if phase_re.match(f.stem)})

    print("\n── Manual-judgment sections (reported, never auto-edited) ──")
    print(f"  ℹ️  Phase notes on disk: {len(phase_names)} (latest: {', '.join(phase_names[-4:])})")
    print("  ℹ️  COMPLETED / NEXT UP / PARKING LOT: verify they reflect the above.")
    print("  ℹ️  Roadmap art: regenerate weekly at most (manual ritual).")

    print(f"\n{'='*60}")
    if issues == 0:
        print("  ✅ Roadmap is current.")
    else:
        print("  ⚠️  Roadmap is stale — run with --apply to sync the sessions block.")
    print(f"{'='*60}\n")
    return 0 if issues == 0 else 1


if __name__ == "__main__":
    exit(main(apply_mode="--apply" in sys.argv))
