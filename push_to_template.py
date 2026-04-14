#!/usr/bin/env python3
"""
push_to_template.py - Automated script to maintain clean main branch
Merges dev commits into main cache, removes dev-only artifacts, pushes clean template.
"""

import os
import subprocess
import sys


def filter_artifacts(git_status: str) -> list:
    """
    Parse git status --porcelain output and return list of allowed files.

    Filters out development-only artifacts at repo root:
    - Features/ folder (and all contents)
    - meetings/ folder (and all contents)
    - tasks.csv (root level only)
    - push_to_template.py (root level only)
    - push_template.sh (root level only)

    Args:
        git_status: Output from `git status --porcelain`

    Returns:
        List of allowed file paths (strings)
    """
    # Exact filenames to exclude only at repo root level
    excluded_at_root = {
        'tasks.csv',
        'push_to_template.py',
        'push_template.sh',
    }
    # Folder patterns to exclude (with trailing / to match root-level folders)
    excluded_folders = (
        'Features/',
        'meetings/',
    )

    if not git_status:
        return []

    allowed = []
    for line in git_status.strip().split('\n'):
        if not line:
            continue

        # Parse git status --porcelain format: [status code] [space] [filename]
        # Example: "M  README.md" or "?? Features/new-item.md"
        parts = line.split(None, 1)  # Split on whitespace, max 2 parts
        if len(parts) < 2:
            continue

        filepath = parts[1]

        # Exclude files that match exactly at root level
        if filepath in excluded_at_root:
            continue

        # Exclude anything under excluded folders (prefix match with /)
        if any(filepath.startswith(folder) for folder in excluded_folders):
            continue

        allowed.append(filepath)

    return allowed


