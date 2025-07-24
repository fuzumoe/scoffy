from pathlib import Path

import pytest


@pytest.fixture
def root_dir() -> Path:
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent.parent
    return project_root
