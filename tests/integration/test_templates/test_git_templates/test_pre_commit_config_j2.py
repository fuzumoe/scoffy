import logging
from pathlib import Path
from typing import Any

import pytest
from jinja2 import Template

logger = logging.getLogger(__name__)


@pytest.fixture
def pre_commit_template(env: Any) -> Any:
    """Return the pre-commit config template."""
    return env.get_template(".pre-commit-config.yaml.j2")


def test_pre_commit_template_exists(git_template_dir: Path) -> None:
    """Test that the .pre-commit-config.yaml template exists."""
    assert (git_template_dir / ".pre-commit-config.yaml.j2").exists()


def test_pre_commit_renders_with_default_values(pre_commit_template: Template) -> None:
    """Test that the .pre-commit-config.yaml template renders with default values."""
    context: dict[str, Any] = {}
    rendered: str = pre_commit_template.render(**context)

    assert "https://github.com/astral-sh/ruff-pre-commit" in rendered
    assert "rev: v0.1.8" in rendered
    assert "id: ruff" in rendered
    assert "id: ruff-format" in rendered
    assert "https://github.com/PyCQA/bandit" in rendered
    assert "rev: 1.7.5" in rendered
    assert "python3.12" in rendered


def test_pre_commit_renders_with_custom_versions(pre_commit_template: Template) -> None:
    """Test that the .pre-commit-config.yaml template renders with custom versions."""
    context: dict[str, str] = {
        "ruff_version": "0.2.0",
        "precommit_hooks_version": "5.0.0",
        "bandit_version": "2.0.0",
        "safety_version": "3.0.0",
        "python_version": "3.11",
    }
    rendered: str = pre_commit_template.render(**context)

    assert "rev: v0.2.0" in rendered
    assert "rev: v5.0.0" in rendered
    assert "rev: 2.0.0" in rendered
    assert "rev: 3.0.0" in rendered
    assert "python3.11" in rendered


def test_pre_commit_renders_with_mypy(pre_commit_template: Template) -> None:
    """Test that the .pre-commit-config.yaml template renders with MyPy."""
    context: dict[str, Any] = {"use_mypy": True, "mypy_version": "1.8.0"}
    rendered: str = pre_commit_template.render(**context)

    assert "https://github.com/pre-commit/mirrors-mypy" in rendered
    assert "rev: v1.8.0" in rendered
    assert "MyPy Type Checking" in rendered
    assert "additional_dependencies: [types-requests, types-PyYAML]" in rendered


def test_pre_commit_renders_without_mypy(pre_commit_template: Template) -> None:
    """Test that the .pre-commit-config.yaml template renders without MyPy."""
    context: dict[str, bool] = {"use_mypy": False}
    rendered: str = pre_commit_template.render(**context)

    assert "https://github.com/pre-commit/mirrors-mypy" not in rendered
    assert "MyPy Type Checking" not in rendered


def test_pre_commit_renders_with_coverage(pre_commit_template: Template) -> None:
    """Test that the .pre-commit-config.yaml template renders with coverage settings."""
    context: dict[str, Any] = {"generate_coverage": True, "min_coverage": "90"}
    rendered: str = pre_commit_template.render(**context)

    assert "--cov=app" in rendered
    assert "--cov-report=term-missing" in rendered
    assert "--cov-fail-under=90" in rendered


def test_pre_commit_renders_with_custom_test_settings(
    pre_commit_template: Template,
) -> None:
    """Test that the .pre-commit-config.yaml template renders with custom test settings."""
    context: dict[str, str] = {
        "test_runner": "python -m pytest",
        "max_test_failures": "5",
        "max_integration_failures": "3",
        "fail_fast": "true",
    }
    rendered: str = pre_commit_template.render(**context)

    assert "entry: python -m pytest" in rendered
    assert "--maxfail=5" in rendered
    assert "--maxfail=3" in rendered
    assert "fail_fast: true" in rendered
