from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader


@pytest.fixture
def code_quality_template_dir() -> Path:
    """Return the code quality template directory."""
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent.parent.parent
    return project_root / "src" / "templates" / "code_quality"


@pytest.fixture
def env(code_quality_template_dir: Path) -> Environment:
    return Environment(loader=FileSystemLoader(code_quality_template_dir))
