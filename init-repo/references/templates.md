# File Templates

All templates use these placeholders:
- `{project_name}` — kebab-case project name (e.g., `my-project`)
- `{package_name}` — snake_case Python package name (e.g., `my_project`)
- `{description}` — one-sentence project description

---

## pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{project_name}"
version = "0.1.0"
description = "{description}"
requires-python = ">=3.11"
license = "MIT"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.8",
    "mypy>=1.13",
]

[tool.hatch.build.targets.wheel]
packages = ["src/{package_name}"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "A", "C4", "SIM"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
```

---

## src/{package_name}/__init__.py

```python
"""{project_name}: {description}"""

__version__ = "0.1.0"

__all__: list[str] = []
```

---

## src/{package_name}/py.typed

Empty file. PEP 561 marker for mypy to recognize the package as typed.

---

## tests/conftest.py

```python
"""Shared test fixtures."""
```

---

## tests/test_{package_name}.py

```python
"""Tests for {package_name}."""

from {package_name} import __version__


def test_version() -> None:
    """Package version is set."""
    assert __version__ == "0.1.0"
```

---

## .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv python install ${{ matrix.python-version }}
      - run: uv sync --python ${{ matrix.python-version }}
      - run: uv run ruff check .
      - run: uv run mypy src/
      - run: uv run pytest
```

---

## .gitignore

```
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.egg-info/
dist/
build/

# Virtual environments
.venv/
venv/

# Tool caches
.pytest_cache/
.ruff_cache/
.mypy_cache/

# Environment and secrets
.env
.env.local

# Data directories
data/

# OS
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo
```

---

## README.md

```markdown
# {project_name}

{description}

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
uv run mypy src/
```
```

Minimal. Real documentation evolves with the project.

---

## CLAUDE.md

This template provides the structure. Substitute placeholders and adapt the Architecture section if the user provides domain context.

```markdown
# {project_name}

{description}

## Architecture

- **Build system:** hatchling (pyproject.toml)
- **Package manager:** uv
- **Source layout:** src/{package_name}/
- **Tests:** tests/

## Development Commands

Always use `uv run` to execute tools:

```bash
uv sync                    # Install dependencies
uv run pytest              # Run tests
uv run ruff check .        # Lint
uv run ruff format .       # Format
uv run mypy src/           # Type check
```

## Principles

- Fail loud over silent failure
- Explicit declarations over inference
- Testing is mandatory critical infrastructure
- Type safety enforced via mypy strict mode

## Governance

Documentation governance (ADRs, CICs, contributor protocols) will be initialized separately.
The docs/ directory is prepared for this.
```

---

## .gitkeep files

`docs/.gitkeep` and `scripts/.gitkeep` are empty files. They exist solely to track otherwise-empty directories in git.
