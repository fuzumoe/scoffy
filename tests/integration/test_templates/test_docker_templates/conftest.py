from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader


@pytest.fixture
def docker_template_dir() -> Path:
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent.parent.parent
    return project_root / "src" / "templates" / "docker"


@pytest.fixture
def env(docker_template_dir):
    return Environment(loader=FileSystemLoader(docker_template_dir))
