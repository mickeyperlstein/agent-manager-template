#!/usr/bin/env python3
"""
csv_to_folders.py - Read tasks.csv and move task files to correct column folders.
Usage: python3 scripts/csv_to_folders.py [--dry-run]
"""

import csv
import subprocess
import sys
from pathlib import Path
from kanban import COLUMNS, repo_root, parse_filename


def find_task_file(features_dir: Path, task_id: str) -> Path:
    """
    Find a task file by parsing filename and matching taskid.

    Searches all .md files and uses parse_filename() to extract the taskid,
    which correctly handles task names with hyphens. Falls back to matching
    the leading segment of 2-segment filenames ({taskid}-{name}.md), the
    legacy naming convention still present alongside 4-segment files.
    """
    for folder in features_dir.iterdir():
        if not folder.is_dir():
            continue
        for md_file in folder.rglob('*.md'):
            try:
                _, parsed_taskid, _, _ = parse_filename(md_file)
                if parsed_taskid == task_id:
                    return md_file
            except ValueError:
                stem = md_file.stem
                if '-' in stem and stem.split('-', 1)[0] == task_id:
                    print(f"Exception: Found task file: {md_file} that is legacy format")
                    return md_file
                continue
    return None


def get_column_from_path(features_dir: Path, file_path: Path) -> str:
    """Extract column name from file path by finding the numbered folder."""
    try:
        rel_parts = file_path.relative_to(features_dir).parts
        if len(rel_parts) > 0:
            folder_name = rel_parts[0]
            return folder_name.split('-', 1)[1] if '-' in folder_name else folder_name
    except ValueError:
        pass
    return ''


def move_task(features_dir: Path, task_id: str, target_column: str, path: str = '', dry_run: bool = False) -> bool:
    """Move a task file to the correct folder using git mv. Returns True if moved."""
    target_folder = COLUMNS.get(target_column)
    if not target_folder:
        print(f"Error: Unknown column '{target_column}' for task {task_id}", file=sys.stderr)
        return False

    current_file = find_task_file(features_dir, task_id)
    target_dir = features_dir / target_folder

    if not target_dir.exists():
        print(f"Error: Target folder '{target_folder}' does not exist", file=sys.stderr)
        return False

    if current_file is None:
        # Task in CSV but no file exists - this is a "create" case
        print(f"Task {task_id} not found on disk (would create in {target_folder})", file=sys.stderr)
        return False

    current_column = get_column_from_path(features_dir, current_file)

    if current_column == target_column:
        return False  # Already in correct folder

    # Move file to target folder
    # Build target path including subdirectory
    if path:
        target_dir = target_dir / path
        target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / current_file.name

    if dry_run:
        print(f"Would move: {current_file.relative_to(features_dir.parent)} -> {target_file.relative_to(features_dir.parent)}")
        return True

    # Check for name collision
    if target_file.exists():
        print(f"Error: File already exists at {target_file}", file=sys.stderr)
        return False

    # Use git mv to keep version control
    try:
        subprocess.run(['git', 'mv', str(current_file), str(target_file)], check=True, capture_output=True)
        print(f"Moved: {current_file.name} -> {target_folder}/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error moving {current_file.name}: {e.stderr.decode()}", file=sys.stderr)
        return False


def sync_csv_to_folders(csv_path: Path, features_dir: Path, dry_run: bool = False):
    """Read CSV and move all tasks to their target folders."""
    moves = 0

    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            task_id = row.get('id', '').strip()
            target_column = row.get('column', '').strip()

            task_path = row.get('path', '').strip()

            if not task_id or not target_column:
                continue

            if move_task(features_dir, task_id, target_column, task_path, dry_run):
                moves += 1

    return moves


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Sync tasks.csv to Features/ folder structure (move task files to columns)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    args = parser.parse_args()

    # Use cwd if Features/ exists there, otherwise use repo_root
    cwd = Path.cwd()
    if (cwd / 'Features').exists():
        csv_path = cwd / 'tasks.csv'
        features_dir = cwd / 'Features'
    else:
        root = repo_root()
        csv_path = root / 'tasks.csv'
        features_dir = root / 'Features'
    
    if not csv_path.exists():
        print(f"Error: {csv_path} not found", file=sys.stderr)
        sys.exit(1)
    
    if not features_dir.exists():
        print(f"Error: {features_dir} not found", file=sys.stderr)
        sys.exit(1)
    
    moves = sync_csv_to_folders(csv_path, features_dir, dry_run=args.dry_run)
    
    if args.dry_run:
        print(f"\nDry run: {moves} files would be moved")
    else:
        print(f"\nDone: {moves} files moved")


if __name__ == '__main__':
    main()
