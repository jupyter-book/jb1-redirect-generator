# JB1 Redirect Generator

Generate HTML redirect files when migrating from Jupyter Book v1 to MyST/Jupyter Book v2.

## What This Does

When you migrate from Jupyter Book v1 to JB2/MyST, your URL structure changes:

- **Old (JB1):** `https://example.com/Overview Page.html`
- **New (JB2):** `https://example.com/overview-page/`

This tool generates HTML redirect files so old links continue to work.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (optional, but convenient for running the script directly)

If not running with `uv`:

- click
- pyyaml

## Usage

Build your site, then generate redirects:

```bash
# With Jupyter Book 2
jupyter book build --html 
uv run https://raw.githubusercontent.com/jupyter/governance/main/jb1-redirect-generator/generate_redirects.py \
  --base-url https://example.com/

# With MyST CLI
myst build --html
uv run https://raw.githubusercontent.com/jupyter/governance/main/jb1-redirect-generator/generate_redirects.py \
  --base-url https://example.com/
```

**Note:** The examples use `uv run` for convenience. You can also download the script and run it with `python generate_redirects.py` instead.

### Options

- `--base-url` (required): Base URL of your site
- `--output-dir`: Where to create redirect files (default: `_build/html`)
- `--myst-config`: Path to `myst.yml` (default: auto-discovers in `./` or `./docs/`)

## How It Works

1. Reads your `myst.yml` to find all content files
2. Generates old-style `.html` URLs based on assumptions from Jupyter Book 1 / Sphinx
3. Applies MyST's URL sanitization (lowercase, hyphens, etc.)
4. Creates redirect HTML files with meta-refresh tags

The redirect files are created in your build output directory, ready to deploy alongside your new site.

## GitHub Actions Example

Here's how to integrate redirect generation into your deployment workflow:

```yaml
name: deploy

on:
  push:
    branches:
    - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: 3.x

    - name: Install uv
      uses: astral-sh/setup-uv@v4

    - name: Install dependencies
      run: pip install jupyter-book

    - name: Build the Jupyter Book site
      run: cd docs && jupyter book build --html

    - name: Generate redirects
      run: |
        uv run https://raw.githubusercontent.com/jupyter-book/jb1-redirect-generator/main/generate_redirects.py \
          --base-url https://example.com/ \
          --output-dir docs/_build/html

    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./docs/_build/html
```

## Credits

Inspired by [Silas Santini's](https://github.com/pancakereport) work in the [data-8/textbook](https://github.com/data-8/textbook) repository.
