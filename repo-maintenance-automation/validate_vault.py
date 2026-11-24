#!/usr/bin/env python3
"""
File: validate_vault.py
Tool: CADMIES Vault Validator
Version: 1.4.0
System: CADMIES / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Scans the Scientific Obsidian vault and reports on frontmatter
         consistency, dead wikilinks, duplicate files, and roadmap drift.
         --fix mode now handles: status fields, raw banners, AND dead wikilinks
         with fuzzy matching to find correct target filenames.

Usage:
    python repo-maintenance-automation/validate_vault.py
    python repo-maintenance-automation/validate_vault.py --fix
    python repo-maintenance-automation/validate_vault.py --fix --yes

Version History:
  v1.0.0 (2026-07-16): Initial read-only validator.
  v1.0.1 (2026-07-16): Fixed YAML parsing for [[wikilinks]] in frontmatter.
                       Fixed duplicate detector self-comparison.
  v1.0.2 (2026-07-16): Skip .ipynb_checkpoints and hidden directories.
  v1.1.0 (2026-07-16): --fix mode with before/after previews, interactive confirmations.
  v1.2.0 (2026-07-16): --fix mode now handles dead wikilinks via fuzzy filename matching.
  v1.2.1 (2026-07-16): Added check for markdown files missing .md extension.
  v1.3.0 (2026-07-16): --fix mode now handles roadmap drift automatically.
  v1.3.1 (2026-09-06): Honor config skip_folders list — directories excluded from all checks.
  v1.4.0 (2026-11-24): Orphan-note detection (informational, zero inbound wikilinks);
                       trend snapshot appended to logs/vault_health_trends.csv on every
                       run (Zulu timestamps, per SOP 0.2); HTML dashboard written to
                       logs/vault_health_dashboard.html for human-readable reports.
"""

import os
import re
import sys
import yaml
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "config.yaml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def get_vault_root(config):
    vault_rel = config.get("vault_root", "../CADMIES-IPLD/Scientific Obsidian")
    return (SCRIPT_DIR / vault_rel).resolve()

def should_skip_path(filepath, config=None):
    parts = str(filepath).split("/")
    for part in parts:
        if part.startswith(".") or part == ".ipynb_checkpoints":
            return True
    # Honor config skip_folders if provided
    if config:
        skip_folders = config.get("skip_folders", [])
        for skip in skip_folders:
            if skip in str(filepath):
                return True
    return False

def find_files(vault_root, folder, pattern):
    target_dir = vault_root / folder
    if not target_dir.exists():
        return []
    return sorted(target_dir.glob(pattern))

def backup_file(filepath):
    backup_dir = SCRIPT_DIR / "logs" / "backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"{filepath.name}.{timestamp}.bak"
    shutil.copy2(filepath, backup_path)
    return backup_path

