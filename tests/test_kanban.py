"""
Unit tests for kanban.py filename parsing

Tests the parse_filename() function which extracts task/feature/epic IDs
from kanban filenames in format: {name}-{taskid}-{featureid}-{epicid}.md
"""

import pytest
from pathlib import Path
from template_workflow.scripts.kanban import parse_filename


class TestParseFilenameBasic:
    """Test basic filename parsing without hyphens in task name"""

    def test_parse_simple_name(self):
        """Simple name without hyphens should parse correctly"""
        result = parse_filename("task-123-456-789.md")
        assert result == ("task", "123", "456", "789")

    def test_parse_simple_name_path(self):
        """Path object should be handled correctly"""
        result = parse_filename(Path("task-123-456-789.md"))
        assert result == ("task", "123", "456", "789")

    def test_with_md_extension(self):
        """Should handle .md extension gracefully (stem removes it)"""
        result = parse_filename("task-123-456-789.md")
        assert result == ("task", "123", "456", "789")

    def test_without_md_extension(self):
        """Should also handle filenames without extension"""
        result = parse_filename("task-123-456-789")
        assert result == ("task", "123", "456", "789")


class TestParseFilenameHyphenated:
    """Test parsing with hyphens in task names"""

    def test_parse_hyphenated_name(self):
        """Hyphenated task name should be preserved"""
        result = parse_filename("example-1-is-the-best-123-456-789.md")
        assert result == ("example-1-is-the-best", "123", "456", "789")

    def test_parse_two_hyphens_in_name(self):
        """Task name with exactly two hyphens"""
        result = parse_filename("my-task-name-123-456-789.md")
        assert result == ("my-task-name", "123", "456", "789")

    def test_parse_many_hyphens(self):
        """Task name with many hyphens"""
        result = parse_filename("a-b-c-d-e-f-123-456-789.md")
        assert result == ("a-b-c-d-e-f", "123", "456", "789")

    def test_parse_single_char_hyphens(self):
        """Each segment separated by hyphen"""
        result = parse_filename("x-y-z-123-456-789.md")
        assert result == ("x-y-z", "123", "456", "789")


class TestParseFilenameErrors:
    """Test error cases and validation"""

    def test_invalid_format_missing_ids(self):
        """Filename with too few segments should raise ValueError"""
        with pytest.raises(ValueError, match="Invalid filename format"):
            parse_filename("my-task.md")

    def test_invalid_format_only_two_segments(self):
        """Only two segments (name-id) should fail"""
        with pytest.raises(ValueError, match="Invalid filename format"):
            parse_filename("my-task-123.md")

    def test_invalid_format_only_three_segments(self):
        """Filename with only 3 segments (2 hyphens) should fail"""
        with pytest.raises(ValueError, match="Invalid filename format"):
            parse_filename("task-123-456.md")

    def test_empty_id_segment_taskid(self):
        """Empty taskid segment should raise ValueError"""
        with pytest.raises(ValueError, match="Invalid taskid.*cannot be empty"):
            parse_filename("task--456-789.md")

    def test_empty_id_segment_featureid(self):
        """Empty featureid segment should raise ValueError"""
        with pytest.raises(ValueError, match="Invalid featureid.*cannot be empty"):
            parse_filename("task-123--789.md")

    def test_empty_id_segment_epicid(self):
        """Empty epicid segment should raise ValueError"""
        with pytest.raises(ValueError, match="Invalid epicid.*cannot be empty"):
            parse_filename("task-123-456-.md")

    def test_invalid_format_too_many_segments(self):
        """More than 4 segments from rsplit means something is wrong"""
        # Actually, rsplit with maxsplit=3 will never produce >4 parts
        # This test verifies the logic handles edge cases
        result = parse_filename("a-b-c-d-e-123-456-789.md")
        assert result == ("a-b-c-d-e", "123", "456", "789")

    def test_single_name_with_ids(self):
        """Single character name with valid IDs"""
        result = parse_filename("x-123-456-789.md")
        assert result == ("x", "123", "456", "789")


class TestParseFilenameOpaqueIDs:
    """Test that IDs can be any non-empty string (opaque tokens)"""

    def test_ids_with_mixed_case(self):
        """IDs can contain uppercase and lowercase"""
        result = parse_filename("task-AbCd-EfGh-IjKl.md")
        assert result == ("task", "AbCd", "EfGh", "IjKl")

    def test_ids_with_numbers_and_letters(self):
        """IDs can be alphanumeric"""
        result = parse_filename("task-8f40-478d-83d1.md")
        assert result == ("task", "8f40", "478d", "83d1")

    def test_ids_special_characters_allowed(self):
        """IDs can contain special characters (not validated)"""
        result = parse_filename("task-a$b-c@d-e!f.md")
        assert result == ("task", "a$b", "c@d", "e!f")

    def test_ids_spaces_not_allowed(self):
        """Spaces are allowed in task names (not delimiters)"""
        # Spaces are not hyphens, so they're preserved in the task name
        result = parse_filename("task-a b-123-456-789.md")
        assert result == ("task-a b", "123", "456", "789")


class TestParseFilenameRoundTrip:
    """Test round-trip: parse -> extract -> reconstruct"""

    def test_roundtrip_hyphenated_name(self):
        """Parse hyphenated name and reconstruct filename"""
        original = "my-task-is-great-123-456-789.md"
        name, taskid, featureid, epicid = parse_filename(original)

        # Verify components
        assert name == "my-task-is-great"
        assert taskid == "123"
        assert featureid == "456"
        assert epicid == "789"

        # Reconstruct
        reconstructed = f"{name}-{taskid}-{featureid}-{epicid}.md"
        assert reconstructed == original

    def test_roundtrip_simple_name(self):
        """Parse simple name and reconstruct"""
        original = "task-123-456-789.md"
        name, taskid, featureid, epicid = parse_filename(original)
        reconstructed = f"{name}-{taskid}-{featureid}-{epicid}.md"
        assert reconstructed == original

    def test_roundtrip_many_hyphens(self):
        """Parse name with many hyphens and reconstruct"""
        original = "a-b-c-d-e-f-123-456-789.md"
        name, taskid, featureid, epicid = parse_filename(original)
        reconstructed = f"{name}-{taskid}-{featureid}-{epicid}.md"
        assert reconstructed == original


class TestParseFilenamePathHandling:
    """Test handling of different path formats"""

    def test_absolute_path(self):
        """Should extract filename from absolute path"""
        result = parse_filename(Path("/home/user/Features/4-Task/task-123-456-789.md"))
        assert result == ("task", "123", "456", "789")

    def test_relative_path(self):
        """Should extract filename from relative path"""
        result = parse_filename(Path("Features/4-Task/task-123-456-789.md"))
        assert result == ("task", "123", "456", "789")

    def test_nested_path_with_hyphens(self):
        """Should extract only the filename, ignoring path hyphens"""
        result = parse_filename(Path("Features/4-Task/my-epic/task-123-456-789.md"))
        assert result == ("task", "123", "456", "789")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
