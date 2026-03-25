import os

import pytest

from functions.tools.write_file import write_file
from config import WORKING_DIRECTORY


@pytest.fixture(autouse=True)
def cleanup():
    yield
    for path in [
        os.path.join(WORKING_DIRECTORY, "lorem.txt"),
        os.path.join(WORKING_DIRECTORY, "pkg", "morelorem.txt"),
    ]:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass


def test_write_new_file():
    result = write_file(WORKING_DIRECTORY, "lorem.txt", "wait, this isn't lorem ipsum")
    assert "Successfully wrote" in result


def test_write_file_in_subdirectory():
    result = write_file(WORKING_DIRECTORY, "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    assert "Successfully wrote" in result


def test_reject_absolute_path():
    result = write_file(WORKING_DIRECTORY, "/tmp/temp.txt", "this should not be allowed")
    assert "outside the permitted working directory" in result


def test_reject_write_in_tests_directory():
    result = write_file(WORKING_DIRECTORY, "tests/foo.py", "this should not be allowed")
    assert "inside a tests directory" in result
