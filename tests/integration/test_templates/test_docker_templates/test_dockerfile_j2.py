import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture
def dockerfile_template(env):
    return env.get_template("Dockerfile.j2")


def test_dockerfile_template_exists(docker_template_dir):
    """Test that the Dockerfile template exists."""
    assert (docker_template_dir / "Dockerfile.j2").exists()


def test_dockerfile_renders_with_default_values(dockerfile_template):
    """Test that the Dockerfile template renders with default values."""
    context = {"python_version": "3.9", "expose_port": 8000, "app_module": "main"}
    rendered = dockerfile_template.render(**context)

    assert "FROM python:3.9" in rendered
    assert "EXPOSE 8000" in rendered
    assert (
        'CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]' in rendered
    )


def test_dockerfile_renders_with_custom_values(dockerfile_template):
    """Test that the Dockerfile template renders with custom values."""
    context = {
        "python_version": "3.10-slim",
        "expose_port": 9000,
        "app_module": "api.main",
    }
    rendered = dockerfile_template.render(**context)

    assert "FROM python:3.10-slim" in rendered
    assert "EXPOSE 9000" in rendered
    assert (
        'CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "9000"]'
        in rendered
    )
