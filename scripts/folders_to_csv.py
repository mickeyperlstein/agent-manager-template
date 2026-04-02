#!/usr/bin/env python3
"""
folders_to_csv.py - Scan Features/ folder structure and rebuild tasks.csv from story file frontmatter.
Usage: python3 scripts/folders_to_csv.py > tasks.csv
"""

import os
import re
import csv
import sys
from pathlib import Path

# Map folder names to column values
COLUMN_MAP = {
    "1-Backlog": "Backlog",
    "2-HLD": "HLD",
    "3-TaskReview": "TaskReview",
    "4-InProgress": "InProgress",
    "5-Testing-Agent": "Testing-Agent",
    "6-Testing-Manual": "Testing-Manual",
    "7-Verified": "Verified",
    "8-Review": "Review",
    "9-Done": "Done",
}

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


def extract_story_from_filename(filepath: Path) -> str:
    """Extract story name from filename (e.g., 0001-agent-manager-repo.md -> agent-manager-repo)."""
    name = filepath.stem
    if '-' in name:
        parts = name.split('-', 1)
        return parts[1].replace('-', ' ')
    return name


def scan_features(features_dir: Path) -> list:
    """Scan Features/ directory and extract story data from all .md files."""
    stories = []
    
    for folder in features_dir.iterdir():
        if not folder.is_dir():
            continue
        
        column = COLUMN_MAP.get(folder.name)
        if not column:
            continue
        
        for md_file in folder.rglob('*.md'):
            content = md_file.read_text()
            fm = parse_frontmatter(content)
            
            if not fm or 'id' not in fm:
                continue
            
            story_name = extract_story_from_filename(md_file)
            rel_path = get_relative_path(features_dir, md_file, folder.name)
            
            stories.append({
                'id': fm.get('id', ''),
                'epic': fm.get('epic', ''),
                'feature': fm.get('feature', ''),
                'story': story_name,
                'status': fm.get('status', 'backlog'),
                'assignee': fm.get('assignee', ''),
                'column': column,
                'type': fm.get('type', 'story'),
                'review_gate': fm.get('review_gate', 'no'),
                'path': rel_path,
            })
    
    return sorted(stories, key=lambda x: x['id'])


def write_csv(stories: list, output_path: Path = None):
    """Write stories to CSV format."""
    fieldnames = ['id', 'epic', 'feature', 'story', 'status', 'assignee', 'column', 'type', 'review_gate', 'path']
    
    if output_path:
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(stories)
    else:
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stories)


def main():
    repo_root = Path(__file__).parent.parent
    features_dir = repo_root / 'Features'
    output_path = repo_root / 'tasks.csv'
    
    stories = scan_features(features_dir)
    write_csv(stories, output_path)
    print(f"Rebuilt {output_path} with {len(stories)} stories", file=sys.stderr)


if __name__ == '__main__':
    main()
