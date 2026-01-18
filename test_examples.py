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

from generate_redirects import generate_redirect_html_content, sanitize_for_myst_url


def print_line():
    print("=" * 80)


def test_url_transformations():
    """Test URL sanitization against various edge cases."""

    test_cases = [
        # (input_file, expected_slug, description)
        ("overview.md", "overview", "Basic file"),
        ("Test_File.md", "test-file", "Underscores to hyphens"),
        ("TestMixedCase.md", "testmixedcase", "Mixed case to lowercase"),
        ("Test With Spaces.md", "test-with-spaces", "Spaces to hyphens"),
        ("_LeadingUnderscore.md", "leadingunderscore", "Strip leading underscore"),
        ("Multiple___Special.md", "multiple-special", "Collapse multiple hyphens"),
        ("charters/MediaStrategy.md", "charters/mediastrategy", "Nested directory"),
        ("nested/Test_File.md", "nested/test-file", "Nested with underscores"),
    ]

    print("Testing URL transformations:")
    print_line()

    all_passed = True
    for input_file, expected_slug, description in test_cases:
        # Remove extension to simulate file path processing
        input_path = input_file.replace(".md", "")
        result = sanitize_for_myst_url(input_path)

        passed = result == expected_slug
        status = "✓" if passed else "✗"

        if passed:
            print(f"{status} {description:30} | {input_file:30} → /{result}/")
        else:
            print(
                f"{status} {description:30} | {input_file:30} → /{result}/ (expected: /{expected_slug}/)"
            )
            all_passed = False

    print_line()

    if all_passed:
        print("✨ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


def test_redirect_html_example():
    """Show example of generated redirect HTML."""

    print("\nExample redirect HTML for 'overview.html':")
    print_line()

    html = generate_redirect_html_content("https://example.com/overview/")
    print(html)
    print_line()


if __name__ == "__main__":
    import sys

    exit_code = test_url_transformations()
    test_redirect_html_example()

    sys.exit(exit_code)
