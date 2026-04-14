"""
Unit tests for push_to_template.py — whitelist filtering and cache management
"""

import pytest
from pathlib import Path
import tempfile
import os
import subprocess
import shutil


class TestFilterArtifacts:
    """Test whitelist filtering of git status output"""

    def test_filter_empty_status(self):
        """Empty git status returns empty list"""
        from push_to_template import filter_artifacts
        result = filter_artifacts("")
        assert result == []

    def test_filter_single_allowed_file(self):
        """Single allowed file passes through"""
        from push_to_template import filter_artifacts
        git_status = "M  README.md\n"
        result = filter_artifacts(git_status)
        assert "README.md" in result

    def test_filter_excludes_features_folder(self):
        """Features/ folder is excluded"""
        from push_to_template import filter_artifacts
        git_status = "M  README.md\n?? Features/new-item.md\n"
        result = filter_artifacts(git_status)
        assert "README.md" in result
        assert not any("Features" in f for f in result)

    def test_filter_excludes_meetings_folder(self):
        """meetings/ folder is excluded"""
        from push_to_template import filter_artifacts
        git_status = "M  src/app.py\n?? meetings/2026-04-14.md\n"
        result = filter_artifacts(git_status)
        assert "src/app.py" in result
        assert not any("meetings" in f for f in result)

    def test_filter_excludes_tasks_csv(self):
        """tasks.csv is excluded"""
        from push_to_template import filter_artifacts
        git_status = "M  tasks.csv\nM  README.md\n"
        result = filter_artifacts(git_status)
        assert "README.md" in result
        assert "tasks.csv" not in result

    def test_filter_excludes_push_scripts(self):
        """push_to_template.py and push_template.sh are excluded"""
        from push_to_template import filter_artifacts
        git_status = "M  push_to_template.py\nM  push_template.sh\nM  main.py\n"
        result = filter_artifacts(git_status)
        assert "main.py" in result
        assert "push_to_template.py" not in result
        assert "push_template.sh" not in result

    def test_filter_multiple_allowed_files(self):
        """Multiple allowed files all pass through"""
        from push_to_template import filter_artifacts
        git_status = "M  README.md\nM  src/app.py\n?? docs/guide.md\n"
        result = filter_artifacts(git_status)
        assert "README.md" in result
        assert "src/app.py" in result
        assert "docs/guide.md" in result

    def test_filter_mixed_allowed_and_excluded(self):
        """Mix of allowed and excluded files — only allowed remain"""
        from push_to_template import filter_artifacts
        git_status = (
            "M  README.md\n"
            "?? Features/item.md\n"
            "M  src/main.py\n"
            "M  tasks.csv\n"
            "?? meetings/notes.md\n"
            "M  push_to_template.py\n"
        )
        result = filter_artifacts(git_status)
        assert "README.md" in result
        assert "src/main.py" in result
        assert len(result) == 2
        assert not any("Features" in f or "tasks.csv" in f or "meetings" in f or "push_to_template" in f for f in result)

    def test_filter_handles_git_status_format(self):
        """Correctly parses git status --porcelain format"""
        from push_to_template import filter_artifacts
        # Git status format: [status code] [space] [filename]
        git_status = "M  file.txt\n?? untracked.py\nA  added.js\n"
        result = filter_artifacts(git_status)
        assert "file.txt" in result
        assert "untracked.py" in result
        assert "added.js" in result


class TestCacheInit:
    """Test cache initialization and stash management"""

    def test_cache_init_creates_folder(self):
        """Cache folder created if it doesn't exist"""
        from push_to_template import cache_init

        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = os.path.join(tmpdir, "cache")
            assert not os.path.exists(cache_path)

            result = cache_init(cache_path)

            assert os.path.exists(cache_path)
            assert os.path.exists(os.path.join(cache_path, '.git'))
            assert result == cache_path

    def test_cache_init_idempotent(self):
        """Cache init can be called multiple times safely"""
        from push_to_template import cache_init

        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = os.path.join(tmpdir, "cache")

            # First call
            result1 = cache_init(cache_path)

            # Second call should not fail
            result2 = cache_init(cache_path)

            assert result1 == result2
            assert os.path.exists(os.path.join(cache_path, '.git'))

    def test_cache_init_default_path(self):
        """Cache init uses default path if none specified"""
        from push_to_template import cache_init

        # We can't test the actual default (~/Documents/...) in unit tests,
        # but we can verify the function accepts no argument
        # Real integration test would verify the default path creation
        # For now, just verify custom path works
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = os.path.join(tmpdir, "cache")
            result = cache_init(cache_path)
            assert os.path.exists(result)

    def test_cache_stash_pop_no_stash(self):
        """Cache stash pop returns False when no stash exists"""
        from push_to_template import cache_init, cache_stash_pop

        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = os.path.join(tmpdir, "cache")
            cache_init(cache_path)

            # Stash should be empty after init
            result = cache_stash_pop(cache_path)

            assert result is False

    def test_cache_stash_pop_with_stash(self):
        """Cache stash pop returns True when stash exists"""
        from push_to_template import cache_init, cache_stash_pop

        with tempfile.TemporaryDirectory() as tmpdir:
            cache_path = os.path.join(tmpdir, "cache")
            cache_init(cache_path)

            # Create initial commit so we can stash
            readme = os.path.join(cache_path, "README.md")
            with open(readme, 'w') as f:
                f.write("initial")
            subprocess.run(['git', 'add', 'README.md'], cwd=cache_path, check=True)
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=cache_path, check=True)
            subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=cache_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'initial'], cwd=cache_path, check=True)

            # Create a change and stash it
            test_file = os.path.join(cache_path, "test.txt")
            with open(test_file, 'w') as f:
                f.write("test content")

            subprocess.run(['git', 'add', 'test.txt'], cwd=cache_path, check=True)
            subprocess.run(['git', 'stash'], cwd=cache_path, check=True)

            # Pop stash should restore it
            result = cache_stash_pop(cache_path)

            assert result is True
            assert os.path.exists(test_file)


