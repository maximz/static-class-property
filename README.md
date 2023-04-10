# Static Class Property

[![](https://img.shields.io/pypi/v/static_class_property.svg)](https://pypi.python.org/pypi/static_class_property)
[![CI](https://github.com/maximz/static-class-property/actions/workflows/ci.yaml/badge.svg?branch=master)](https://github.com/maximz/static-class-property/actions/workflows/ci.yaml)
[![](https://img.shields.io/badge/docs-here-blue.svg)](https://static-class-property.maximz.com)
[![](https://img.shields.io/github/stars/maximz/static-class-property?style=social)](https://github.com/maximz/static-class-property)

## TODOs: Configuring this template

Create a Netlify site for your repository, then turn off automatic builds in Netlify settings.

Add these CI secrets: `PYPI_API_TOKEN`, `NETLIFY_AUTH_TOKEN` (Netlify user settings - personal access tokens), `DEV_NETLIFY_SITE_ID`, `PROD_NETLIFY_SITE_ID` (API ID from Netlify site settings)

Set up Codecov at TODO

## Overview

## Installation

```bash
pip install static_class_property
```

## Usage

## Development

Submit PRs against `develop` branch, then make a release pull request to `master`.

```bash
# Optional: set up a pyenv virtualenv
pyenv virtualenv 3.9 static_class_property-3.9
echo "static_class_property-3.9" > .python-version
pyenv version

# Install requirements
pip install --upgrade pip wheel
pip install -r requirements_dev.txt

# Install local package
pip install -e .

# Install pre-commit
pre-commit install

# Run tests
make test

# Run lint
make lint

# bump version before submitting a PR against master (all master commits are deployed)
bump2version patch # possible: major / minor / patch

# also ensure CHANGELOG.md updated
```
