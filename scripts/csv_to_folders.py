#!/usr/bin/env python3
"""
csv_to_folders.py - Read tasks.csv and move story files to correct column folders.
Usage: python3 scripts/csv_to_folders.py
"""

import csv
import shutil
import sys
from pathlib import Path

# Map column values to folder names
COLUMN_TO_FOLDER = {
    "Backlog": "1-Backlog",
    "HLD": "2-HLD",
    "TaskReview": "3-TaskReview",
    "InProgress": "4-InProgress",
    "Testing-Agent": "5-Testing-Agent",
    "Testing-Manual": "6-Testing-Manual",
    "Verified": "7-Verified",
    "Review": "8-Review",
    "Done": "9-Done",
}


def find_story_file(features_dir: Path, story_id: str) -> Path:
    """Find a story file by ID anywhere in Features/."""
    for folder in features_dir.iterdir():
        if not folder.is_dir():
            continue
        for md_file in folder.rglob('*.md'):
            if md_file.stem.startswith(f"{story_id}-"):
                return md_file
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


def move_story(features_dir: Path, story_id: str, target_column: str, path: str = '', dry_run: bool = False) -> bool:
    """Move a story file to the correct folder. Returns True if moved."""
    target_folder = COLUMN_TO_FOLDER.get(target_column)
    if not target_folder:
        print(f"Error: Unknown column '{target_column}' for story {story_id}", file=sys.stderr)
        return False
    
    current_file = find_story_file(features_dir, story_id)
    target_dir = features_dir / target_folder
    
    if not target_dir.exists():
        print(f"Error: Target folder '{target_folder}' does not exist", file=sys.stderr)
        return False
    
    if current_file is None:
        # Story in CSV but no file exists - this is a "create" case
        print(f"Story {story_id} not found on disk (would create in {target_folder})", file=sys.stderr)
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
    
    shutil.move(str(current_file), str(target_file))
    print(f"Moved: {current_file.name} -> {target_folder}/")
    return True


def sync_csv_to_folders(csv_path: Path, features_dir: Path, dry_run: bool = False):
    """Read CSV and move all stories to their target folders."""
    moves = 0
    
    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            story_id = row.get('id', '').strip()
            target_column = row.get('column', '').strip()
            
            story_path = row.get('path', '').strip()
            
            if not story_id or not target_column:
                continue
            
            if move_story(features_dir, story_id, target_column, story_path, dry_run):
                moves += 1
    
    return moves


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Sync tasks.csv to Features/ folder structure')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    args = parser.parse_args()
    
    repo_root = Path(__file__).parent.parent
    csv_path = repo_root / 'tasks.csv'
    features_dir = repo_root / 'Features'
    
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
