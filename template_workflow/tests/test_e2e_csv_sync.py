"""
End-to-end tests for CSV sync scripts.
Tests run against a real git repo in test_area/ with real filesystem operations.
"""

import csv
from pathlib import Path
import subprocess
import pytest


def test_folders_to_csv_generates_csv(test_area, story_helper, run):
    """S1: folders_to_csv generates correct tasks.csv from Features/ structure."""
    # Place 2 story files in different columns
    story_helper("1-Backlog", "0001-feature-a.md", "0001", "Feature A")
    story_helper("2-HLD", "0002-feature-b-HLD.md", "0002", "Feature B HLD")

    # Run folders_to_csv.py
    rc, stdout, stderr = run("folders_to_csv")

    # Assert script succeeded
    assert rc == 0, f"Script failed: {stderr}"
    assert "Rebuilt" in stderr and "2 tasks" in stderr

    # Assert tasks.csv was created and has correct data
    csv_path = test_area / "tasks.csv"
    assert csv_path.exists(), "tasks.csv not created"

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 2
    assert rows[0]["id"] == "0001"
    assert rows[0]["column"] == "Backlog"
    assert rows[1]["id"] == "0002"
    assert rows[1]["column"] == "HLD"


def test_folders_to_csv_dry_run_prints_no_file(test_area, story_helper, run):
    """S2: folders_to_csv --dry-run prints to stdout, doesn't write file."""
    # Place a story file
    story_helper("4-Task", "0005-story.md", "0005", "Test Story")

    # Run with --dry-run
    rc, stdout, stderr = run("folders_to_csv", "--dry-run")

    # Assert script succeeded
    assert rc == 0

    # Assert CSV output to stdout
    assert "id,epic,feature,task,status,assignee,column,type,review_gate,path" in stdout
    assert "0005" in stdout

    # Assert no file was written
    csv_path = test_area / "tasks.csv"
    assert not csv_path.exists(), "tasks.csv should not be created with --dry-run"


def test_csv_to_folders_dry_run_shows_moves(test_area, story_helper, run):
    """S3: csv_to_folders --dry-run shows moves without touching files."""
    # Place a story file in 2-HLD
    story_helper("2-HLD", "0003-story.md", "0003", "Test Story")

    # Create tasks.csv saying the story should be in Task
    csv_path = test_area / "tasks.csv"
    csv_path.write_text("id,epic,feature,story,status,assignee,column,type,review_gate,path\n")
    csv_path.write_text(
        csv_path.read_text() + "0003,,,Test Story,backlog,test,Task,story,no,\n"
    )

    # Commit the CSV
    subprocess.run(["git", "add", "tasks.csv"], cwd=test_area, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add csv"], cwd=test_area, check=True, capture_output=True)

    # Run csv_to_folders with --dry-run
    rc, stdout, stderr = run("csv_to_folders", "--dry-run")

    assert rc == 0
    assert "Would move" in stdout

    # Assert file is still in 2-HLD (not moved)
    original_file = test_area / "Features" / "2-HLD" / "0003-story.md"
    assert original_file.exists(), "File should still be in 2-HLD after dry-run"

    target_file = test_area / "Features" / "4-Task" / "0003-story.md"
    assert not target_file.exists(), "File should not be in 4-Task after dry-run"


def test_csv_to_folders_moves_straggler(test_area, story_helper, run):
    """S4: csv_to_folders moves a straggler via git mv."""
    # Place a story file in 2-HLD
    story_helper("2-HLD", "0004-story.md", "0004", "Test Story")

    # Create tasks.csv saying it should be in 4-Task
    csv_path = test_area / "tasks.csv"
    csv_path.write_text("id,epic,feature,story,status,assignee,column,type,review_gate,path\n")
    csv_path.write_text(
        csv_path.read_text() + "0004,,,Test Story,backlog,test,Task,story,no,\n"
    )

    # Commit the CSV
    subprocess.run(["git", "add", "tasks.csv"], cwd=test_area, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add csv"], cwd=test_area, check=True, capture_output=True)

    # Run csv_to_folders (actual move)
    rc, stdout, stderr = run("csv_to_folders")

    assert rc == 0, f"Script failed: {stderr}"
    assert "Moved" in stdout and "0004-story.md" in stdout

    # Assert file moved to 4-Task
    target_file = test_area / "Features" / "4-Task" / "0004-story.md"
    assert target_file.exists(), "File should be in 4-Task after move"

    # Assert git status shows rename
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=test_area,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "R  Features/2-HLD" in result.stdout, f"git status didn't show rename:\n{result.stdout}"


def test_csv_to_folders_skips_correct_column(test_area, story_helper, run):
    """S5: csv_to_folders skips files already in correct column."""
    # Place a story in 4-Task
    story_helper("4-Task", "0006-story.md", "0006", "Test Story")

    # Create tasks.csv saying it's in Task (correct)
    csv_path = test_area / "tasks.csv"
    csv_path.write_text("id,epic,feature,story,status,assignee,column,type,review_gate,path\n")
    csv_path.write_text(
        csv_path.read_text() + "0006,,,Test Story,backlog,test,Task,story,no,\n"
    )

    # Commit the CSV
    subprocess.run(["git", "add", "tasks.csv"], cwd=test_area, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "add csv"], cwd=test_area, check=True, capture_output=True)

    # Run csv_to_folders
    rc, stdout, stderr = run("csv_to_folders")

    assert rc == 0
    assert "0 files moved" in stdout, f"Should have moved 0 files, but got:\n{stdout}"

    # File should still be in 4-Task (no rename in git)
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=test_area,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "R " not in result.stdout, f"Should have no renames:\n{result.stdout}"
