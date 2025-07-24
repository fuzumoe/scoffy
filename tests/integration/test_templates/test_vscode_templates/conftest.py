from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader


@pytest.fixture
def vscode_template_dir() -> Path:
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent.parent.parent
    return project_root / "src" / "templates" / ".vscode"


@pytest.fixture
def env(vscode_template_dir):
    return Environment(loader=FileSystemLoader(vscode_template_dir))
