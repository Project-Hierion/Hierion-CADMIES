#!/usr/bin/env python3
"""
File: validate_vault.py
Tool: CADMIES Vault Validator
Version: 1.1.0
System: CADMIES / repo-maintenance-automation
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Scans the Scientific Obsidian vault and reports on frontmatter
         consistency, dead wikilinks, duplicate files, and roadmap drift.
         Phase 2 — read-only reporting + interactive --fix mode with
         before/after previews.

Usage:
    python repo-maintenance-automation/validate_vault.py          # Report only
    python repo-maintenance-automation/validate_vault.py --fix    # Interactive fixes
    python repo-maintenance-automation/validate_vault.py --fix --yes  # Auto-apply all

Output:
    Terminal report + saved log file in logs/vault_health_report.txt

Version History:
  v1.0.0 (2026-07-16): Initial read-only validator.
  v1.0.1 (2026-07-16): Fixed YAML parsing for [[wikilinks]] in frontmatter.
                       Fixed duplicate detector self-comparison.
  v1.0.2 (2026-07-16): Skip .ipynb_checkpoints and hidden directories.
  v1.1.0 (2026-07-16): --fix mode with before/after previews, interactive confirmations,
                       and automatic backups before modification.
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

# ──────────────────────────────────────────────────────────────
# CONFIG LOADING
# ──────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "config.yaml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

# ──────────────────────────────────────────────────────────────
# FILE DISCOVERY
# ──────────────────────────────────────────────────────────────

def get_vault_root(config):
    vault_rel = config.get("vault_root", "../CADMIES-IPLD/Scientific Obsidian")
    return (SCRIPT_DIR / vault_rel).resolve()

def should_skip_path(filepath):
    """Skip hidden directories and Jupyter checkpoint files."""
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

# ──────────────────────────────────────────────────────────────
# BACKUP
# ──────────────────────────────────────────────────────────────

def backup_file(filepath):
    """Create a timestamped backup of a file before modifying it."""
    backup_dir = SCRIPT_DIR / "logs" / "backups"
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"{filepath.name}.{timestamp}.bak"
    shutil.copy2(filepath, backup_path)
    return backup_path

# ──────────────────────────────────────────────────────────────
# FRONTMATTER PARSING (with wikilink tolerance)
# ──────────────────────────────────────────────────────────────

def parse_frontmatter(filepath):
    """
    Extract YAML frontmatter from a markdown file.
    Handles [[wikilinks]] in fields like 'related' by quoting them
    before YAML parsing.
    Returns (dict or None, body_text).
    """
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

# ──────────────────────────────────────────────────────────────
# INTERACTIVE CONFIRMATION
# ──────────────────────────────────────────────────────────────

def confirm_fix(description, before, after, auto_yes=False):
    """Show a before/after diff and ask for confirmation."""
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

# ──────────────────────────────────────────────────────────────
# FRONTMATTER CHECKING + FIXING
# ──────────────────────────────────────────────────────────────

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

    # Check status against valid values
    valid_statuses = rules.get("valid_statuses", [])
    if valid_statuses and "status" in fm and fix_mode:
        raw_status = str(fm["status"])
        matched = False
        for vs in valid_statuses:
            if vs.lower() in raw_status.lower():
                matched = True
                break
        
        if not matched:
            # Try to auto-detect the right status
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
                    # Apply the fix
                    backup_file(filepath)
                    with open(filepath, "r") as f:
                        content = f.read()
                    # Replace the status line in the YAML frontmatter
                    new_content = content.replace(
                        f"status: {raw_status}",
                        f"status: {suggested}"
                    )
                    with open(filepath, "w") as f:
                        f.write(new_content)
                    fixes_applied += 1
                    print(f"     ✅ Fixed: status → '{suggested}'")
                    return [], fixes_applied  # No more issues for this file

    return issues, fixes_applied

# ──────────────────────────────────────────────────────────────
# SECTION CHECKING
# ──────────────────────────────────────────────────────────────

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

# ──────────────────────────────────────────────────────────────
# RAW BANNER CHECKING + FIXING
# ──────────────────────────────────────────────────────────────

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
                # Check if file starts with a heading
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

# ──────────────────────────────────────────────────────────────
# CROSS-REFERENCE CHECKING
# ──────────────────────────────────────────────────────────────

def check_cross_references(vault_root, config):
    issues = []
    scan_folders = config.get("cross_refs", {}).get("scan_folders", [])
    link_pattern = re.compile(r"\[\[([^\]]+)\]\]")

    # Build a set of all known note titles (without .md extension)
    all_notes = set()
    for folder in scan_folders:
        target_dir = vault_root / folder
        if target_dir.exists():
            for f in target_dir.rglob("*.md"):
                if should_skip_path(f):
                    continue
                all_notes.add(f.stem)

    # Also add vault root and meta files
    for f in vault_root.glob("*.md"):
        all_notes.add(f.stem)
    meta_dir = vault_root / "00-Meta"
    if meta_dir.exists():
        for f in meta_dir.rglob("*.md"):
            if should_skip_path(f):
                continue
            all_notes.add(f.stem)

    # Scan each file for wikilinks
    for folder in scan_folders:
        target_dir = vault_root / folder
        if not target_dir.exists():
            continue
        for filepath in target_dir.rglob("*.md"):
            if should_skip_path(filepath):
                continue
            with open(filepath, "r") as f:
                content = f.read()
            links = link_pattern.findall(content)
            for link in links:
                clean_link = link.split("#")[0].split("|")[0].strip()
                if clean_link not in all_notes:
                    rel_path = filepath.relative_to(vault_root)
                    issues.append(f"DEAD_LINK: {rel_path} -> [[{link}]] (target not found)")

    return issues

# ──────────────────────────────────────────────────────────────
# DUPLICATE DETECTION
# ──────────────────────────────────────────────────────────────

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

# ──────────────────────────────────────────────────────────────
# ROADMAP DRIFT CHECKING
# ──────────────────────────────────────────────────────────────

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
                issues.append(
                    f"ROADMAP_DRIFT: Phase {phase_num} — roadmap shows {roadmap_status_symbol}, "
                    f"note says '{note_status}'"
                )

    return issues

# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────

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

    # Cross-reference check
    print(f"\n── Cross-Reference Check ──")
    ref_issues = check_cross_references(vault_root, config)
    if ref_issues:
        for issue in ref_issues:
            print(f"  🔗 {issue}")
            stats["issues_found"] += 1
        all_issues.extend(ref_issues)
    else:
        print(f"  ✅ All wikilinks resolve")

    # Duplicate check
    print(f"\n── Duplicate Check ──")
    dup_issues = check_duplicates(vault_root, config)
    if dup_issues:
        for issue in dup_issues:
            print(f"  👯 {issue}")
            stats["issues_found"] += 1
        all_issues.extend(dup_issues)
    else:
        print(f"  ✅ No duplicates found")

    # Roadmap drift check
    print(f"\n── Roadmap Sync ──")
    drift_issues = check_roadmap_drift(vault_root, config)
    if drift_issues:
        for issue in drift_issues:
            print(f"  🗺️  {issue}")
            stats["issues_found"] += 1
        all_issues.extend(drift_issues)
    else:
        print(f"  ✅ Roadmap matches phase notes")

    # Summary
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

    # Save report
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