def parse_frontmatter(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    if not content.startswith("---"):
        return None, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content
    raw_yaml = parts[1]
    body = parts[2]
    lines = raw_yaml.split("\n")
    protected_lines = []
    for line in lines:
        if "[[" in line and ":" in line:
            key, _, value = line.partition(":")
            value = value.strip()
            if not (value.startswith('"') and value.endswith('"')):
                value = '"' + value + '"'
            protected_lines.append(f"{key}: {value}")
        else:
            protected_lines.append(line)
    protected_yaml = "\n".join(protected_lines)
    try:
        frontmatter = yaml.safe_load(protected_yaml)
        return frontmatter, body
    except yaml.YAMLError:
        return "PARSE_ERROR", body

def confirm_fix(description, before, after, auto_yes=False):
    if auto_yes:
        print(f"  📝 {description}")
        print(f"     BEFORE: {before}")
        print(f"     AFTER:  {after}")
        return True
    print(f"\n  ┌─ FIX PROPOSED ─────────────────────────────")
    print(f"  │ {description}")
    print(f"  │")
    print(f"  │ BEFORE: {before}")
    print(f"  │ AFTER:  {after}")
    print(f"  └───────────────────────────────────────────")
    while True:
        response = input("  Apply? [y]es / [n]o / [s]kip all: ").lower().strip()
        if response in ("y", "yes", ""):
            return True
        elif response in ("n", "no"):
            return False
        elif response in ("s", "skip"):
            return "skip_all"
        print("  Please answer y, n, or s")

def check_frontmatter(filepath, doc_type, config, fix_mode=False, auto_yes=False):
    issues = []
    fixes_applied = 0
    rules = config["doc_types"].get(doc_type, {})
    required = rules.get("required_frontmatter", [])
    if not required:
        return issues, fixes_applied
    fm, body = parse_frontmatter(filepath)
    if fm is None:
        issues.append(f"MISSING_FRONTMATTER: No YAML frontmatter found")
        return issues, fixes_applied
    if fm == "PARSE_ERROR":
        issues.append(f"PARSE_ERROR: YAML frontmatter is malformed")
        return issues, fixes_applied
    for field in required:
        if field not in fm or fm[field] is None:
            issues.append(f"MISSING_FIELD: '{field}' is required but missing")
    valid_statuses = rules.get("valid_statuses", [])
    if valid_statuses and "status" in fm and fix_mode:
        raw_status = str(fm["status"])
        matched = False
        for vs in valid_statuses:
            if vs.lower() in raw_status.lower():
                matched = True
                break
        if not matched:
            suggested = None
            if "🔴" in raw_status or "critical" in raw_status.lower() or "bug" in raw_status.lower():
                suggested = "In Progress"
            elif "✅" in raw_status or "complete" in raw_status.lower():
                suggested = "Complete"
            elif "📋" in raw_status or "planned" in raw_status.lower():
                suggested = "Planned"
            elif "🔄" in raw_status or "progress" in raw_status.lower():
                suggested = "In Progress"
            if suggested:
                desc = f"Fix status in {filepath.name}"
                before = f"status: {raw_status}"
                after = f"status: {suggested}"
                result = confirm_fix(desc, before, after, auto_yes)
                if result == "skip_all":
                    auto_yes = False
                elif result:
                    backup_file(filepath)
                    with open(filepath, "r") as f:
                        content = f.read()
                    new_content = content.replace(f"status: {raw_status}", f"status: {suggested}")
                    with open(filepath, "w") as f:
                        f.write(new_content)
                    fixes_applied += 1
                    print(f"     ✅ Fixed: status → '{suggested}'")
                    return [], fixes_applied
    return issues, fixes_applied

def check_sections(filepath, doc_type, config):
    issues = []
    rules = config["doc_types"].get(doc_type, {})
    required_sections = rules.get("required_sections", [])
    if not required_sections:
        return issues
    with open(filepath, "r") as f:
        content = f.read()
    for section in required_sections:
        pattern = rf"^#{{1,3}}\s+{re.escape(section)}"
        if not re.search(pattern, content, re.MULTILINE):
            issues.append(f"MISSING_SECTION: '{section}' section not found")
    return issues

def check_raw_banner(filepath, doc_type, config, fix_mode=False, auto_yes=False):
    issues = []
    fixes_applied = 0
    rules = config["doc_types"].get(doc_type, {})
    if not rules.get("required_banner", False):
        return issues, fixes_applied
    banner_marker = rules.get("banner_marker", "RAW NOTE")
    with open(filepath, "r") as f:
        content = f.read()
    if banner_marker not in content[:500]:
        if fix_mode:
            desc = f"Add raw note banner to {filepath.name}"
            before = "(no banner)"
            banner_text = "> ⚠️ RAW NOTE — Work in progress. May contain half-formed ideas, typos,\n> unfiltered thoughts, and coded messages for fellow gardeners.\n> For polished documentation, check Polished CADMIES or promote this note.\n\n"
            after = banner_text[:80] + "..."
            result = confirm_fix(desc, before, after, auto_yes)
            if result == "skip_all":
                auto_yes = False
            elif result:
                backup_file(filepath)
                if content.startswith("#"):
                    new_content = banner_text + content
                else:
                    new_content = banner_text + content
                with open(filepath, "w") as f:
                    f.write(new_content)
                fixes_applied += 1
                print(f"     ✅ Fixed: banner added")
                return [], fixes_applied
        else:
            issues.append(f"MISSING_BANNER: Raw note banner not found")
    return issues, fixes_applied

def build_note_index(vault_root, config):
    """Build a mapping of note titles -> full filenames for fuzzy matching."""
    note_index = {}
    scan_folders = config.get("cross_refs", {}).get("scan_folders", [])
    for folder in scan_folders:
        target_dir = vault_root / folder
        if target_dir.exists():
            for f in target_dir.rglob("*.md"):
                if should_skip_path(f, config):
                    continue
                note_index[f.stem] = str(f.relative_to(vault_root))
    for f in vault_root.glob("*.md"):
        if should_skip_path(f, config):
            continue
        note_index[f.stem] = f.name
    meta_dir = vault_root / "00-Meta"
    if meta_dir.exists():
        for f in meta_dir.rglob("*.md"):
            if should_skip_path(f, config):
                continue
            note_index[f.stem] = str(f.relative_to(vault_root))
    return note_index

def fuzzy_match_link(link_text, note_index):
    """Try to find the correct filename for a dead wikilink."""
    # Exact match
    if link_text in note_index:
        return note_index[link_text]
    
    # Check if any note starts with the link text
    matches = [title for title in note_index if title.startswith(link_text)]
    if len(matches) == 1:
        return note_index[matches[0]]
    
    # Check if link text is contained in any note title
    matches = [title for title in note_index if link_text.lower() in title.lower()]
    if len(matches) == 1:
        return note_index[matches[0]]
    
    return None

def check_and_fix_cross_references(vault_root, config, fix_mode=False, auto_yes=False):
    issues = []
    fixes_applied = 0
    scan_folders = config.get("cross_refs", {}).get("scan_folders", [])
    link_pattern = re.compile(r"\[\[([^\]]+)\]\]")
    
    note_index = build_note_index(vault_root, config)
    
    for folder in scan_folders:
        target_dir = vault_root / folder
        if not target_dir.exists():
            continue
        for filepath in target_dir.rglob("*.md"):
            if should_skip_path(filepath, config):
                continue
            with open(filepath, "r") as f:
                content = f.read()
            
            # Skip template/teaching files
            if "<!-- TEMPLATE:" in content[:200]:
                continue
            
            links = link_pattern.findall(content)
            modified = False
            new_content = content
            
            for link in links:
                clean_link = link.split("#")[0].split("|")[0].strip()
                
                # Skip intentional placeholder links
                if clean_link in ["note-one", "note-two", "linked-note", "double brackets", "Session-005"]:
                    continue
                
                # Skip non-note references (scripts, concepts)
                if clean_link.endswith(".py") or clean_link in ["bayes_theorem", "problem_solving_guide"]:
                    continue
                
                if clean_link not in note_index:
                    # Try fuzzy match
                    match = fuzzy_match_link(clean_link, note_index)
                    if match and fix_mode:
                        match_stem = Path(match).stem
                        desc = f"Fix dead link in {filepath.name}"
                        before = f"[[{link}]]"
                        after = f"[[{match_stem}]]"
                        result = confirm_fix(desc, before, after, auto_yes)
                        if result == "skip_all":
                            auto_yes = False
                            issues.append(f"DEAD_LINK: {filepath.relative_to(vault_root)} -> [[{link}]] (target not found)")
                        elif result:
                            new_content = new_content.replace(f"[[{link}]]", f"[[{match_stem}]]")
                            modified = True
                            fixes_applied += 1
                            print(f"     ✅ Fixed: [[{link}]] → [[{match_stem}]]")
                        else:
                            issues.append(f"DEAD_LINK: {filepath.relative_to(vault_root)} -> [[{link}]] (target not found)")
                    else:
                        rel_path = filepath.relative_to(vault_root)
                        issues.append(f"DEAD_LINK: {rel_path} -> [[{link}]] (target not found)")
            
            if modified:
                backup_file(filepath)
                with open(filepath, "w") as f:
                    f.write(new_content)
    
    return issues, fixes_applied

def check_duplicates(vault_root, config):
    issues = []
    scan_folders = config.get("cross_refs", {}).get("scan_folders", [])
    scan_folders = list(scan_folders)
    scan_folders.append("./")
    hashes = defaultdict(list)
    for folder in scan_folders:
        target_dir = vault_root / folder
        if not target_dir.exists():
            continue
        for filepath in target_dir.rglob("*.md"):
            if should_skip_path(filepath, config):
                continue
            with open(filepath, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            rel_path = str(filepath.relative_to(vault_root))
            hashes[file_hash].append(rel_path)
    for h, paths in hashes.items():
        unique_paths = list(set(paths))
        if len(unique_paths) > 1:
            issues.append(f"DUPLICATE: {len(unique_paths)} identical files: {', '.join(sorted(unique_paths))}")
    return issues

def check_roadmap_drift(vault_root, config, fix_mode=False, auto_yes=False):
    issues = []
    roadmap_path = vault_root / "growth_roadmap.md"
    if not roadmap_path.exists():
        issues.append("ROADMAP_NOT_FOUND: growth_roadmap.md missing from vault root")
        return issues, {}  # v1.4.0 fix: early-return path now matches the tuple contract
    phases_dir = vault_root / "Polished-CADMIES/03-Development/"
    phase_statuses = {}
    if phases_dir.exists():
        for f in phases_dir.glob("Phase-*.md"):
            if should_skip_path(f, config):
                continue
            fm, _ = parse_frontmatter(f)
            if fm and fm != "PARSE_ERROR" and "phase" in fm and "status" in fm:
                phase_num = str(fm["phase"]).strip()
                phase_statuses[phase_num] = str(fm["status"]).strip()
    with open(roadmap_path, "r") as f:
        roadmap_content = f.read()
    for phase_num, note_status in phase_statuses.items():
        pattern = rf"Phase {re.escape(phase_num)}.*?(✅|📋|🔄|💡|🔴)"
        match = re.search(pattern, roadmap_content)
        if match:
            roadmap_status_symbol = match.group(1)
            symbol_map = {
                "✅": ["complete", "active"],
                "📋": ["planned", "designed", "pending"],
                "🔄": ["in progress", "active"],
                "💡": ["designed", "planned", "idea"],
                "🔴": ["abandoned", "blocked", "critical"],
            }
            expected = symbol_map.get(roadmap_status_symbol, [])
            note_status_lower = note_status.lower().replace("✅", "").replace("🔄", "").strip()
            if expected and not any(e in note_status_lower for e in expected):
                issues.append(f"ROADMAP_DRIFT: Phase {phase_num} — roadmap shows {roadmap_status_symbol}, note says '{note_status}'")
    return issues, phase_statuses


def check_missing_extensions(vault_root, config):
    """Find markdown files missing the .md extension."""
    issues = []
    scan_folders = config.get("cross_refs", {}).get("scan_folders", [])
    scan_folders = list(scan_folders)
    scan_folders.append("./")
    for folder in scan_folders:
        target_dir = vault_root / folder
        if not target_dir.exists():
            continue
        for filepath in target_dir.rglob("*"):
            if should_skip_path(filepath, config):
                continue
            if filepath.is_file() and not filepath.suffix:
                # Check if it looks like markdown (starts with # or has frontmatter)
                try:
                    with open(filepath, "r") as f:
                        first_line = f.readline()
                    if first_line.startswith("#") or first_line.startswith("---"):
                        rel_path = filepath.relative_to(vault_root)
                        issues.append(f"MISSING_EXTENSION: {rel_path} (add .md)")
                except:
                    pass
    return issues

def check_orphan_notes(vault_root, config):
    """Informational: notes in scan folders with zero inbound wikilinks.
    Reported but NOT counted as issues — orphan status is diagnosis, not failure."""
    scan_folders = config.get("cross_refs", {}).get("scan_folders", [])
    link_pattern = re.compile(r"\[\[([^\]]+)\]\]")
    note_stems = {}
    all_outbound = set()
    for folder in scan_folders:
        target_dir = vault_root / folder
        if not target_dir.exists():
            continue
        for filepath in target_dir.rglob("*.md"):
            if should_skip_path(filepath, config):
                continue
            note_stems[filepath.stem] = str(filepath.relative_to(vault_root))
            try:
                content = filepath.read_text()
            except Exception:
                continue
            for link in link_pattern.findall(content):
                clean = link.split("#")[0].split("|")[0].strip()
                if clean:
                    all_outbound.add(clean)
    orphans = []
    for stem, rel in sorted(note_stems.items()):
        if stem in all_outbound:
            continue
        # fuzzy: allow prefix/substring refs
        if any(stem in ref or ref in stem for ref in all_outbound if len(ref) > 6):
            continue
        # skip trivial/template stems
        if stem in ("note-one", "note-two", "Public README.md"):
            continue
        orphans.append(rel)
    return orphans

def append_trend_snapshot(stats):
    """Append one Zulu-stamped line to the trend CSV. Header on first write."""
    log_dir = SCRIPT_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    trend_path = log_dir / "vault_health_trends.csv"
    if not trend_path.exists():
        trend_path.write_text("timestamp_utc,files_checked,issues_found\n")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    with open(trend_path, "a") as f:
        f.write(f"{ts},{stats['files_checked']},{stats['issues_found']}\n")
    return trend_path

def write_html_dashboard(vault_root, config, stats, section_results, issues_count):
    """Write a human-readable HTML dashboard next to the text report."""
    log_dir = SCRIPT_DIR / config["reporting"].get("output_dir", "logs/")
    log_dir.mkdir(exist_ok=True)
    html_path = log_dir / "vault_health_dashboard.html"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    healthy = issues_count == 0
    badge = ("background:#1a7f37;", "HEALTHY — THE MYCELIUM IS CLEAN") if healthy \
            else ("background:#b35900;", f"{issues_count} ISSUE(S) FOUND")
    rows = ""
    for section_name, (checked, issue_count) in section_results.items():
        mark = "✅" if issue_count == 0 else "⚠️"
        rows += f"<tr><td>{mark} {section_name}</td><td>{checked}</td><td>{issue_count}</td></tr>\n"
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>CADMIES Vault Health Dashboard</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; background:#0d1117; color:#c9d1d9; }}
.badge {{ display:inline-block; color:#fff; padding:.35rem .8rem; border-radius:6px; font-weight:600; }}
table {{ border-collapse: collapse; width:100%; margin-top:1.2rem; }}
td, th {{ border:1px solid #30363d; padding:.45rem .8rem; text-align:left; }}
th {{ background:#161b22; }}
h1 {{ font-size:1.3rem; }} .meta {{ color:#8b949e; font-size:.9rem; }}
</style></head><body>
<h1>🌱 CADMIES Vault Health Dashboard</h1>
<p class="meta">{ts} · {stats['files_checked']} files checked · vault: {vault_root.name}</p>
<p><span class="badge" style="{badge[0]}">{badge[1]}</span></p>
<table><tr><th>Section</th><th>Files</th><th>Issues</th></tr>
{rows}</table>
<p class="meta">History: vault_health_trends.csv · Text report: vault_health_report.txt</p>
</body></html>"""
    html_path.write_text(html)
    return html_path

def run_validation(fix_mode=False, auto_yes=False):
    config = load_config()
    vault_root = get_vault_root(config)
    all_issues = []
    total_fixes = 0
    stats = {"files_checked": 0, "issues_found": 0}
    section_results = {}  # name -> (files_checked, issues) for the HTML dashboard

    mode_label = "FIX MODE" if fix_mode else "REPORT MODE"
    if auto_yes:
        mode_label = "AUTO-FIX MODE"

    print(f"\n{'='*60}")
    print(f"  🌱 CADMIES VAULT HEALTH REPORT — {mode_label}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Vault: {vault_root}")
    print(f"{'='*60}\n")

    skip_all = False

    for doc_type, rules in config["doc_types"].items():
        folder = rules.get("folder", "")
        pattern = rules.get("name_pattern", "*.md")
        if "filename" in rules:
            filepath = vault_root / folder / rules["filename"]
            files = [filepath] if filepath.exists() else []
        else:
            files = find_files(vault_root, folder, pattern)
        if not files:
            continue
        print(f"── {doc_type} ({len(files)} files) ──")
        _sec_start_issues = stats["issues_found"]
        _sec_start_files = stats["files_checked"]
        for filepath in files:
            if should_skip_path(filepath, config):
                continue
            rel = filepath.relative_to(vault_root) if filepath.is_relative_to(vault_root) else filepath.name
            stats["files_checked"] += 1
            file_issues = []
            fixes = 0
            fm_issues, fm_fixes = check_frontmatter(filepath, doc_type, config, fix_mode and not skip_all, auto_yes)
            file_issues.extend(fm_issues)
            fixes += fm_fixes
            file_issues.extend(check_sections(filepath, doc_type, config))
            banner_issues, banner_fixes = check_raw_banner(filepath, doc_type, config, fix_mode and not skip_all, auto_yes)
            file_issues.extend(banner_issues)
            fixes += banner_fixes
            if file_issues:
                print(f"  ⚠️  {rel}")
                for issue in file_issues:
                    print(f"     → {issue}")
                    stats["issues_found"] += 1
                all_issues.extend([f"{rel}: {i}" for i in file_issues])
            else:
                if config.get("reporting", {}).get("show_passing", True):
                    print(f"  ✅ {rel}")
            total_fixes += fixes
        section_results[doc_type] = (stats["files_checked"] - _sec_start_files,
                                     stats["issues_found"] - _sec_start_issues)

    print(f"\n── Cross-Reference Check ──")
    ref_issues, ref_fixes = check_and_fix_cross_references(vault_root, config, fix_mode and not skip_all, auto_yes)
    total_fixes += ref_fixes
    section_results["cross_references"] = (0, len(ref_issues))
    if ref_issues:
        for issue in ref_issues:
            print(f"  🔗 {issue}")
            stats["issues_found"] += 1
        all_issues.extend(ref_issues)
    else:
        print(f"  ✅ All wikilinks resolve")

    print(f"\n── Missing Extensions ──")
    ext_issues = check_missing_extensions(vault_root, config)
    if ext_issues:
        for issue in ext_issues:
            print(f"  📄 {issue}")
            stats["issues_found"] += 1
        all_issues.extend(ext_issues)
    else:
        print(f"  ✅ All markdown files have .md extension")

    print(f"\n── Duplicate Check ──")
    dup_issues = check_duplicates(vault_root, config)
    if dup_issues:
        for issue in dup_issues:
            print(f"  👯 {issue}")
            stats["issues_found"] += 1
        all_issues.extend(dup_issues)
    else:
        print(f"  ✅ No duplicates found")

    print(f"\n── Orphan Notes (informational) ──")
    orphan_list = check_orphan_notes(vault_root, config)
    section_results["orphan_notes_info"] = (len(orphan_list), 0)
    if orphan_list:
        for o in orphan_list:
            print(f"  🍄 ORPHAN: {o} (no inbound wikilinks)")
    else:
        print(f"  ✅ No orphans — every note is referenced")

    print(f"\n── Roadmap Sync ──")
    drift_issues, phase_statuses = check_roadmap_drift(vault_root, config, fix_mode and not skip_all, auto_yes)
    section_results["roadmap_sync"] = (0, len(drift_issues))
    if drift_issues:
        for issue in drift_issues:
            print(f"  🗺️  {issue}")
            stats["issues_found"] += 1
        all_issues.extend(drift_issues)
        
        # Auto-fix roadmap drift
        if fix_mode and not skip_all:
            from pathlib import Path
            roadmap_path = vault_root / "growth_roadmap.md"
            for phase_num, note_status in phase_statuses.items():
                status_lower = note_status.lower()
                if "complete" in status_lower:
                    symbol = "✅"
                elif "progress" in status_lower:
                    symbol = "🔄"
                elif "designed" in status_lower or "planned" in status_lower or "postponed" in status_lower:
                    symbol = "📋"
                elif "abandoned" in status_lower:
                    symbol = "🔴"
                else:
                    continue
                desc = f"Update roadmap: Phase {phase_num} status"
                before = f"Phase {phase_num} roadmap entry"
                after = f"Phase {phase_num} → {symbol}"
                result = confirm_fix(desc, before, after, auto_yes)
                if result == "skip_all":
                    skip_all = True
                    auto_yes = False
                elif result:
                    backup_file(roadmap_path)
                    with open(roadmap_path, "r") as f:
                        roadmap = f.read()
                    pattern = rf"(\\|\\s*\\*\\*Phase {re.escape(phase_num)}:.*?\\|\\s*)[✅📋🔄💡🔴](\\s*\\|)"
                    roadmap = re.sub(pattern, f"\\\\g<1>{symbol}\\\\g<2>", roadmap)
                    with open(roadmap_path, "w") as f:
                        f.write(roadmap)
                    total_fixes += 1
                    print(f"     ✅ Fixed: Phase {phase_num} roadmap → {symbol}")
    else:
        print(f"  ✅ Roadmap matches phase notes")

    print(f"\n{'='*60}")
    print(f"  📊 SUMMARY")
    print(f"  Files checked: {stats['files_checked']}")
    print(f"  Issues found:  {stats['issues_found']}")
    if fix_mode:
        print(f"  Fixes applied: {total_fixes}")
    if stats["issues_found"] == 0:
        print(f"  ✅ Vault is healthy. The mycelium is clean.")
    else:
        if fix_mode:
            print(f"  ⚠️  Remaining issues require manual attention.")
        else:
            print(f"  ⚠️  Run with --fix to resolve auto-fixable issues.")
    print(f"{'='*60}\n")

    if config.get("reporting", {}).get("save_report", False):
        log_dir = SCRIPT_DIR / config["reporting"].get("output_dir", "logs/")
        log_dir.mkdir(exist_ok=True)
        report_path = log_dir / config["reporting"].get("report_filename", "vault_health_report.txt")
        with open(report_path, "w") as f:
            f.write(f"CADMIES Vault Health Report — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Mode: {mode_label}\n")
            f.write(f"Vault: {vault_root}\n")
            f.write(f"Files checked: {stats['files_checked']}\n")
            f.write(f"Issues found: {stats['issues_found']}\n")
            if fix_mode:
                f.write(f"Fixes applied: {total_fixes}\n")
            f.write("\n")
            for issue in all_issues:
                f.write(f"{issue}\n")
        print(f"  Report saved to: {report_path}")

    trend_path = append_trend_snapshot(stats)
    print(f"  Trend snapshot appended: {trend_path.name}")
    html_path = write_html_dashboard(vault_root, config, stats, section_results, stats["issues_found"])
    print(f"  HTML dashboard: {html_path.name}")

    return 0 if stats["issues_found"] == 0 else 1

if __name__ == "__main__":
    fix_mode = "--fix" in sys.argv
    auto_yes = "--yes" in sys.argv
    exit(run_validation(fix_mode=fix_mode, auto_yes=auto_yes))
