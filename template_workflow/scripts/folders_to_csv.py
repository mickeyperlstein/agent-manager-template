#!/usr/bin/env python3
"""
folders_to_csv.py - Scan Features/ folder structure and rebuild tasks.csv from task file frontmatter.
Usage: python3 scripts/folders_to_csv.py [--dry-run]
"""

import os
import re
import csv
import sys
from pathlib import Path
from kanban import FOLDER_TO_COLUMN, repo_root, parse_filename

FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return {}
    
    frontmatter = match.group(1)
    result = {}
    
    for line in frontmatter.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            result[key] = value
    
    return result


def get_relative_path(features_dir: Path, md_file: Path, column_folder: str) -> str:
    """Get path relative to column folder (e.g., 'devops-bootstrap/stories')."""
    column_path = features_dir / column_folder
    try:
        rel = md_file.parent.relative_to(column_path)
        return str(rel) if str(rel) != '.' else ''
    except ValueError:
        return ''


def extract_task_from_filename(filepath: Path) -> str:
    """
    Extract task name from filename using parse_filename().

    Handles both 4-segment format (with epicid/featureid) and 2-segment format.
    Preserves hyphens in task name for round-trip CSV consistency.
    Examples:
    - my-task-123-456-789.md (4-seg) -> my-task
    - my-task-123.md (2-seg) -> my-task
    """
    try:
        name, _, _, _ = parse_filename(filepath)
        return name
    except ValueError:
        # Fallback for 2-segment filenames (common format: {id}-{name})
        # Split on first hyphen and extract the name part (preserving hyphens)
        stem = filepath.stem
        if '-' in stem:
            parts = stem.split('-', 1)
            return parts[1]  # Return name part (2nd segment after ID)
        return stem


def scan_features(features_dir: Path) -> list:
    """Scan Features/ directory and extract task data from all .md files."""
    tasks = []

    for folder in features_dir.iterdir():
        if not folder.is_dir():
            continue

        column = FOLDER_TO_COLUMN.get(folder.name)
        if not column:
            continue

        for md_file in folder.rglob('*.md'):
            content = md_file.read_text()
            fm = parse_frontmatter(content)

            if not fm or 'id' not in fm:
                continue
            
            task_name = extract_task_from_filename(md_file)
            rel_path = get_relative_path(features_dir, md_file, folder.name)

            tasks.append({
                'id': fm.get('id', ''),
                'epic': fm.get('epic', ''),
                'feature': fm.get('feature', ''),
                'task': task_name,
                'status': fm.get('status', 'backlog'),
                'assignee': fm.get('assignee', ''),
                'column': column,
                'type': fm.get('type', 'task'),
                'review_gate': fm.get('review_gate', 'no'),
                'path': rel_path,
            })

    return sorted(tasks, key=lambda x: x['id'])


def write_csv(stories: list, output_path: Path = None, dry_run: bool = False):
    """Write tasks to CSV format. If dry_run, always output to stdout."""
    fieldnames = ['id', 'epic', 'feature', 'task', 'status', 'assignee', 'column', 'type', 'review_gate', 'path']

    if dry_run or output_path is None:
        # Always print to stdout in dry-run or when no output path specified
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stories)
    else:
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(stories)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Scan Features/ and rebuild tasks.csv')
    parser.add_argument('--dry-run', action='store_true', help='Print CSV to stdout instead of writing file')
    args = parser.parse_args()

    # Use cwd if Features/ exists there, otherwise use repo_root
    cwd = Path.cwd()
    if (cwd / 'Features').exists():
        features_dir = cwd / 'Features'
        output_path = cwd / 'tasks.csv'
    else:
        root = repo_root()
        features_dir = root / 'Features'
        output_path = root / 'tasks.csv'

    tasks = scan_features(features_dir)
    write_csv(tasks, output_path, dry_run=args.dry_run)

    if not args.dry_run:
        print(f"Rebuilt {output_path} with {len(tasks)} tasks", file=sys.stderr)


if __name__ == '__main__':
    main()
