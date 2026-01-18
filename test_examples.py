#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyyaml>=6.0",
#     "click>=8.0",
# ]
# ///
"""Simple test examples demonstrating URL transformations.

This script shows how the redirect generator transforms Jupyter Book v1
URLs to MyST/Jupyter Book v2 URLs, including edge cases.

Run with: uv run test_examples.py
"""

import unittest

from generate_redirects import generate_redirect_html_content, sanitize_for_myst_url


class TestURLTransformations(unittest.TestCase):
    """Test URL sanitization against various edge cases."""

    def test_basic_file(self):
        result = sanitize_for_myst_url("overview")
        self.assertEqual(result, "overview")

    def test_underscores_to_hyphens(self):
        result = sanitize_for_myst_url("Test_File")
        self.assertEqual(result, "test-file")

    def test_mixed_case_to_lowercase(self):
        result = sanitize_for_myst_url("TestMixedCase")
        self.assertEqual(result, "testmixedcase")

    def test_spaces_to_hyphens(self):
        result = sanitize_for_myst_url("Test With Spaces")
        self.assertEqual(result, "test-with-spaces")

    def test_strip_leading_underscore(self):
        result = sanitize_for_myst_url("_LeadingUnderscore")
        self.assertEqual(result, "leadingunderscore")

    def test_collapse_multiple_hyphens(self):
        result = sanitize_for_myst_url("Multiple___Special")
        self.assertEqual(result, "multiple-special")

    def test_nested_directory(self):
        result = sanitize_for_myst_url("charters/MediaStrategy")
        self.assertEqual(result, "charters/mediastrategy")

    def test_nested_with_underscores(self):
        result = sanitize_for_myst_url("nested/Test_File")
        self.assertEqual(result, "nested/test-file")


class TestRedirectHTML(unittest.TestCase):
    """Test HTML redirect generation."""

    def test_redirect_html_content(self):
        url = "https://example.com/overview/"
        html = generate_redirect_html_content(url)

        self.assertIn('meta http-equiv="refresh"', html)
        self.assertIn(f"url={url}", html)
        self.assertIn(f'href="{url}"', html)
        self.assertIn(url, html)

    def test_redirect_html_structure(self):
        html = generate_redirect_html_content("https://example.com/test/")

        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("<title>Redirecting...</title>", html)


if __name__ == "__main__":
    unittest.main()
