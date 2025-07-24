import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture
def gitignore_template(env):
    """Return the gitignore template."""
    return env.get_template(".gitignore.j2")


def test_gitignore_template_exists(git_template_dir):
    """Test that the .gitignore.j2 template exists."""
    assert (git_template_dir / ".gitignore.j2").exists()


def test_gitignore_renders_with_default_values(gitignore_template):
    """Test that the .gitignore template renders with default values."""
    context = {}
    rendered = gitignore_template.render(**context)

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


def test_gitignore_renders_with_custom_environment_files(gitignore_template):
    """Test that the .gitignore template renders with custom environment files."""
    context = {"environment_files": [".custom-env", "config/.secrets", ".env.custom"]}
    rendered = gitignore_template.render(**context)

    # Check custom environment files
    assert ".custom-env" in rendered
    assert "config/.secrets" in rendered
    assert ".env.custom" in rendered

    # Ensure default environment files are not included when custom ones are provided
    assert ".env.local" not in rendered
    assert ".env.development" not in rendered


def test_gitignore_renders_with_custom_uploads(gitignore_template):
    """Test that the .gitignore template renders with custom upload directory."""
    context = {"use_uploads": True, "upload_dir": "custom_uploads/"}
    rendered = gitignore_template.render(**context)

    assert "custom_uploads/" in rendered


def test_gitignore_renders_with_sqlite_database(gitignore_template):
    """Test that the .gitignore template renders with SQLite database settings."""
    context = {"database_type": "sqlite", "db_name": "custom.db"}
    rendered = gitignore_template.render(**context)

    assert "*.db" in rendered
    assert "*.sqlite" in rendered
    assert "*.sqlite3" in rendered
    assert "custom.db" in rendered


def test_gitignore_renders_with_alembic(gitignore_template):
    """Test that the .gitignore template renders with Alembic settings."""
    context = {"use_alembic": True}
    rendered = gitignore_template.render(**context)

    assert "# alembic/versions/*.py" in rendered


def test_gitignore_renders_with_custom_logs(gitignore_template):
    """Test that the .gitignore template renders with custom log files."""
    context = {"log_file": "custom.log", "error_log": "custom_error.log"}
    rendered = gitignore_template.render(**context)

    assert "custom.log" in rendered
    assert "custom_error.log" in rendered


def test_gitignore_renders_with_docker(gitignore_template):
    """Test that the .gitignore template renders with Docker settings."""
    context = {"use_docker": True}
    rendered = gitignore_template.render(**context)

    assert ".dockerignore" in rendered


def test_gitignore_renders_with_celery(gitignore_template):
    """Test that the .gitignore template renders with Celery settings."""
    context = {"use_celery": True}
    rendered = gitignore_template.render(**context)

    assert "celerybeat-schedule" in rendered
    assert "celerybeat.pid" in rendered


def test_gitignore_renders_with_redis(gitignore_template):
    """Test that the .gitignore template renders with Redis settings."""
    context = {"use_redis": True}
    rendered = gitignore_template.render(**context)

    assert "dump.rdb" in rendered


def test_gitignore_renders_with_frontend(gitignore_template):
    """Test that the .gitignore template renders with frontend settings."""
    context = {"use_frontend": True}
    rendered = gitignore_template.render(**context)

    assert "node_modules/" in rendered
    assert "npm-debug.log*" in rendered
    assert "yarn-debug.log*" in rendered


def test_gitignore_renders_with_custom_ignores(gitignore_template):
    """Test that the .gitignore template renders with custom ignores."""
    context = {"custom_ignores": ["*.custom", "generated/", "secret_tokens.txt"]}
    rendered = gitignore_template.render(**context)

    assert "*.custom" in rendered
    assert "generated/" in rendered
    assert "secret_tokens.txt" in rendered
