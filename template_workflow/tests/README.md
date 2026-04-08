# CSV Sync Tests

End-to-end tests for the CSV sync scripts (`folders_to_csv.py` and `csv_to_folders.py`).

Tests run against a real git repo in `test_area/` with actual filesystem operations.

## Requirements

```bash
pip install pytest
```

Or use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows
pip install pytest
```

## Running Tests

From the repo root:

```bash
python -m pytest template_workflow/tests/ -v
```

Or from `test_area/`:

```bash
cd test_area
python -m pytest ../template_workflow/tests/ -v
```

## Test Scenarios

- **S1:** `folders_to_csv` generates correct `tasks.csv` from folder structure
- **S2:** `folders_to_csv --dry-run` prints to stdout, doesn't write file
- **S3:** `csv_to_folders --dry-run` shows moves without touching files
- **S4:** `csv_to_folders` moves stragglers via `git mv`
- **S5:** `csv_to_folders` skips files already in correct column

Each test creates a real git repo in `test_area/`, sets up files, runs the script, and asserts on observable outcomes (filesystem state, git status, stdout/stderr).
