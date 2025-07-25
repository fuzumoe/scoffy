import json
import logging
from pathlib import Path
from typing import Any

import pytest
from jinja2 import Template

logger = logging.getLogger(__name__)


@pytest.fixture
def launch_json_template(env: Any) -> Any:
    return env.get_template("launch.json.j2")


def test_launch_json_template_exists(vscode_template_dir: Path) -> None:
    """Test that the launch.json template exists."""
    assert (vscode_template_dir / "launch.json.j2").exists()


def test_launch_json_renders_with_default_values(
    launch_json_template: Template,
) -> None:
    """Test that the launch.json template renders with default values."""

    context: dict[str, Any] = {}
    rendered: str = launch_json_template.render(**context)

    assert "configurations" in rendered
    # Check that it's valid JSON
    json_data: dict[str, Any] = json.loads(rendered)
    assert json_data["version"] == "0.2.0"
    assert "configurations" in json_data
    assert isinstance(json_data["configurations"], list)


def test_launch_json_configurations_content(launch_json_template: Template) -> None:
    """Test that the launch.json configurations have expected structure."""

    rendered: str = launch_json_template.render()
    json_data: dict[str, Any] = json.loads(rendered)

    for config in json_data["configurations"]:
        assert "name" in config
        assert "type" in config
        assert "request" in config


def test_launch_json_with_custom_values(launch_json_template: Template) -> None:
    """Test that the launch.json template renders with custom values."""

    context: dict[str, Any] = {"python_path": "/custom/python/path", "debug_port": 9999}
    rendered: str = launch_json_template.render(**context)
    json_data: dict[str, Any] = json.loads(rendered)

    assert json_data["version"] == "0.2.0"

    # Check that custom values are properly used in configurations
    for config in json_data["configurations"]:
        if "python" in config.get("type", ""):
            assert "/custom/python/path" in str(config)
        if "attach" in config.get("request", "") and "port" in config:
            assert config["port"] == 9999


def test_launch_json_is_valid_vscode_configuration(
    launch_json_template: Template,
) -> None:
    """Test that the launch.json template produces a valid VS Code debug configuration."""

    rendered: str = launch_json_template.render()
    json_data: dict[str, Any] = json.loads(rendered)

    required_fields = ["version", "configurations"]
    for field in required_fields:
        assert field in json_data

    assert isinstance(json_data["configurations"], list)
    assert len(json_data["configurations"]) > 0
