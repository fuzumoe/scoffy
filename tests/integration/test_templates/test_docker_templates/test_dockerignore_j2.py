import logging
from pathlib import Path

import pytest
from jinja2 import Environment, Template

logger = logging.getLogger(__name__)


@pytest.fixture
def dockerignore_template(env: Environment) -> Template:
    return env.get_template(".dockerignore.j2")


def test_dockerignore_template_exists(docker_template_dir: Path) -> None:
    """Test that the .dockerignore template exists."""
    assert (docker_template_dir / ".dockerignore.j2").exists()


def test_dockerignore_renders(dockerignore_template: Template) -> None:
    """Test that the .dockerignore template renders correctly."""
    rendered = dockerignore_template.render()

    # Check for common Python ignore patterns
    assert "__pycache__/" in rendered
    assert "*.py[cod]" in rendered
    assert "*$py.class" in rendered

    # Check for packaging and distribution ignores
    assert "build/" in rendered
    assert "dist/" in rendered
    assert "*.egg-info/" in rendered

    # Check for test and coverage ignores
    assert ".pytest_cache/" in rendered
    assert ".coverage" in rendered

    # Check for virtual environment ignores
    assert "venv/" in rendered
    assert "env/" in rendered
    assert "ENV/" in rendered

    # Check for Docker-related ignores
    assert "Dockerfile" in rendered
    assert "docker-compose.yml" in rendered
    assert ".dockerignore" in rendered
