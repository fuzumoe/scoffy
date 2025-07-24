import logging
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

# Configure logger for the test module
logger = logging.getLogger(__name__)


@pytest.fixture
def docker_template_dir(template_dir: Path) -> Path:
    return template_dir / "docker"


@pytest.fixture
def env(docker_template_dir):
    return Environment(loader=FileSystemLoader(docker_template_dir))
