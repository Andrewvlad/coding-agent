import os

import pytest

from functions.util.check_path import check_path
from config import WORKING_DIRECTORY

WORKING_DIR_ABS = os.path.abspath(WORKING_DIRECTORY)


def test_check_path_returns_absolute_path():
    result = check_path(WORKING_DIRECTORY, "main.py")
    assert os.path.isabs(result)


def test_check_path_dot_returns_working_dir():
    result = check_path(WORKING_DIRECTORY, ".")
    assert result == WORKING_DIR_ABS


def test_check_path_subdirectory():
    result = check_path(WORKING_DIRECTORY, "pkg/calculator.py")
    assert result.endswith(os.path.join("pkg", "calculator.py"))


def test_check_path_rejects_parent_traversal():
    with pytest.raises(PermissionError):
        check_path(WORKING_DIRECTORY, "../")


def test_check_path_rejects_deep_traversal():
    with pytest.raises(PermissionError):
        check_path(WORKING_DIRECTORY, "a/b/../../..")


def test_check_path_rejects_absolute_path():
    with pytest.raises(PermissionError):
        check_path(WORKING_DIRECTORY, "/etc/passwd")


def test_check_path_symlink_escape():
    link_path = os.path.join(WORKING_DIR_ABS, "_test_symlink_escape")
    try:
        os.symlink("/tmp", link_path)
        result = check_path(WORKING_DIRECTORY, "_test_symlink_escape/evil.txt")
        # check_path uses normpath/commonpath, not realpath, so it won't catch
        # symlink escapes — this documents the current behaviour
        assert result.startswith(WORKING_DIR_ABS)
    finally:
        if os.path.lexists(link_path):
            os.remove(link_path)
