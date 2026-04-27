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
    "push_template.py"
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

def bump_patch_version(version):
    """Bump the patch version."""
    parts = version.split('.')
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

def main():
    test_mode = "--test" in sys.argv

    VERSION_FILE = "template_workflow/version.json"

    # Read current version
    version_data = load_from_file(VERSION_FILE)
    current_version = version_data['version']
    print(f"Current template version: {current_version}")

    # Bump version (skip in test mode)
    if not test_mode:
        new_version = bump_patch_version(current_version)
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
