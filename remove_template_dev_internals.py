#!/usr/bin/env python3
"""
push_template.py
Bumps minor version, syncs current state to the main (template) branch.
Uses git status to collect files, filters out excluded items, then stages only approved files.
"""

import json
import subprocess
import sys
from pathlib import Path

# Files and directories to exclude
EXCLUSIONS = [
    "Features/",
    "meetings/",
    "tasks.csv",
    "push_template.sh",
    "push_template.py",
    "remove_template_dev_internals.py"
]

def run_command(cmd, capture_output=True, check=True, test_mode=False):
    """Run a shell command and return result."""
    try:
        if test_mode:
            cmd = "echo " + cmd

        result = subprocess.run(cmd, shell=True, capture_output=capture_output,
                              text=True, check=check)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        if check:
            print(f"Error running command: {cmd}")
            print(f"Error: {e.stderr}")
            sys.exit(1)
        return e.stdout.strip(), e.stderr.strip()

def should_exclude(filepath):
    """Check if file matches any exclusion pattern."""
    for exclusion in EXCLUSIONS:
        # Handle both directory (Features/) and exact file (push_template.py) matches
        if exclusion.endswith('/'):
            # Directory: check prefix
            if filepath.startswith(exclusion):
                return True
        else:
            # File: check exact match or as filename
            if filepath == exclusion or filepath.endswith('/' + exclusion):
                return True
    return False

def get_git_status_files():
    """Get modified and untracked files from git status."""
    stdout, _ = run_command("git status --porcelain", check=False)
    files = []

    for line in stdout.split('\n'):
        if not line.strip():
            continue
        # Format: XY filename (X = staged status, Y = working tree status, then space, then filename)
        # Examples: " M file.txt" (modified), "?? file.txt" (untracked), "M file.txt" (can be just status + space + file)
        filepath = line[3:] if len(line) > 3 and line[2] == ' ' else line[2:]

        if filepath:
            files.append(filepath)

    return files

def bump_version(version, bump_type="patch"):
    """Bump version by major, minor, or patch."""
    parts = version.split('.')
    if bump_type == "major":
        parts[0] = str(int(parts[0]) + 1)
        parts[1] = "0"
        parts[2] = "0"
    elif bump_type == "minor":
        parts[1] = str(int(parts[1]) + 1)
        parts[2] = "0"
    else:  # patch
        parts[2] = str(int(parts[2]) + 1)
    return '.'.join(parts)

def save_to_file(file_path, data):
    """Save data to JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def load_from_file(file_path):
    """Load data from JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def resolve_merge_conflicts():
    """Resolve modify/delete conflicts by removing excluded files."""
    stdout, _ = run_command("git status --porcelain", check=False)

    conflicts_resolved = False
    for line in stdout.split('\n'):
        if not line.strip():
            continue
        # Detect deleted/modified conflicts (DU or UD status)
        if line[:2] in ['DU', 'UD']:
            filepath = line[3:]
            if should_exclude(filepath):
                run_command(f'git rm "{filepath}"')
                conflicts_resolved = True

    # Complete the merge after resolving conflicts
    if conflicts_resolved:
        run_command('git commit -m "Merge origin/dev, resolve conflicts by removing excluded files"')

def show_help():
    """Display usage information."""
    print()
    print("Options:")
    print("  --major    Bump major version (1.1.17 → 2.0.0)")
    print("  --minor    Bump minor version (1.1.17 → 1.2.0)")
    print("  --patch    Bump patch version (1.1.17 → 1.1.18) [default]")
    print("  --test     Run in test mode (skip commit/push)")
    print("  --latest   Show latest version in origin/main")
    print()
    print("  --help (or no args)    Show this help message")
    print()

def show_latest():
    """Display the latest version from origin/main."""
    try:
        stdout, _ = run_command("git show origin/main:template_workflow/version.json", check=False)
        if stdout:
            data = json.loads(stdout)
            print(f"Latest version in origin/main: {data.get('version', 'unknown')}")
        else:
            print("Could not fetch version from origin/main")
    except Exception as e:
        print(f"Error fetching latest version: {e}")

def main():
    if "--help" in sys.argv or (len(sys.argv) == 1):
        show_help()
        return

    if "--latest" in sys.argv:
        show_latest()
        return

    test_mode = "--test" in sys.argv
    bump_type = "patch"

    # Parse version bump type from args
    for arg in sys.argv[1:]:
        if arg in ["--major", "--minor", "--patch"]:
            bump_type = arg.lstrip("--")
            break

    VERSION_FILE = Path("template_workflow/version.json").resolve()

    # Resolve any merge conflicts with excluded files
    resolve_merge_conflicts()

    # Read current version
    version_data = load_from_file(VERSION_FILE)
    current_version = version_data['version']
    print(f"Current template version: {current_version}")

    # Bump version (skip in test mode)
    if not test_mode:
        new_version = bump_version(current_version, bump_type)
        version_data['version'] = new_version
        save_to_file(VERSION_FILE, version_data)
        print(f"Version bumped to {new_version}")
    else:
        new_version = current_version
        print("TEST MODE: Skipping version bump")

    # Get files from git status
    print("\nScanning git status...")
    all_files = get_git_status_files()
    if test_mode:
        print("\nFiles in status:")
        print("-" * 13)
        for i, f in enumerate(all_files, 1):
            print(f"{i}. /{f}")

    if not all_files:
        print("No changes to commit.")
        return


    # Filter out excluded items
    print("\nApproved:")
    print("-" * 19)
    approved_files = [f for f in all_files if not should_exclude(f)]
    for i, f in enumerate(approved_files, 1):
        print(f"{i}. /{f}")
    
    excluded_files = [f for f in all_files if should_exclude(f)]
    
    print("\nExcluded:")
    print("-" * 27)
    for i, f in enumerate(excluded_files, 1):
        print(f"{i}. /{f}")



    # Clean output
    print("\nfiles/folders to be excluded:")
    print("-" * 27)
    if excluded_files:
        for i, f in enumerate(excluded_files, 1):
            print(f"{i}. /{f}")
    else:
        print("none")

    print("\nfiles to be pushed:")
    print("-" * 19)
    if approved_files:
        for i, f in enumerate(approved_files, 1):
            print(f"{i}. /{f}")
    else:
        print("none")

    # Stage approved files
    if approved_files:
        # Quote filenames to handle spaces
        files_str = ' '.join(f'"{f}"' for f in approved_files)
        run_command(f"git add {files_str}")
    else:
        print("\nNo approved files to stage.")


    # Commit and push (skip in test mode)
    if not test_mode and approved_files:
        run_command(f'git commit -m "chore: release template v{new_version}"')
        run_command("git push origin HEAD:main --force")
        
        if current_version != new_version:
            print(f"\nDone. main is now template v{new_version}.")
    else:
        print("\nNo files to commit.")
        sys.exit(1)

if __name__ == "__main__":
    main()
