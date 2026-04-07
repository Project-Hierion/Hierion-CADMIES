#!/usr/bin/env python3
"""
import_from_github.py v1.0.0
Purpose: Download a CAR file from GitHub and import to CADMIES
Usage: python tools/import_from_github.py --url <GitHub_CAR_url> [--keep]
"""

import argparse
import sys
import subprocess
from pathlib import Path
import urllib.request
import urllib.error

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
INCOMING_DIR = PROJECT_ROOT / "incoming_cars"


# ============================================================================
# FUNCTIONS
# ============================================================================

def ensure_incoming_dir():
    """Create incoming_cars directory if it doesn't exist."""
    INCOMING_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Incoming CARs directory: {INCOMING_DIR}")


def download_file(url: str, destination: Path) -> bool:
    """
    Download a file from URL to destination.
    
    Args:
        url: Source URL
        destination: Where to save the file
    
    Returns:
        True if successful, False otherwise
    """
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
    """
    Import a CAR file using import_from_car.py.
    
    Args:
        car_path: Path to CAR file
        dry_run: If True, preview without importing
        verbose: Show detailed output
    
    Returns:
        True if successful, False otherwise
    """
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
        description="Download CAR file from GitHub and import to CADMIES",
        epilog="""
Examples:
  # Download and import (CAR will be deleted after import)
  python tools/import_from_github.py --url https://github.com/user/repo/releases/download/v1/file.car
  
  # Download, import, and keep the CAR file
  python tools/import_from_github.py --url https://github.com/.../file.car --keep
  
  # Preview without importing
  python tools/import_from_github.py --url https://github.com/.../file.car --dry-run
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--url', '-u',
        required=True,
        help='GitHub URL of the CAR file to download'
    )
    
    parser.add_argument(
        '--keep',
        action='store_true',
        help='Keep the CAR file after import (default: delete after successful import)'
    )
    
    parser.add_argument(
        '--dry-run', '-n',
        action='store_true',
        help='Preview import without making changes'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    
    args = parser.parse_args()
    
    # Ensure incoming directory exists
    ensure_incoming_dir()
    
    # Extract filename from URL
    filename = args.url.split('/')[-1]
    if not filename.endswith('.car'):
        filename += '.car'
    
    car_path = INCOMING_DIR / filename
    
    # Download the file
    if not download_file(args.url, car_path):
        sys.exit(1)
    
    # Import the CAR file
    success = import_car(car_path, dry_run=args.dry_run, verbose=args.verbose)
    
    if not success:
        print("❌ Import failed")
        sys.exit(1)
    
    # Cleanup unless --keep or --dry-run
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