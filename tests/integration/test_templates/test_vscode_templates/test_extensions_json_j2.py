import logging
from pathlib import Path
from typing import Any

import pytest
from jinja2 import Environment, Template

logger = logging.getLogger(__name__)


@pytest.fixture
def extensions_json_template(env: Environment) -> Template:
    return env.get_template("extensions.json.j2")


def test_extensions_json_template_exists(vscode_template_dir: Path) -> None:
    """Test that the extensions.json template exists."""
    assert (vscode_template_dir / "extensions.json.j2").exists()


def test_extensions_json_renders_with_default_values(
    extensions_json_template: Template,
) -> None:
    """Test that the extensions.json template renders with default values."""
    context: dict[str, Any] = {}
    rendered: str = extensions_json_template.render(**context)

    assert "recommendations" in rendered
    assert "{" in rendered
    assert "}" in rendered


def test_extensions_json_renders_with_python_extensions(
    extensions_json_template: Template,
) -> None:
    """Test that the extensions.json template renders with Python extensions."""
    context: dict[str, str] = {"language": "python"}
    rendered: str = extensions_json_template.render(**context)

    assert "ms-python.python" in rendered
    # The template uses ms-python.pylint and ms-python.debugpy instead of vscode-pylance
    assert "ms-python.pylint" in rendered
    assert "ms-python.debugpy" in rendered


def test_extensions_json_renders_with_javascript_extensions(
    extensions_json_template: Template,
) -> None:
    """Test that the extensions.json template renders with JavaScript extensions."""
    context: dict[str, str] = {"language": "javascript"}
    rendered: str = extensions_json_template.render(**context)

    # The template includes these JavaScript-related extensions
    assert "esbenp.prettier-vscode" in rendered
    assert "ms-vscode.vscode-typescript-next" in rendered


def test_extensions_json_renders_with_docker_extensions(
    extensions_json_template: Template,
) -> None:
    """Test that the extensions.json template renders with Docker extensions."""
    context: dict[str, bool] = {"use_docker": True}
    rendered: str = extensions_json_template.render(**context)

    assert "ms-azuretools.vscode-docker" in rendered


def test_extensions_json_renders_with_database_extensions(
    extensions_json_template: Template,
) -> None:
    """Test that the extensions.json template renders with database extensions."""
    context: dict[str, str] = {"database_type": "postgresql"}
    rendered: str = extensions_json_template.render(**context)

    # The template uses different PostgreSQL extension names
    assert "cweijan.vscode-postgresql-client2" in rendered
    assert "mtxr.sqltools-driver-pg" in rendered

    # Test MongoDB extensions
    context = {"database_type": "mongodb"}
    rendered = extensions_json_template.render(**context)

    assert "mongodb.mongodb-vscode" in rendered


def test_extensions_json_renders_with_git_extensions(
    extensions_json_template: Template,
) -> None:
    """Test that the extensions.json template renders with Git extensions."""
    context: dict[str, bool] = {"use_git": True}
    rendered: str = extensions_json_template.render(**context)

    assert "eamodio.gitlens" in rendered


def test_extensions_json_renders_with_multiple_features(
    extensions_json_template: Template,
) -> None:
    """Test that the extensions.json template renders with multiple features."""
    context: dict[str, Any] = {
        "language": "python",
        "use_docker": True,
        "database_type": "postgresql",
        "use_git": True,
    }
    rendered: str = extensions_json_template.render(**context)

    assert "ms-python.python" in rendered
    assert "ms-azuretools.vscode-docker" in rendered
    # Update to use the extension ID that's actually in the template
    assert "cweijan.vscode-postgresql-client2" in rendered
    assert "eamodio.gitlens" in rendered
