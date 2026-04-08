#!/usr/bin/env python3
"""
push_template.py
Bumps minor version, syncs current state to the main (template) branch.
Stages everything except Features/, meetings/, and tasks.csv, then force-pushes to main.
"""

import json
import subprocess
import sys
from pathlib import Path

# Files and directories to exclude
exclusions = [
    "Features/",
    "meetings/", 
    "tasks.csv",
    "push_template.sh",
    "push_template.py"
]


def run_command(cmd, capture_output=True, check=True):
    """Run a shell command and return result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, 
                              text=True, check=check)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        if check:
            print(f"Error running command: {cmd}")
            print(f"Error: {e.stderr}")
            sys.exit(1)
        return e.stdout.strip(), e.stderr.strip()

def BumpPatchNumber(version):
    parts = version.split('.')
    parts[2] = str(int(parts[2]) + 1)
    return '.'.join(parts)

def unstage(path):
    """Walk directory or return single file list for unstaging."""
    import os
    files_to_unstage = []
    
    if not os.path.exists(path):
        print(f"Warning: {path} does not exist, skipping")
        return files_to_unstage
    
    if os.path.isfile(path):
        # Single file
        return [path]
    
    # Directory - walk it
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            files_to_unstage.append(filepath)
        for d in dirs:
            dirpath = os.path.join(root, d)
            files_to_unstage.append(dirpath)
    
    return files_to_unstage

def save_to_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def load_from_file(file_path):
    with open(file_path, 'r') as f:
        version_data = json.load(f)
    return version_data

def main():
    import sys
    
    # Check for test flag
    test_mode = "--test" in sys.argv
    
    VERSION_FILE = "template_workflow/version.json"
    # Read current version
    version_data = load_from_file(VERSION_FILE)
    current_version = version_data['version']
    print(f"current template version: {current_version}")
    
    # Bump version (skip in test mode)
    if not test_mode:
        print("Bumping version...")

        new_version = BumpPatchNumber(current_version)
        
        version_file_data = version_data.copy()
        version_file_data['version'] = new_version

        save_to_file(VERSION_FILE, version_file_data)
        print(f"Version bumped to {new_version}")
    else:
        print("TEST MODE: Skipping version bump")
        # Read current version for display
        version_data = load_from_file(VERSION_FILE)
        new_version = version_data['version']
    
    # Stage everything
    print("Staging all files...")
    run_command("git add .")
    
    # Collect all files to unstage
    all_files_to_unstage = []
    for exclusion in exclusions:
        files = unstage(exclusion)
        all_files_to_unstage.extend(files)
    
    # Batch unstage in groups of 3
    print(f"Excluding {len(all_files_to_unstage)} dev-specific files...")
    batch_size = 3
    for i in range(0, len(all_files_to_unstage), batch_size):
        batch = all_files_to_unstage[i:i+batch_size]
        files_str = ' '.join(f'"{f}"' for f in batch)
        run_command(f"git restore --staged {files_str}", check=False)
    
    print(f"  Excluded {len(all_files_to_unstage)} files from main")
    
    # Commit and push (skip in test mode)
    if not test_mode:
        # Commit
        print(f"Committing template v{new_version}...")
        run_command(f'git commit -m "chore: release template v{new_version}"')
        
        # Force push to main
        print("Pushing to main branch...")
        run_command("git push origin HEAD:main --force")
        
        print(f"\nDone. main is now template v{new_version}.")
    else:
        print("TEST MODE: Skipping commit and push")
        print("\nTest complete. Check 'git status' to see what would be staged.")

if __name__ == "__main__":
    main()
