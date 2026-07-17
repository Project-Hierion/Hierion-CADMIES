#!/usr/bin/env python3
"""
File: validate_vault.py
Tool: CADMIES Vault Validator
Version: 1.2.0
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
"""

import os
import re
import sys
import yaml
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "config.yaml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def get_vault_root(config):
    vault_rel = config.get("vault_root", "../CADMIES-IPLD/Scientific Obsidian")
    return (SCRIPT_DIR / vault_rel).resolve()

def should_skip_path(filepath):
    parts = str(filepath).split("/")
    for part in parts:
        if part.startswith(".") or part == ".ipynb_checkpoints":
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
                if should_skip_path(f):
                    continue
                note_index[f.stem] = str(f.relative_to(vault_root))
    for f in vault_root.glob("*.md"):
        note_index[f.stem] = f.name
    meta_dir = vault_root / "00-Meta"
    if meta_dir.exists():
        for f in meta_dir.rglob("*.md"):
            if should_skip_path(f):
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
            if should_skip_path(filepath):
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
            if should_skip_path(filepath):
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

def check_roadmap_drift(vault_root, config):
    issues = []
    roadmap_path = vault_root / "growth_roadmap.md"
    if not roadmap_path.exists():
        issues.append("ROADMAP_NOT_FOUND: growth_roadmap.md missing from vault root")
        return issues
    phases_dir = vault_root / "Polished-CADMIES/03-Development/"
    phase_statuses = {}
    if phases_dir.exists():
        for f in phases_dir.glob("Phase-*.md"):
            if should_skip_path(f):
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
    return issues

def run_validation(fix_mode=False, auto_yes=False):
    config = load_config()
    vault_root = get_vault_root(config)
    all_issues = []
    total_fixes = 0
    stats = {"files_checked": 0, "issues_found": 0}

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
        for filepath in files:
            if should_skip_path(filepath):
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

    print(f"\n── Cross-Reference Check ──")
    ref_issues, ref_fixes = check_and_fix_cross_references(vault_root, config, fix_mode and not skip_all, auto_yes)
    total_fixes += ref_fixes
    if ref_issues:
        for issue in ref_issues:
            print(f"  🔗 {issue}")
            stats["issues_found"] += 1
        all_issues.extend(ref_issues)
    else:
        print(f"  ✅ All wikilinks resolve")

    print(f"\n── Duplicate Check ──")
    dup_issues = check_duplicates(vault_root, config)
    if dup_issues:
        for issue in dup_issues:
            print(f"  👯 {issue}")
            stats["issues_found"] += 1
        all_issues.extend(dup_issues)
    else:
        print(f"  ✅ No duplicates found")

    print(f"\n── Roadmap Sync ──")
    drift_issues = check_roadmap_drift(vault_root, config)
    if drift_issues:
        for issue in drift_issues:
            print(f"  🗺️  {issue}")
            stats["issues_found"] += 1
        all_issues.extend(drift_issues)
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

    return 0 if stats["issues_found"] == 0 else 1

if __name__ == "__main__":
    fix_mode = "--fix" in sys.argv
    auto_yes = "--yes" in sys.argv
    exit(run_validation(fix_mode=fix_mode, auto_yes=auto_yes))