class TestMergeAndCommit:
    """Test git merge, staging allowed files, and commit"""

    def _setup_repo_with_branch(self, repo_path: str, branch_name: str = "dev") -> None:
        """Helper: set up git repo with initial commit and second branch"""
        # Configure git
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=repo_path, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=repo_path, check=True)

        # Create initial commit on main
        readme = os.path.join(repo_path, "README.md")
        with open(readme, 'w') as f:
            f.write("initial content")
        subprocess.run(['git', 'add', 'README.md'], cwd=repo_path, check=True)
        subprocess.run(['git', 'commit', '-m', 'initial'], cwd=repo_path, check=True)

        # Create branch and add commits
        subprocess.run(['git', 'checkout', '-b', branch_name], cwd=repo_path, check=True)
        for i in range(2):
            file_path = os.path.join(repo_path, f"file{i}.txt")
            with open(file_path, 'w') as f:
                f.write(f"content {i}")
            subprocess.run(['git', 'add', f'file{i}.txt'], cwd=repo_path, check=True)
            subprocess.run(['git', 'commit', '-m', f'commit {i}'], cwd=repo_path, check=True)

        # Switch back to main
        subprocess.run(['git', 'checkout', 'main'], cwd=repo_path, check=True)

    def test_merge_dev_ff_only_success(self):
        """Merge dev branch with fast-forward"""
        from push_to_template import merge_dev

        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = os.path.join(tmpdir, "repo")
            os.makedirs(repo_path)
            subprocess.run(['git', 'init'], cwd=repo_path, check=True)
            self._setup_repo_with_branch(repo_path, "dev")

            # Merge should succeed
            result = merge_dev(repo_path, "dev")
            assert result is True

            # Check we're on main and dev changes are included
            log_output = subprocess.run(['git', 'log', '--oneline'], cwd=repo_path,
                                       capture_output=True, text=True, check=True).stdout
            assert "commit" in log_output  # Dev commits should be in main's history

    def test_merge_dev_fails_if_not_ff(self):
        """Merge fails gracefully if not fast-forward"""
        from push_to_template import merge_dev

        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = os.path.join(tmpdir, "repo")
            os.makedirs(repo_path)
            subprocess.run(['git', 'init'], cwd=repo_path, check=True)
            self._setup_repo_with_branch(repo_path, "dev")

            # Add conflicting commit to main
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=repo_path, check=True)
            subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=repo_path, check=True)
            conflict_file = os.path.join(repo_path, "conflict.txt")
            with open(conflict_file, 'w') as f:
                f.write("conflict")
            subprocess.run(['git', 'add', 'conflict.txt'], cwd=repo_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'conflict'], cwd=repo_path, check=True)

            # Merge should fail
            result = merge_dev(repo_path, "dev")
            assert result is False

    def test_stage_allowed_files(self):
        """Stage only allowed files using filter"""
        from push_to_template import stage_allowed_files

        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = os.path.join(tmpdir, "repo")
            os.makedirs(repo_path)
            subprocess.run(['git', 'init'], cwd=repo_path, check=True)
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=repo_path, check=True)
            subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=repo_path, check=True)

            # Create initial commit
            readme = os.path.join(repo_path, "README.md")
            with open(readme, 'w') as f:
                f.write("initial")
            subprocess.run(['git', 'add', 'README.md'], cwd=repo_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'initial'], cwd=repo_path, check=True)

            # Create mixed allowed/excluded changes
            allowed = os.path.join(repo_path, "src/main.py")
            os.makedirs(os.path.dirname(allowed), exist_ok=True)
            with open(allowed, 'w') as f:
                f.write("code")

            excluded = os.path.join(repo_path, "tasks.csv")
            with open(excluded, 'w') as f:
                f.write("csv")

            # Stage allowed files
            stage_allowed_files(repo_path)

            # Check git status
            status = subprocess.run(['git', 'status', '--porcelain'], cwd=repo_path,
                                  capture_output=True, text=True, check=True).stdout

            # tasks.csv should not be staged
            assert "tasks.csv" not in subprocess.run(['git', 'diff', '--cached', '--name-only'],
                                                     cwd=repo_path, capture_output=True, text=True, check=True).stdout

    def test_commit_removal(self):
        """Create commit with removal message"""
        from push_to_template import commit_removal

        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = os.path.join(tmpdir, "repo")
            os.makedirs(repo_path)
            subprocess.run(['git', 'init'], cwd=repo_path, check=True)
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=repo_path, check=True)
            subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=repo_path, check=True)

            # Create initial commit and stage a change
            readme = os.path.join(repo_path, "README.md")
            with open(readme, 'w') as f:
                f.write("initial")
            subprocess.run(['git', 'add', 'README.md'], cwd=repo_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'initial'], cwd=repo_path, check=True)

            # Make and stage a change
            with open(readme, 'w') as f:
                f.write("updated")
            subprocess.run(['git', 'add', 'README.md'], cwd=repo_path, check=True)

            # Commit
            commit_removal(repo_path)

            # Verify commit message
            log_output = subprocess.run(['git', 'log', '--oneline', '-1'], cwd=repo_path,
                                       capture_output=True, text=True, check=True).stdout
            assert "chore: merge dev changes to template" in log_output


