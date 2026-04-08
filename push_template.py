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

def main():
    import sys
    
    # Check for test flag
    test_mode = "--test" in sys.argv
    
    VERSION_FILE = "template_workflow/version.json"
    
    # Bump minor version (skip in test mode)
    if not test_mode:
        print("Bumping minor version...")
        
        # Read current version
        with open(VERSION_FILE, 'r') as f:
            version_data = json.load(f)
        current_version = version_data['version']
        print(f"previous version: {current_version}")
        
        # Increment patch version
        parts = current_version.split('.')
        parts[2] = str(int(parts[2]) + 1)
        new_version = '.'.join(parts)
        print(f"current version was: {new_version}")
        
        # Update version file
        version_data['version'] = new_version
        with open(VERSION_FILE, 'w') as f:
            json.dump(version_data, f, indent=2)
        print(f"Version bumped to {new_version}")
    else:
        print("TEST MODE: Skipping version bump")
        # Read current version for display
        with open(VERSION_FILE, 'r') as f:
            version_data = json.load(f)
        new_version = version_data['version']
        print(f"Using current version: {new_version}")
    
    # Stage everything
    print("Staging all files...")
    run_command("git add .")
    
    # Files and directories to exclude
    exclusions = [
        "Features/",
        "meetings/", 
        "tasks.csv",
        "push_template.sh",
        "push_template.py"
    ]
    
    # Unstage exclusions
    print("Excluding dev-specific files...")
    for exclusion in exclusions:
        stdout, stderr = run_command(f"git restore --staged {exclusion}", check=False)
        if stderr and "did not match" not in stderr:
            print(f"  Excluded {exclusion}")
        elif not stderr:
            print(f"  Excluded {exclusion}")
    
    # Also exclude any files directly in Features directory
    features_dir = Path("Features")
    if features_dir.exists():
        for item in features_dir.iterdir():
            if item.is_dir():
                stdout, stderr = run_command(f"git restore --staged {item}", check=False)
                if stderr and "did not match" not in stderr:
                    print(f"  Excluded {item}/")
                elif not stderr:
                    print(f"  Excluded {item}/")
    
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
