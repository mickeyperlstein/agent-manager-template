"""
Pytest fixtures for E2E CSV sync tests.
Tests run against a real git repo in test_area/.
"""

import shutil
import subprocess
import sys
from pathlib import Path
import pytest

# Import kanban constants
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from kanban import COLUMNS


@pytest.fixture(autouse=True)
def clean_test_area():
    """
    Reset test_area/ to a clean git repo before each test.
    Creates Features/ column structure and initializes git.
    """
    root = Path(__file__).parent.parent.parent / "test_area"

    # Wipe and reinit
    if root.exists():
        shutil.rmtree(root)
    root.mkdir()

    # Create Features/ columns from shared COLUMNS dict
    for col_name, col_folder in COLUMNS.items():
        (root / "Features" / col_folder).mkdir(parents=True)

    # Initialize git repo
    subprocess.run(
        ["git", "init"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=root,
        check=True,
        capture_output=True,
    )

    # Create initial commit so git mv works
    (root / ".gitkeep").touch()
    subprocess.run(
        ["git", "add", "."],
        cwd=root,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=root,
        check=True,
        capture_output=True,
    )

    yield root

    # Cleanup after test
    if root.exists():
        shutil.rmtree(root)


@pytest.fixture
def test_area(clean_test_area):
    """Provide the test_area path for a test."""
    return clean_test_area


def write_story(test_area: Path, column: str, filename: str, story_id: str, title: str):
    """Helper to write a story .md file and commit it."""
    col_path = test_area / "Features" / column
    file_path = col_path / filename
    file_path.write_text(
        f"---\nid: \"{story_id}\"\ntitle: {title}\nstatus: backlog\nassignee: test\n---\n"
    )
    subprocess.run(
        ["git", "add", str(file_path)],
        cwd=test_area,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "commit", "-m", f"add {filename}"],
        cwd=test_area,
        check=True,
        capture_output=True,
    )
    return file_path


@pytest.fixture
def story_helper(test_area):
    """Provide a helper to write story files."""
    return lambda col, filename, sid, title: write_story(test_area, col, filename, sid, title)


def run_script(test_area: Path, script_name: str, *args):
    """
    Run a script in test_area and return (returncode, stdout, stderr).
    """
    script_path = (
        Path(__file__).parent.parent / "scripts" / f"{script_name}.py"
    ).resolve()
    cmd = ["python3", str(script_path)] + list(args)
    result = subprocess.run(
        cmd,
        cwd=test_area,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


@pytest.fixture
def run(test_area):
    """Provide a helper to run scripts."""
    return lambda script, *args: run_script(test_area, script, *args)
