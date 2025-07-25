import logging
from pathlib import Path
from typing import Any

import pytest
from jinja2 import Template

logger = logging.getLogger(__name__)


@pytest.fixture
def docker_compose_template(env: Any) -> Any:
    return env.get_template("docker-compose.yml.j2")


def test_docker_compose_template_exists(docker_template_dir: Path) -> None:
    """Test that the docker-compose.yml template exists."""
    assert (docker_template_dir / "docker-compose.yml.j2").exists()


def test_docker_compose_renders_with_default_values(
    docker_compose_template: Template,
) -> None:
    """Test that the docker-compose.yml template renders with default values."""
    context = {"app_name": "fastapi-app", "app_port": "8000"}
    rendered = docker_compose_template.render(**context)

    assert "container_name: fastapi-app" in rendered
    assert '"8000:8000"' in rendered
    assert "networks:" in rendered
    assert "fastapi-network:" in rendered


def test_docker_compose_renders_with_postgresql(
    docker_compose_template: Template,
) -> None:
    """Test that the docker-compose.yml template renders with PostgreSQL."""
    context = {
        "app_name": "my-api",
        "database_type": "postgresql",
        "db_user": "testuser",
        "db_password": "testpass",
        "db_name": "testdb",
    }
    rendered = docker_compose_template.render(**context)

    assert "container_name: my-api" in rendered
    assert "postgres:" in rendered
    assert "POSTGRES_USER=testuser" in rendered
    assert "POSTGRES_PASSWORD=testpass" in rendered
    assert "POSTGRES_DB=testdb" in rendered
    assert "postgres_data:" in rendered


def test_docker_compose_renders_with_mongodb(docker_compose_template: Template) -> None:
    """Test that the docker-compose.yml template renders with MongoDB."""
    context = {
        "app_name": "doc-api",
        "database_type": "document",
        "mongo_user": "mongouser",
        "mongo_password": "mongopass",
        "mongo_db_name": "mongodb",
    }
    rendered = docker_compose_template.render(**context)

    assert "container_name: doc-api" in rendered
    assert "mongodb:" in rendered
    assert "MONGO_INITDB_ROOT_USERNAME=mongouser" in rendered
    assert "MONGO_INITDB_ROOT_PASSWORD=mongopass" in rendered
    assert "MONGO_INITDB_DATABASE=mongodb" in rendered
    assert "mongodb_data:" in rendered


def test_docker_compose_renders_with_redis(docker_compose_template: Template) -> None:
    """Test that the docker-compose.yml template renders with Redis."""
    context = {
        "app_name": "cache-api",
        "use_redis": True,
        "redis_version": "6-alpine",
        "redis_password": "redispass",
    }
    rendered = docker_compose_template.render(**context)

    assert "container_name: cache-api" in rendered
    assert "redis:" in rendered
    assert "redis:6-alpine" in rendered
    assert "redis-server --requirepass redispass" in rendered
    assert "redis_data:" in rendered


def test_docker_compose_renders_with_nginx(docker_compose_template: Template) -> None:
    """Test that the docker-compose.yml template renders with Nginx."""
    context = {
        "app_name": "web-api",
        "use_nginx": True,
        "nginx_port": "8080",
        "nginx_ssl_port": "8443",
    }
    rendered = docker_compose_template.render(**context)

    assert "container_name: web-api" in rendered
    assert "nginx:" in rendered
    assert '"8080:80"' in rendered
    assert '"8443:443"' in rendered
