import json
import logging
import re
from pathlib import Path
from typing import Any

import pytest
from jinja2 import Template

logger = logging.getLogger(__name__)


@pytest.fixture
def settings_json_template(env: Any) -> Any:
    return env.get_template("settings.json.j2")


def strip_json_comments(json_string: str) -> str:
    """Remove // comments from JSON string."""
    # Remove lines that are purely comments
    lines = json_string.split("\n")
    cleaned_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("//"):
            # Remove inline comments
            if "//" in line:
                line = line[: line.index("//")]
            cleaned_lines.append(line)

    # Join lines and fix common JSON issues
    cleaned_json = "\n".join(cleaned_lines)

    # Remove trailing commas
    cleaned_json = re.sub(r",(\s*[}\]])", r"\1", cleaned_json)

    # Remove any ellipsis that might have been inserted
    cleaned_json = re.sub(r"(\.{3,}|…)", "", cleaned_json)

    # Remove any control characters
    cleaned_json = "".join(
        char for char in cleaned_json if ord(char) >= 32 or char in "\n\r\t"
    )

    return cleaned_json


def test_settings_json_template_exists(vscode_template_dir: Path) -> None:
    """Test that the settings.json template exists."""
    assert (vscode_template_dir / "settings.json.j2").exists()


def test_settings_json_renders_with_default_values(
    settings_json_template: Template,
) -> None:
    """Test that the settings.json template renders with default values."""

    context: dict[str, Any] = {}
    rendered = settings_json_template.render(**context)
    cleaned_json = strip_json_comments(rendered)

    # Check that it's valid JSON
    json_data = json.loads(cleaned_json)
    assert "recommendations" in json_data
    assert "unwantedRecommendations" in json_data
    assert "ms-python.python" in json_data["recommendations"]


def test_settings_json_with_custom_values(settings_json_template: Template) -> None:
    """Test that the settings.json template renders with custom values."""

    context: dict[str, Any] = {
        "type_checking_mode": "strict",
        "line_length": 100,
        "use_mypy": True,
        "auto_save_delay": 2000,
        "default_shell": "zsh",
    }
    rendered = settings_json_template.render(**context)
    cleaned_json = strip_json_comments(rendered)
    json_data = json.loads(cleaned_json)

    # Check mypy extension is included when use_mypy is True
    assert "ms-python.mypy-type-checker" in json_data["recommendations"]


def test_settings_json_database_configurations(
    settings_json_template: Template,
) -> None:
    """Test that the settings.json template renders correctly with different database types."""

    # Test PostgreSQL configuration
    postgres_context: dict[str, str] = {
        "database_type": "postgresql",
    }
    rendered = settings_json_template.render(**postgres_context)
    cleaned_json = strip_json_comments(rendered)
    json_data = json.loads(cleaned_json)

    # Check that PostgreSQL extensions are included
    assert "cweijan.vscode-postgresql-client2" in json_data["recommendations"]
    assert "mtxr.sqltools" in json_data["recommendations"]
    assert "mtxr.sqltools-driver-pg" in json_data["recommendations"]

    # Test MongoDB configuration
    mongo_context: dict[str, str] = {
        "database_type": "mongodb",
    }
    rendered = settings_json_template.render(**mongo_context)
    cleaned_json = strip_json_comments(rendered)
    json_data = json.loads(cleaned_json)

    # Check that MongoDB extensions are included
    assert "mongodb.mongodb-vscode" in json_data["recommendations"]


def test_settings_json_redis_configuration(settings_json_template: Template) -> None:
    """Test that the settings.json template renders correctly with Redis configuration."""

    context: dict[str, bool] = {"use_redis": True}
    rendered = settings_json_template.render(**context)
    cleaned_json = strip_json_comments(rendered)
    json_data = json.loads(cleaned_json)

    # Check that Redis client is included
    assert "cweijan.vscode-redis-client" in json_data["recommendations"]


def test_settings_json_is_valid_vscode_configuration(
    settings_json_template: Template,
) -> None:
    """Test that the settings.json template produces a valid VS Code configuration."""

    rendered = settings_json_template.render()
    cleaned_json = strip_json_comments(rendered)
    json_data = json.loads(cleaned_json)

    # Check essential sections
    assert "recommendations" in json_data
    assert "unwantedRecommendations" in json_data
    assert "ms-python.flake8" in json_data["unwantedRecommendations"]
