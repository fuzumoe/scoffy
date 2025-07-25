import logging
from pathlib import Path
from typing import Any

import pytest
from jinja2 import Environment, FileSystemLoader, Template

logger = logging.getLogger(__name__)


@pytest.fixture
def env(code_quality_template_dir: Path) -> Environment:
    """Return a Jinja2 environment for the code quality templates."""
    return Environment(loader=FileSystemLoader(code_quality_template_dir))


@pytest.fixture
def ruff_template(env: Environment) -> Template:
    """Return the ruff.toml template."""
    return env.get_template("ruff.toml.j2")


def test_ruff_template_exists(code_quality_template_dir: Path) -> None:
    """Test that the ruff.toml template exists."""
    assert (code_quality_template_dir / "ruff.toml.j2").exists()


def test_ruff_toml_renders_with_default_values(ruff_template: Template) -> None:
    """Test that the ruff.toml template renders with default values."""
    context: dict[str, str] = {"project_name": "Test Project"}
    rendered: str = ruff_template.render(**context)

    assert "# Ruff Configuration for Test Project" in rendered
    assert 'target-version = "py3.12"' in rendered
    assert "line-length = 88" in rendered
    assert 'quote-style = "double"' in rendered
    assert 'known-first-party = ["app", "tests"]' in rendered


def test_ruff_toml_renders_with_custom_values(ruff_template: Template) -> None:
    """Test that the ruff.toml template renders with custom values."""
    context: dict[str, Any] = {
        "project_name": "Custom Project",
        "python_version": "3.11",
        "line_length": 100,
        "app_name": "custom_app",
        "additional_rules": ["D", "PT"],
        "ignore_rules": ["F401", "E231"],
        "exclude_dirs": ["temp", "scripts"],
        "use_pydantic": True,
        "docstring_convention": "numpy",
        "per_file_ignores": {"custom_file.py": ["E501", "F403"]},
    }
    rendered: str = ruff_template.render(**context)

    assert "# Ruff Configuration for Custom Project" in rendered
    assert 'target-version = "py3.11"' in rendered
    assert "line-length = 100" in rendered
    assert '"D",' in rendered
    assert '"PT",' in rendered
    assert '"F401",' in rendered
    assert '"E231",' in rendered
    assert '"temp",' in rendered
    assert '"scripts",' in rendered
    assert 'known-first-party = ["custom_app", "tests"]' in rendered
    assert 'convention = "numpy"' in rendered
    assert '"custom_file.py" = ["E501", "F403"]' in rendered


def test_ruff_toml_renders_with_mccabe_and_pylint_config(
    ruff_template: Template,
) -> None:
    """Test that the ruff.toml template renders with mccabe and pylint configurations."""
    context: dict[str, dict[str, int]] = {
        "mccabe": {"max_complexity": 15},
        "pylint": {"max_args": 8, "max_returns": 5},
    }
    rendered: str = ruff_template.render(**context)

    assert "max-complexity = 15" in rendered
    assert "max-args = 8" in rendered
    assert "max-returns = 5" in rendered
