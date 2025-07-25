import logging
from pathlib import Path
from typing import Any

import pytest
from jinja2 import Environment, FileSystemLoader, Template

logger = logging.getLogger(__name__)


@pytest.fixture
def env(code_quality_template_dir: Path) -> Environment:
    """Return a Jinja2 environment for the code quality templates."""
    return Environment(loader=FileSystemLoader(code_quality_template_dir))


@pytest.fixture
def mypy_template(env: Environment) -> Template:
    """Return the mypy.ini template."""
    return env.get_template("mypy.ini.j2")


def test_mypy_template_exists(code_quality_template_dir: Path) -> None:
    """Test that the mypy.ini template exists."""
    assert (code_quality_template_dir / "mypy.ini.j2").exists()


def test_mypy_ini_renders_with_default_values(mypy_template: Template) -> None:
    """Test that the mypy.ini template renders with default values."""
    context: dict[str, str] = {"project_name": "Test Project"}
    rendered: str = mypy_template.render(**context)

    assert "# MyPy Configuration for Test Project" in rendered
    assert "python_version = 3.12" in rendered
    assert "warn_return_any = True" in rendered
    assert "warn_unused_configs = True" in rendered
    assert "warn_redundant_casts = True" in rendered
    assert "disallow_untyped_defs = False" in rendered
    assert "ignore_missing_imports = True" in rendered
    assert "follow_imports = normal" in rendered
    assert "no_implicit_reexport = False" in rendered


def test_mypy_ini_renders_with_custom_values(mypy_template: Template) -> None:
    """Test that the mypy.ini template renders with custom values."""
    context: dict[str, str] = {
        "project_name": "Custom Project",
        "python_version": "3.10",
        "strict_typing": "True",
        "ignore_missing_imports": "False",
        "follow_imports": "skip",
        "no_implicit_reexport": "True",
    }
    rendered: str = mypy_template.render(**context)

    assert "# MyPy Configuration for Custom Project" in rendered
    assert "python_version = 3.10" in rendered
    assert "disallow_untyped_defs = True" in rendered
    assert "disallow_incomplete_defs = True" in rendered
    assert "disallow_untyped_decorators = True" in rendered
    assert "ignore_missing_imports = False" in rendered
    assert "follow_imports = skip" in rendered
    assert "no_implicit_reexport = True" in rendered


def test_mypy_ini_renders_with_warn_unreachable(mypy_template: Template) -> None:
    """Test that the mypy.ini template renders with warn_unreachable option."""
    context: dict[str, bool] = {
        "warn_unreachable": True,
    }
    rendered: str = mypy_template.render(**context)

    assert "# Warn on unreachable code" in rendered
    assert "warn_unreachable = True" in rendered


def test_mypy_ini_renders_with_plugins(mypy_template: Template) -> None:
    """Test that the mypy.ini template renders with plugins."""
    context: dict[str, list[str]] = {
        "plugins": ["pydantic.mypy", "sqlalchemy.ext.mypy.plugin"]
    }
    rendered: str = mypy_template.render(**context)

    assert "# Plugins" in rendered
    assert "plugins = pydantic.mypy, sqlalchemy.ext.mypy.plugin" in rendered


def test_mypy_ini_renders_with_cache_options(mypy_template: Template) -> None:
    """Test that the mypy.ini template renders with cache options."""
    context: dict[str, Any] = {"cache_dir": ".mypy_cache", "sqlite_cache": True}
    rendered: str = mypy_template.render(**context)

    assert "# Cache directory" in rendered
    assert "cache_dir = .mypy_cache" in rendered
    assert "# Use SQLite for caching" in rendered
    assert "sqlite_cache = True" in rendered


def test_mypy_ini_renders_with_error_codes(mypy_template: Template) -> None:
    """Test that the mypy.ini template renders with error code options."""
    context: dict[str, list[str]] = {
        "enable_error_code": ["redundant-expr", "unused-awaitable"],
        "disable_error_code": ["misc", "no-untyped-def"],
    }
    rendered: str = mypy_template.render(**context)

    assert "# Enable specific error codes" in rendered
    assert "enable_error_code = redundant-expr, unused-awaitable" in rendered
    assert "# Disable specific error codes" in rendered
    assert "disable_error_code = misc, no-untyped-def" in rendered


def test_mypy_ini_renders_with_custom_modules(mypy_template: Template) -> None:
    """Test that the mypy.ini template renders with custom module options."""
    context: dict[str, dict[str, dict[str, str]]] = {
        "modules": {
            "app.models": {"disallow_untyped_defs": "True", "strict_optional": "False"},
            "app.api": {
                "ignore_missing_imports": "True",
                "disallow_any_explicit": "True",
            },
        }
    }
    rendered: str = mypy_template.render(**context)

    assert "[mypy.app.models]" in rendered
    assert "disallow_untyped_defs = True" in rendered
    assert "strict_optional = False" in rendered
    assert "[mypy.app.api]" in rendered
    assert "ignore_missing_imports = True" in rendered
    assert "disallow_any_explicit = True" in rendered
    assert "[mypy.tests.*]" not in rendered


def test_mypy_ini_renders_without_custom_modules(mypy_template: Template) -> None:
    """Test that the mypy.ini template renders default module settings when no custom ones are provided."""
    context: dict[str, Any] = {}
    rendered: str = mypy_template.render(**context)

    assert "# Default module overrides for tests" in rendered
    assert "[mypy.tests.*]" in rendered
    assert "disallow_untyped_defs = False" in rendered
    assert "check_untyped_defs = True" in rendered


def test_mypy_ini_renders_with_stdlib_modules(mypy_template: Template) -> None:
    """Test that the mypy.ini template renders with stdlib module options."""
    context: dict[str, dict[str, dict[str, str]]] = {
        "stdlib_modules": {
            "dataclasses": {"disallow_untyped_defs": "True"},
            "typing": {"warn_redundant_casts": "True"},
        }
    }
    rendered: str = mypy_template.render(**context)

    assert "# Standard library modules that require type stubs" in rendered
    assert "[mypy.dataclasses]" in rendered
    assert "disallow_untyped_defs = True" in rendered
    assert "[mypy.typing]" in rendered
    assert "warn_redundant_casts = True" in rendered


def test_mypy_ini_renders_with_third_party_modules(mypy_template: Template) -> None:
    """Test that the mypy.ini template renders with third-party module options."""
    context: dict[str, dict[str, dict[str, str]]] = {
        "third_party": {
            "numpy": {"ignore_missing_imports": "True"},
            "pandas": {"ignore_missing_imports": "True"},
        }
    }
    rendered: str = mypy_template.render(**context)

    assert "# Third-party modules configuration" in rendered
    assert "[mypy.numpy]" in rendered
    assert "[mypy.pandas]" in rendered
    assert "[mypy.pydantic.*]" not in rendered
    assert "[mypy.fastapi.*]" not in rendered


def test_mypy_ini_renders_with_default_third_party(mypy_template: Template) -> None:
    """Test that the mypy.ini template renders with default third-party modules when none are provided."""
    context: dict[str, Any] = {}
    rendered: str = mypy_template.render(**context)

    assert "# Common third-party modules" in rendered
    assert "[mypy.pydantic.*]" in rendered
    assert "[mypy.fastapi.*]" in rendered
    assert "[mypy.sqlalchemy.*]" in rendered
    assert "ignore_missing_imports = True" in rendered