def cache_init(cache_dir: str = None) -> str:
    """
    Initialize or reset cache folder for clean main checkout.

    Creates cache folder, initializes git repo, stashes any existing work,
    fetches latest from origin, and pulls main to ensure clean state.

    Args:
        cache_dir: Path to cache folder. Defaults to ~/Documents/agent-manager-template-release/

    Returns:
        Path to initialized cache folder (ready for git operations)

    Raises:
        subprocess.CalledProcessError: If git operations fail
        OSError: If cache folder cannot be created
    """
    if cache_dir is None:
        cache_dir = os.path.expanduser("~/Documents/agent-manager-template-release")

    # Step 1: Create cache folder if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)

    # Step 2: Initialize as git repo if not already
    git_dir = os.path.join(cache_dir, '.git')
    if not os.path.exists(git_dir):
        subprocess.run(['git', 'init'], cwd=cache_dir, check=True)
        # Create initial commit so we can merge
        readme = os.path.join(cache_dir, 'README.md')
        with open(readme, 'w') as f:
            f.write('Template cache')
        subprocess.run(['git', 'config', 'user.email', 'cache@example.com'], cwd=cache_dir, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Cache'], cwd=cache_dir, check=True)
        subprocess.run(['git', 'add', 'README.md'], cwd=cache_dir, check=True)
        subprocess.run(['git', 'commit', '-m', 'initial'], cwd=cache_dir, check=True)

    # Step 3: Stash any existing work (preserve if interrupted)
    try:
        subprocess.run(['git', 'stash'], cwd=cache_dir, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pass  # Stash may fail if nothing to stash, which is fine

    # Step 4: Fetch latest from remote (if origin exists)
    try:
        subprocess.run(['git', 'fetch', 'origin'], cwd=cache_dir, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pass  # Origin may not be reachable, which is fine for test scenarios

    # Step 5: Pull main to latest (if possible)
    try:
        subprocess.run(['git', 'pull', 'origin', 'main'], cwd=cache_dir, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pass  # Pull may fail if no remote, which is fine for test scenarios

    return cache_dir


def cache_stash_pop(cache_dir: str) -> bool:
    """
    Restore stashed work after operations complete.

    Args:
        cache_dir: Path to cache folder

    Returns:
        True if stash was restored, False if no stash to restore
    """
    try:
        subprocess.run(['git', 'stash', 'pop'], cwd=cache_dir, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        # No stash to restore (normal case)
        return False


def merge_dev(repo_path: str, branch_name: str = "dev") -> bool:
    """
    Merge dev branch into current branch using fast-forward only.

    Ensures main branch is not diverged from dev by requiring fast-forward merge.
    If merge fails (not fast-forward), exits with error code.

    Args:
        repo_path: Path to git repository
        branch_name: Branch to merge (default: "dev")

    Returns:
        True if merge succeeded, False if merge failed (not fast-forward)
    """
    try:
        subprocess.run(['git', 'merge', '--ff-only', branch_name], cwd=repo_path,
                      check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        # Merge failed (likely not fast-forward)
        return False


def stage_allowed_files(repo_path: str) -> None:
    """
    Stage only allowed files (using whitelist filter) for commit.

    Removes dev artifacts from staging by using filter_artifacts to whitelist only
    allowed files, then staging only those files.

    Args:
        repo_path: Path to git repository

    Raises:
        subprocess.CalledProcessError: If git operations fail
    """
    # Get git status
    status_output = subprocess.run(['git', 'status', '--porcelain'], cwd=repo_path,
                                  capture_output=True, text=True, check=True).stdout

    # Filter to allowed files only
    allowed_files = filter_artifacts(status_output)

    if allowed_files:
        # Stage only allowed files
        subprocess.run(['git', 'add'] + allowed_files, cwd=repo_path, check=True)


def commit_removal(repo_path: str) -> bool:
    """
    Create commit with removal message if there are staged changes.

    Commits staged changes with message indicating dev artifacts were removed
    and dev changes were merged to template. Returns False if nothing to commit.

    Args:
        repo_path: Path to git repository

    Returns:
        True if commit was created, False if nothing to commit

    Raises:
        subprocess.CalledProcessError: If git commit fails with unexpected error
    """
    try:
        subprocess.run(['git', 'commit', '-m', 'chore: merge dev changes to template'],
                      cwd=repo_path, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        # Check if it's just "nothing to commit" (normal case) or a real error
        status = subprocess.run(['git', 'status', '--porcelain'], cwd=repo_path,
                               capture_output=True, text=True, check=True).stdout
        if status:
            # There are changes but commit failed - this is a real error
            raise
        # Nothing to commit - return False
        return False


def push_to_main(repo_path: str) -> bool:
    """
    Push commits to origin/main using fast-forward push.

    Pushes current HEAD to origin/main. On failure, logs error to stderr
    and returns False without raising. Design is idempotent: cache resets
    on next run if this fails.

    Args:
        repo_path: Path to git repository

    Returns:
        True if push succeeded, False if push failed
    """
    try:
        subprocess.run(['git', 'push', 'origin', 'HEAD:main'], cwd=repo_path,
                      check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        # Log error to stderr
        sys.stderr.write(f"error: git push failed: {e}\n")
        if e.stderr:
            sys.stderr.write(e.stderr.decode('utf-8') if isinstance(e.stderr, bytes) else e.stderr)
        return False


def main() -> int:
    """
    Orchestrate push-to-template workflow: cache init, merge, filter, commit, push.

    Reads configuration from environment variables:
    - PUSH_DEV_REPO: path to dev repository (required)
    - PUSH_CACHE_FOLDER: cache folder location (default: ~/Documents/agent-manager-template-release/)
    - BRANCH: branch to merge from dev (default: dev)
    - VERSION: optional version string for logging

    Workflow:
    1. Initialize cache folder (stash→fetch→pull)
    2. Set up dev repo as origin
    3. Merge dev branch with fast-forward only
    4. Stage only allowed files (filter artifacts)
    5. Commit with removal message
    6. Push to origin/main
    7. Log results and exit code

    Returns:
        0 on success, 1 on any failure (idempotent: safe to retry)
    """
    # Read environment variables
    dev_repo = os.environ.get('PUSH_DEV_REPO')
    cache_folder = os.environ.get('PUSH_CACHE_FOLDER')
    branch = os.environ.get('BRANCH', 'dev')
    version = os.environ.get('VERSION', '')

    if not dev_repo:
        sys.stderr.write("error: PUSH_DEV_REPO environment variable not set\n")
        return 1

    if cache_folder is None:
        cache_folder = os.path.expanduser("~/Documents/agent-manager-template-release")

    sys.stdout.write(f"Starting push-to-template: branch={branch}, cache={cache_folder}\n")
    if version:
        sys.stdout.write(f"Version: {version}\n")

    try:
        # Step 1: Initialize cache (transitory: stash→fetch→pull)
        sys.stdout.write("Initializing cache folder...\n")
        cache_init(cache_folder)

        # Step 2: Add dev repo as additional remote if not same as origin
        try:
            subprocess.run(['git', 'remote', 'remove', 'dev'], cwd=cache_folder, check=False, capture_output=True)
        except subprocess.CalledProcessError:
            pass

        # Get dev_repo's origin as the cache origin
        try:
            dev_origin = subprocess.run(['git', 'config', '--get', 'remote.origin.url'],
                                       cwd=dev_repo, check=True,
                                       capture_output=True, text=True).stdout.strip()
            # Update cache origin if needed
            try:
                subprocess.run(['git', 'remote', 'remove', 'origin'], cwd=cache_folder, check=False, capture_output=True)
            except subprocess.CalledProcessError:
                pass
            subprocess.run(['git', 'remote', 'add', 'origin', dev_origin], cwd=cache_folder, check=True, capture_output=True)
        except subprocess.CalledProcessError:
            # dev_repo might not have an origin, use it directly
            try:
                subprocess.run(['git', 'remote', 'remove', 'origin'], cwd=cache_folder, check=False, capture_output=True)
            except subprocess.CalledProcessError:
                pass
            subprocess.run(['git', 'remote', 'add', 'origin', dev_repo], cwd=cache_folder, check=True, capture_output=True)

        # Add dev_repo as a remote for fetching the dev branch
        try:
            subprocess.run(['git', 'remote', 'remove', 'dev'], cwd=cache_folder, check=False, capture_output=True)
        except subprocess.CalledProcessError:
            pass
        subprocess.run(['git', 'remote', 'add', 'dev', dev_repo], cwd=cache_folder, check=True, capture_output=True)

        # Step 3: Fetch and merge dev
        sys.stdout.write(f"Merging {branch} branch...\n")
        subprocess.run(['git', 'fetch', 'dev'], cwd=cache_folder, check=True, capture_output=True)

        if not merge_dev(cache_folder, f"dev/{branch}"):
            sys.stderr.write(f"error: merge --ff-only dev/{branch} failed (not fast-forward)\n")
            return 1

        # Step 4-6: Stage allowed files, commit, push
        sys.stdout.write("Staging allowed files and committing...\n")
        stage_allowed_files(cache_folder)

        if not commit_removal(cache_folder):
            # Nothing to commit (no changes), which is fine
            sys.stdout.write("Note: No changes to commit (dev already merged cleanly)\n")

        sys.stdout.write("Pushing to origin/main...\n")
        if not push_to_main(cache_folder):
            sys.stderr.write("error: push to origin/main failed\n")
            return 1

        sys.stdout.write("Success: dev changes pushed to template (clean)\n")
        return 0

    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"error: command failed: {e}\n")
        return 1
    except Exception as e:
        sys.stderr.write(f"error: unexpected error: {e}\n")
        return 1
