import logging
from pathlib import Path
from typing import Any

import pytest
from jinja2 import Environment, Template

logger = logging.getLogger(__name__)


@pytest.fixture
def gitignore_template(env: Environment) -> Template:
    """Return the gitignore template."""
    return env.get_template(".gitignore.j2")


def test_gitignore_template_exists(git_template_dir: Path) -> None:
    """Test that the .gitignore.j2 template exists."""
    assert (git_template_dir / ".gitignore.j2").exists()


def test_gitignore_renders_with_default_values(gitignore_template: Template) -> None:
    """Test that the .gitignore template renders with default values."""
    context: dict[str, Any] = {}
    rendered: str = gitignore_template.render(**context)

    # Check common Python ignores
    assert "__pycache__/" in rendered
    assert "*.py[cod]" in rendered
    assert "*.so" in rendered
    assert "dist/" in rendered
    assert "*.egg-info/" in rendered

    # Check default environment files
    assert ".env.local" in rendered
    assert ".env.development" in rendered
    assert ".env.production" in rendered

    # Check default directories
    assert "static/" in rendered
    assert "media/" in rendered


def test_gitignore_renders_with_custom_environment_files(
    gitignore_template: Template,
) -> None:
    """Test that the .gitignore template renders with custom environment files."""
    context: dict[str, list[str]] = {
        "environment_files": [".custom-env", "config/.secrets", ".env.custom"]
    }
    rendered: str = gitignore_template.render(**context)

    # Check custom environment files
    assert ".custom-env" in rendered
    assert "config/.secrets" in rendered
    assert ".env.custom" in rendered

    # Ensure default environment files are not included when custom ones are provided
    assert ".env.local" not in rendered
    assert ".env.development" not in rendered


def test_gitignore_renders_with_custom_uploads(gitignore_template: Template) -> None:
    """Test that the .gitignore template renders with custom upload directory."""
    context: dict[str, Any] = {"use_uploads": True, "upload_dir": "custom_uploads/"}
    rendered: str = gitignore_template.render(**context)

    assert "custom_uploads/" in rendered


def test_gitignore_renders_with_sqlite_database(gitignore_template: Template) -> None:
    """Test that the .gitignore template renders with SQLite database settings."""
    context: dict[str, str] = {"database_type": "sqlite", "db_name": "custom.db"}
    rendered: str = gitignore_template.render(**context)

    assert "*.db" in rendered
    assert "*.sqlite" in rendered
    assert "*.sqlite3" in rendered
    assert "custom.db" in rendered


def test_gitignore_renders_with_alembic(gitignore_template: Template) -> None:
    """Test that the .gitignore template renders with Alembic settings."""
    context: dict[str, bool] = {"use_alembic": True}
    rendered: str = gitignore_template.render(**context)

    assert "# alembic/versions/*.py" in rendered


def test_gitignore_renders_with_custom_logs(gitignore_template: Template) -> None:
    """Test that the .gitignore template renders with custom log files."""
    context: dict[str, str] = {
        "log_file": "custom.log",
        "error_log": "custom_error.log",
    }
    rendered: str = gitignore_template.render(**context)

    assert "custom.log" in rendered
    assert "custom_error.log" in rendered


def test_gitignore_renders_with_docker(gitignore_template: Template) -> None:
    """Test that the .gitignore template renders with Docker settings."""
    context: dict[str, bool] = {"use_docker": True}
    rendered: str = gitignore_template.render(**context)

    assert ".dockerignore" in rendered


def test_gitignore_renders_with_celery(gitignore_template: Template) -> None:
    """Test that the .gitignore template renders with Celery settings."""
    context: dict[str, bool] = {"use_celery": True}
    rendered: str = gitignore_template.render(**context)

    assert "celerybeat-schedule" in rendered
    assert "celerybeat.pid" in rendered


def test_gitignore_renders_with_redis(gitignore_template: Template) -> None:
    """Test that the .gitignore template renders with Redis settings."""
    context: dict[str, bool] = {"use_redis": True}
    rendered: str = gitignore_template.render(**context)

    assert "dump.rdb" in rendered


def test_gitignore_renders_with_frontend(gitignore_template: Template) -> None:
    """Test that the .gitignore template renders with frontend settings."""
    context: dict[str, bool] = {"use_frontend": True}
    rendered: str = gitignore_template.render(**context)

    assert "node_modules/" in rendered
    assert "npm-debug.log*" in rendered
    assert "yarn-debug.log*" in rendered


def test_gitignore_renders_with_custom_ignores(gitignore_template: Template) -> None:
    """Test that the .gitignore template renders with custom ignores."""
    context: dict[str, list[str]] = {
        "custom_ignores": ["*.custom", "generated/", "secret_tokens.txt"]
    }
    rendered: str = gitignore_template.render(**context)

    assert "*.custom" in rendered
    assert "generated/" in rendered
    assert "secret_tokens.txt" in rendered
