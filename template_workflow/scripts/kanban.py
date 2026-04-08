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