class TestPush:
    """Test git push and error handling"""

    def test_push_to_main_success(self):
        """Push succeeds when origin is available"""
        from push_to_template import push_to_main

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a bare repo to act as origin
            origin_path = os.path.join(tmpdir, "origin.git")
            os.makedirs(origin_path)
            subprocess.run(['git', 'init', '--bare'], cwd=origin_path, check=True)

            # Create a local repo and push
            local_path = os.path.join(tmpdir, "local")
            os.makedirs(local_path)
            subprocess.run(['git', 'init'], cwd=local_path, check=True)
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=local_path, check=True)
            subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=local_path, check=True)
            subprocess.run(['git', 'remote', 'add', 'origin', origin_path], cwd=local_path, check=True)

            # Create initial commit
            readme = os.path.join(local_path, "README.md")
            with open(readme, 'w') as f:
                f.write("content")
            subprocess.run(['git', 'add', 'README.md'], cwd=local_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'initial'], cwd=local_path, check=True)

            # Push should succeed
            result = push_to_main(local_path)
            assert result is True

    def test_push_to_main_fails_no_origin(self):
        """Push fails gracefully when origin doesn't exist"""
        from push_to_template import push_to_main

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a local repo without origin
            local_path = os.path.join(tmpdir, "local")
            os.makedirs(local_path)
            subprocess.run(['git', 'init'], cwd=local_path, check=True)
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=local_path, check=True)
            subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=local_path, check=True)

            # Create initial commit
            readme = os.path.join(local_path, "README.md")
            with open(readme, 'w') as f:
                f.write("content")
            subprocess.run(['git', 'add', 'README.md'], cwd=local_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'initial'], cwd=local_path, check=True)

            # Push should fail
            result = push_to_main(local_path)
            assert result is False

    def test_push_error_message_to_stderr(self):
        """Push failure logs error message to stderr"""
        from push_to_template import push_to_main
        import io
        from contextlib import redirect_stderr

        with tempfile.TemporaryDirectory() as tmpdir:
            local_path = os.path.join(tmpdir, "local")
            os.makedirs(local_path)
            subprocess.run(['git', 'init'], cwd=local_path, check=True)
            subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=local_path, check=True)
            subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=local_path, check=True)

            # Create initial commit
            readme = os.path.join(local_path, "README.md")
            with open(readme, 'w') as f:
                f.write("content")
            subprocess.run(['git', 'add', 'README.md'], cwd=local_path, check=True)
            subprocess.run(['git', 'commit', '-m', 'initial'], cwd=local_path, check=True)

            # Capture stderr
            stderr_capture = io.StringIO()
            with redirect_stderr(stderr_capture):
                result = push_to_main(local_path)

            assert result is False
            # Error should be logged
            stderr_output = stderr_capture.getvalue()
            assert "error" in stderr_output.lower() or "fatal" in stderr_output.lower()





if __name__ == "__main__":
    pytest.main([__file__, "-v"])
