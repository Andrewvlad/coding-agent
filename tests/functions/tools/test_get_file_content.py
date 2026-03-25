from functions.tools.get_file_content import get_file_content
from config import WORKING_DIRECTORY


def test_read_file():
    result = get_file_content(WORKING_DIRECTORY, "main.py")
    assert "import sys" in result


def test_read_file_in_subdirectory():
    result = get_file_content(WORKING_DIRECTORY, "pkg/calculator.py")
    assert "class Calculator" in result


def test_reject_absolute_path():
    result = get_file_content(WORKING_DIRECTORY, "/bin/cat")
    assert "outside the permitted working directory" in result


def test_file_not_found():
    result = get_file_content(WORKING_DIRECTORY, "pkg/does_not_exist.py")
    assert "File not found" in result
