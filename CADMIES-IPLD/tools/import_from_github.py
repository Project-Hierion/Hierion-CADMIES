#!/usr/bin/env python3
"""
File: import_from_github.py
Tool: CADMIES GitHub CAR Downloader
Version: 1.0.0
System: CADMIES / tools
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Download a CAR file from a URL and import into CADMIES.
         Handles download, import, and optional cleanup.

Usage:
    python tools/import_from_github.py --url <CAR_url>
    python tools/import_from_github.py --url <CAR_url> --keep
    python tools/import_from_github.py --url <CAR_url> --dry-run
"""

import argparse
import sys
import subprocess
from pathlib import Path
import urllib.request
import urllib.error

PROJECT_ROOT = Path(__file__).parent.parent
INCOMING_DIR = PROJECT_ROOT / "incoming_cars"


def ensure_incoming_dir():
    """Create incoming_cars directory if it doesn't exist."""
    INCOMING_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Incoming CARs directory: {INCOMING_DIR}")


def download_file(url: str, destination: Path) -> bool:
    """Download a file from URL to destination."""
    try:
        print(f"🌐 Downloading from: {url}")
        urllib.request.urlretrieve(url, destination)
        print(f"✅ Downloaded to: {destination}")
        print(f"   File size: {destination.stat().st_size:,} bytes")
        return True
    except urllib.error.URLError as e:
        print(f"❌ Download failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def import_car(car_path: Path, dry_run: bool = False, verbose: bool = False) -> bool:
    """Import a CAR file using import_from_car.py."""
    import_script = PROJECT_ROOT / "tools" / "import_from_car.py"
    
    if not import_script.exists():
        print(f"❌ import_from_car.py not found at {import_script}")
        return False
    
    cmd = [sys.executable, str(import_script), str(car_path)]
    if dry_run:
        cmd.append("--dry-run")
    if verbose:
        cmd.append("--verbose")
    
    print(f"🔄 Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="CADMIES GitHub CAR Downloader v1.0.0",
        epilog="""
Examples:
  python tools/import_from_github.py --url https://github.com/.../file.car
  python tools/import_from_github.py --url https://github.com/.../file.car --keep
  python tools/import_from_github.py --url https://github.com/.../file.car --dry-run
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--url', '-u', required=True, help='URL of the CAR file to download')
    parser.add_argument('--keep', action='store_true', help='Keep the CAR file after import')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Preview import without making changes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    
    args = parser.parse_args()
    
    ensure_incoming_dir()
    
    filename = args.url.split('/')[-1]
    if not filename.endswith('.car'):
        filename += '.car'
    
    car_path = INCOMING_DIR / filename
    
    if not download_file(args.url, car_path):
        sys.exit(1)
    
    success = import_car(car_path, dry_run=args.dry_run, verbose=args.verbose)
    
    if not success:
        print("❌ Import failed")
        sys.exit(1)
    
    if not args.keep and not args.dry_run:
        car_path.unlink()
        print(f"🗑️  Deleted CAR file: {car_path}")
    elif args.keep:
        print(f"📁 Kept CAR file: {car_path}")
    elif args.dry_run:
        print(f"📁 CAR file preserved (dry-run): {car_path}")
    
    print("\n✅ Done!")
    sys.exit(0)


if __name__ == "__main__":
    main()
