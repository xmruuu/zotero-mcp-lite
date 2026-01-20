"""
Tests for zotero_mcp.utils module.

Tests cover:
- format_creators: Creator name formatting
- clean_html: HTML tag removal
- text_to_html: Plain text to HTML conversion with detection
"""

import unittest

from zotero_mcp.utils import clean_html, format_creators, text_to_html


class TestFormatCreators(unittest.TestCase):
    """Tests for format_creators function."""

    def test_with_first_last_name(self):
        """Standard format with firstName and lastName."""
        creators = [
            {"firstName": "John", "lastName": "Smith"},
            {"firstName": "Jane", "lastName": "Doe"},
        ]
        result = format_creators(creators)
        self.assertEqual(result, "Smith, John; Doe, Jane")

    def test_with_single_name(self):
        """Institutional or single name format."""
        creators = [{"name": "World Health Organization"}]
        result = format_creators(creators)
        self.assertEqual(result, "World Health Organization")

    def test_mixed_formats(self):
        """Mix of individual and institutional names."""
        creators = [
            {"firstName": "John", "lastName": "Smith"},
            {"name": "Research Institute"},
        ]
        result = format_creators(creators)
        self.assertEqual(result, "Smith, John; Research Institute")

    def test_empty_list(self):
        """Empty creator list returns default message."""
        result = format_creators([])
        self.assertEqual(result, "No authors listed")

    def test_ignores_unknown_fields(self):
        """Entries without recognized fields are skipped."""
        creators = [
            {"firstName": "John", "lastName": "Smith"},
            {"unknown": "value"},  # Should be ignored
        ]
        result = format_creators(creators)
        self.assertEqual(result, "Smith, John")


class TestCleanHtml(unittest.TestCase):
    """Tests for clean_html function."""

    def test_removes_simple_tags(self):
        """Removes basic HTML tags."""
        result = clean_html("<p>Hello</p>")
        self.assertEqual(result, "Hello")

    def test_removes_nested_tags(self):
        """Removes nested HTML tags."""
        result = clean_html("<div><p>Hello <strong>world</strong>!</p></div>")
        self.assertEqual(result, "Hello world!")

    def test_preserves_plain_text(self):
        """Plain text without tags remains unchanged."""
        result = clean_html("Hello world")
        self.assertEqual(result, "Hello world")

    def test_empty_string(self):
        """Empty string returns empty string."""
        result = clean_html("")
        self.assertEqual(result, "")

    def test_removes_self_closing_tags(self):
        """Removes self-closing tags like <br/>."""
        result = clean_html("Line1<br/>Line2")
        self.assertEqual(result, "Line1Line2")


class TestTextToHtml(unittest.TestCase):
    """Tests for text_to_html function."""

    def test_single_paragraph(self):
        """Single paragraph wrapped in <p> tags."""
        result = text_to_html("Hello world")
        self.assertEqual(result, "<p>Hello world</p>")

    def test_multiple_paragraphs(self):
        """Double newlines create separate paragraphs."""
        result = text_to_html("First paragraph.\n\nSecond paragraph.")
        self.assertEqual(result, "<p>First paragraph.</p><p>Second paragraph.</p>")

    def test_single_newlines_become_br(self):
        """Single newlines become <br/> within paragraphs."""
        result = text_to_html("Line 1\nLine 2")
        self.assertEqual(result, "<p>Line 1<br/>Line 2</p>")

    def test_passthrough_existing_html_p(self):
        """Content with <p>...</p> structure passes through unchanged."""
        html = "<p>Already HTML</p>"
        result = text_to_html(html)
        self.assertEqual(result, html)

    def test_passthrough_existing_html_div(self):
        """Content with <div>...</div> structure passes through unchanged."""
        html = "<div>Content</div>"
        result = text_to_html(html)
        self.assertEqual(result, html)

    def test_passthrough_br_tag(self):
        """Content with <br/> passes through unchanged."""
        html = "Line 1<br/>Line 2"
        result = text_to_html(html)
        self.assertEqual(result, html)

    def test_plain_text_with_angle_brackets_not_html(self):
        """Plain text mentioning '<p>' is NOT treated as HTML structure."""
        # This tests the fix for false positives
        text = "I wrote <p> in my code"
        result = text_to_html(text)
        # Should be converted because '<p>' alone is not a complete tag structure
        self.assertTrue(result.startswith("<p>"))

    def test_empty_string(self):
        """Empty string returns single empty paragraph."""
        result = text_to_html("")
        self.assertEqual(result, "<p></p>")


if __name__ == "__main__":
    unittest.main()
