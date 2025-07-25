import logging
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, Template

logger = logging.getLogger(__name__)


@pytest.fixture
def env(code_quality_template_dir: Path) -> Environment:
    """Return a Jinja2 environment for the code quality templates."""
    return Environment(loader=FileSystemLoader(code_quality_template_dir))


@pytest.fixture
def pytest_template(env: Environment) -> Template:
    """Return the pytest.ini template."""
    return env.get_template("pytest.ini.j2")


def test_pytest_template_exists(code_quality_template_dir: Path) -> None:
    """Test that the pytest.ini template exists."""
    assert (code_quality_template_dir / "pytest.ini.j2").exists()


def test_pytest_ini_renders_with_default_values(pytest_template: Template) -> None:
    """Test that the pytest.ini template renders with default values."""
    context = {"project_name": "Test Project"}
    rendered = pytest_template.render(**context)

    assert "# Pytest Configuration for Test Project" in rendered
    assert "testpaths = tests" in rendered
    assert (
        "norecursedirs = env venv .env .venv node_modules .git __pycache__ .pytest_cache"
        in rendered
    )
    assert "filterwarnings = ignore::DeprecationWarning" in rendered
    assert "verbosity = 2" in rendered
    assert "showlocals = True" in rendered
    assert "durations = 10" in rendered
    assert "xvs = True" in rendered
    assert "addopts = -xvs" in rendered
    assert "log_cli = True" in rendered


def test_pytest_ini_renders_with_custom_values(pytest_template: Template) -> None:
    """Test that the pytest.ini template renders with custom values."""
    context = {
        "project_name": "Custom Project",
        "testpaths": "custom_tests",
        "norecursedirs": "custom_ignore",
        "filterwarnings": "ignore::UserWarning",
        "verbose": True,
        "verbosity": 3,
        "showlocals": False,
        "durations": True,
        "durations_number": 5,
        "parallel": True,
        "numprocesses": 4,
        "addopts": "--no-cov",
        "app_name": "custom_app",
    }
    rendered = pytest_template.render(**context)

    assert "# Pytest Configuration for Custom Project" in rendered
    assert "testpaths = custom_tests" in rendered
    assert "norecursedirs = custom_ignore" in rendered
    assert "filterwarnings = ignore::UserWarning" in rendered
    assert "verbosity = 3" in rendered
    assert "showlocals = True" not in rendered
    assert "durations = 5" in rendered
    assert "addopts = -xvs --no-cov --numprocesses=4" in rendered


def test_pytest_ini_renders_with_custom_markers(pytest_template: Template) -> None:
    """Test that the pytest.ini template renders with custom markers."""
    context = {
        "custom_markers": {
            "smoke": "quick tests for sanity checking",
            "performance": "tests that measure execution time",
        }
    }
    rendered = pytest_template.render(**context)

    assert "smoke: quick tests for sanity checking" in rendered
    assert "performance: tests that measure execution time" in rendered


def test_pytest_ini_renders_with_env_vars(pytest_template: Template) -> None:
    """Test that the pytest.ini template renders with environment variables."""
    context = {
        "env_vars": {
            "TEST_ENV": "testing",
            "DEBUG": "True",
        }
    }
    rendered = pytest_template.render(**context)

    assert "env =" in rendered
    assert "TEST_ENV=testing" in rendered
    assert "DEBUG=True" in rendered


def test_pytest_ini_renders_with_coverage_options(pytest_template: Template) -> None:
    """Test that the pytest.ini template renders with coverage options."""
    context = {
        "enable_coverage": True,
        "app_name": "my_app",
        "cover_pylib": True,
        "minversion": "7.0",
        "coverage_addopts": "--cov=my_app --cov-report=term",
    }
    rendered = pytest_template.render(**context)

    assert "cover_pylib = True" in rendered
    assert "minversion = 7.0" in rendered
    assert "addopts = --cov=my_app --cov-report=term" in rendered


def test_pytest_ini_renders_with_junit_logging(pytest_template: Template) -> None:
    """Test that the pytest.ini template renders with JUnit logging options."""
    context = {
        "junit_logging": "all",
    }
    rendered = pytest_template.render(**context)

    assert "# JUnit XML logging" in rendered
    assert "junit_logging = all" in rendered


def test_pytest_ini_renders_with_custom_logging_config(
    pytest_template: Template,
) -> None:
    """Test that the pytest.ini template renders with custom logging configuration."""
    context = {
        "configure_logging": True,
        "log_cli": "False",
        "log_cli_level": "DEBUG",
        "log_cli_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "log_cli_date_format": "%Y-%m-%d %H:%M",
    }
    rendered = pytest_template.render(**context)

    assert "log_cli = False" in rendered
    assert "log_cli_level = DEBUG" in rendered
    assert (
        "log_cli_format = %(asctime)s - %(name)s - %(levelname)s - %(message)s"
        in rendered
    )
    assert "log_cli_date_format = %Y-%m-%d %H:%M" in rendered
