from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader


@pytest.fixture
def git_template_dir() -> Path:
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent.parent.parent
    return project_root / "src" / "templates" / "git"


@pytest.fixture
def env(git_template_dir: Path) -> Environment:
    return Environment(loader=FileSystemLoader(git_template_dir))
