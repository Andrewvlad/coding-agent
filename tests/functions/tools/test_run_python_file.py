import os

from functions.tools.run_python_file import run_python_file
from config import WORKING_DIRECTORY


def test_run_without_args():
    result = run_python_file(WORKING_DIRECTORY, "main.py")
    assert "STDOUT" in result


def test_run_with_args():
    result = run_python_file(WORKING_DIRECTORY, "main.py", ["3 + 5"])
    assert "8" in result


def test_run_tests():
    result = run_python_file(WORKING_DIRECTORY, "tests/calculator.py")
    assert "STDOUT" in result


def test_reject_parent_traversal():
    result = run_python_file(WORKING_DIRECTORY, "../main.py")
    assert "outside the permitted working directory" in result


def test_file_not_found():
    result = run_python_file(WORKING_DIRECTORY, "nonexistent.py")
    assert "does not exist" in result


def test_reject_non_python_file():
    txt_path = os.path.join(os.path.abspath(WORKING_DIRECTORY), "temp.txt")
    try:
        with open(txt_path, "w") as f:
            f.write("not python")
        result = run_python_file(WORKING_DIRECTORY, "temp.txt")
        assert "not a Python file" in result
    finally:
        try:
            os.remove(txt_path)
        except FileNotFoundError:
            pass
