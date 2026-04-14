#!/usr/bin/env python3
"""
Shared Kanban constants for CSV sync scripts.
Single source of truth for column mappings.
"""

from pathlib import Path

# Map column names to folder paths
COLUMNS = {
    "Backlog":        "1-Backlog",
    "HLD":            "2-HLD",
    "HLD-Review":     "3-HLD-Review",
    "Task":           "4-Task",
    "TaskReview":     "5-TaskReview",
    "Implementation": "6-Implementation",
    "Test":           "7-Test",
    "Review":         "8-Review",
    "Done":           "9-Done",
}

# Reverse map: folder name → column name
FOLDER_TO_COLUMN = {v: k for k, v in COLUMNS.items()}


def repo_root() -> Path:
    """Return the project root directory."""
    return Path(__file__).parent.parent.parent


def parse_filename(filepath) -> tuple[str, str, str, str]:
    """
    Parse kanban filename in format {name}-{taskid}-{featureid}-{epicid}.md

    Extracts task metadata from the filename by splitting from the right,
    preserving hyphens in the task name. IDs are opaque tokens (may be hashes,
    random values, SSH ciphers, etc.) — not validated for format.

    Args:
        filepath: Path object or filename string (with or without .md extension)

    Returns:
        Tuple of (name, taskid, featureid, epicid) where:
        - name: task name (may contain hyphens)
        - taskid: task ID (opaque 4-char token)
        - featureid: feature ID (opaque 4-char token)
        - epicid: epic ID (opaque 4-char token)

    Raises:
        ValueError: If filename doesn't match expected format (missing segments)
                   or if any ID segment is empty

    Examples:
        >>> parse_filename("my-task-123-456-789.md")
        ("my-task", "123", "456", "789")

        >>> parse_filename("task-8f40-478d-83d1.md")
        ("task", "8f40", "478d", "83d1")

        >>> parse_filename(Path("Features/4-Task/example-1-is-the-best-123-456-789.md"))
        ("example-1-is-the-best", "123", "456", "789")
    """
    # Step 1: Get filename without extension
    filename = Path(filepath).stem

    # Step 2: Split from RIGHT by '-' with maxsplit=3
    # This keeps hyphens in the task name intact
    parts = filename.rsplit('-', 3)

    if len(parts) != 4:
        raise ValueError(f"Invalid filename format: {filename}")

    name, taskid, featureid, epicid = parts

    # Step 3: Validate IDs are non-empty
    # IDs are opaque tokens (hashes, random, SSH cipher outputs) — no format enforcement
    for id_val, id_name in [(taskid, 'taskid'), (featureid, 'featureid'), (epicid, 'epicid')]:
        if not id_val:
            raise ValueError(f"Invalid {id_name}: cannot be empty")

    return (name, taskid, featureid, epicid)
