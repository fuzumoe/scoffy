from pathlib import Path

import pytest

current_file = Path(__file__)
project_root = current_file.parent.parent


@pytest.fixture
def project_root_fixture() -> Path:
    return project_root
