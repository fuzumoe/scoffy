import sys
from io import StringIO
from unittest.mock import patch

from main import main

sys.path.insert(0, "/opt/adam/scoffy")


def test_main_prints_expected_message():
    """Test that main() prints the expected message."""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        main()
        assert fake_out.getvalue().strip() == "Hello from scoffy!"


def test_main_function_exists():
    """Test that main function exists and is callable."""
    assert callable(main)


def test_main_returns_none():
    """Test that main function returns None."""
    assert main() is None
