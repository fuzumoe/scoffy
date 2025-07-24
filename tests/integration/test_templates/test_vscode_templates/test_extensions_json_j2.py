import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture
def extensions_json_template(env):
    return env.get_template("extensions.json.j2")


def test_extensions_json_template_exists(vscode_template_dir):
    """Test that the extensions.json template exists."""
    assert (vscode_template_dir / "extensions.json.j2").exists()


# def test_extensions_json_renders_with_default_values(extensions_json_template):
#     """Test that the extensions.json template renders with default values."""
#     context = {}
#     rendered = extensions_json_template.render(**context)

#     assert "recommendations" in rendered
#     assert "{" in rendered
#     assert "}" in rendered


# def test_extensions_json_renders_with_python_extensions(extensions_json_template):
#     """Test that the extensions.json template renders with Python extensions."""
#     context = {"language": "python"}
#     rendered = extensions_json_template.render(**context)

#     assert "ms-python.python" in rendered
#     assert "ms-python.vscode-pylance" in rendered


# def test_extensions_json_renders_with_javascript_extensions(extensions_json_template):
#     """Test that the extensions.json template renders with JavaScript extensions."""
#     context = {"language": "javascript"}
#     rendered = extensions_json_template.render(**context)

#     assert "dbaeumer.vscode-eslint" in rendered
#     assert "esbenp.prettier-vscode" in rendered


# def test_extensions_json_renders_with_docker_extensions(extensions_json_template):
#     """Test that the extensions.json template renders with Docker extensions."""
#     context = {"use_docker": True}
#     rendered = extensions_json_template.render(**context)

#     assert "ms-azuretools.vscode-docker" in rendered


# def test_extensions_json_renders_with_database_extensions(extensions_json_template):
#     """Test that the extensions.json template renders with database extensions."""
#     context = {"database_type": "postgresql"}
#     rendered = extensions_json_template.render(**context)

#     assert "ckolkman.vscode-postgres" in rendered

#     # Test MongoDB extensions
#     context = {"database_type": "document"}
#     rendered = extensions_json_template.render(**context)

#     assert "mongodb.mongodb-vscode" in rendered


# def test_extensions_json_renders_with_git_extensions(extensions_json_template):
#     """Test that the extensions.json template renders with Git extensions."""
#     context = {"use_git": True}
#     rendered = extensions_json_template.render(**context)

#     assert "eamodio.gitlens" in rendered


# def test_extensions_json_renders_with_multiple_features(extensions_json_template):
#     """Test that the extensions.json template renders with multiple features."""
#     context = {
#         "language": "python",
#         "use_docker": True,
#         "database_type": "postgresql",
#         "use_git": True,
#     }
#     rendered = extensions_json_template.render(**context)

#     assert "ms-python.python" in rendered
#     assert "ms-azuretools.vscode-docker" in rendered
#     assert "ckolkman.vscode-postgres" in rendered
#     assert "eamodio.gitlens" in rendered
