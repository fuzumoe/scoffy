from pathlib import Path

import pytest

current_file = Path(__file__)
project_root = current_file.parent.parent
template_path = project_root / "src" / "templates"


@pytest.fixture
def template_dir() -> Path:
    return template_path


@pytest.fixture
def project_root_fixture() -> Path:
    return project_root
