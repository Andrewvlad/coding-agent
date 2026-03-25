from functions.tools.get_files_info import get_files_info
from config import WORKING_DIRECTORY


def test_list_working_directory():
    result = get_files_info(WORKING_DIRECTORY, ".")
    assert "main.py" in result


def test_list_subdirectory():
    result = get_files_info(WORKING_DIRECTORY, "pkg")
    assert "calculator.py" in result


def test_reject_absolute_path():
    result = get_files_info(WORKING_DIRECTORY, "/bin")
    assert "outside the permitted working directory" in result


def test_reject_parent_traversal():
    result = get_files_info(WORKING_DIRECTORY, "../")
    assert "outside the permitted working directory" in result
