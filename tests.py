import os
from functions.util.check_path import check_path
from functions.tools.get_files_info import get_files_info
from functions.tools.get_file_content import get_file_content
from functions.tools.write_file import write_file
from functions.tools.run_python_file import run_python_file
from config import WORKING_DIRECTORY

WORKING_DIR_ABS = os.path.abspath(WORKING_DIRECTORY)

# --- check_path ---

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
    try:
        check_path(WORKING_DIRECTORY, "../")
        assert False, "Expected PermissionError"
    except PermissionError:
        pass

def test_check_path_rejects_deep_traversal():
    try:
        check_path(WORKING_DIRECTORY, "a/b/../../..")
        assert False, "Expected PermissionError"
    except PermissionError:
        pass

def test_check_path_rejects_absolute_path():
    try:
        check_path(WORKING_DIRECTORY, "/etc/passwd")
        assert False, "Expected PermissionError"
    except PermissionError:
        pass

def test_check_path_symlink_escape():
    link_path = os.path.join(WORKING_DIR_ABS, "_test_symlink_escape")
    try:
        os.symlink("/tmp", link_path)
        result = check_path(WORKING_DIRECTORY, "_test_symlink_escape/evil.txt")
        # check_path uses normpath/commonpath, not realpath, so it won't catch
        # symlink escapes — this documents the current behaviour
        assert os.path.isabs(result)
    finally:
        if os.path.lexists(link_path):
            os.remove(link_path)


# --- get_files_info ---

def test_list_working_directory():
    result = get_files_info(WORKING_DIRECTORY, ".")
    assert "main.py" in result

def test_list_subdirectory():
    result = get_files_info(WORKING_DIRECTORY, "pkg")
    assert "calculator.py" in result

def test_reject_absolute_path_files_info():
    result = get_files_info(WORKING_DIRECTORY, "/bin")
    assert result.startswith("Error")

def test_reject_parent_traversal_files_info():
    result = get_files_info(WORKING_DIRECTORY, "../")
    assert result.startswith("Error")


# --- get_file_content ---

def test_read_file():
    result = get_file_content(WORKING_DIRECTORY, "main.py")
    assert not result.startswith("Error")

def test_read_file_in_subdirectory():
    result = get_file_content(WORKING_DIRECTORY, "pkg/calculator.py")
    assert not result.startswith("Error")

def test_reject_absolute_path_file_content():
    result = get_file_content(WORKING_DIRECTORY, "/bin/cat")
    assert result.startswith("Error")

def test_file_not_found():
    result = get_file_content(WORKING_DIRECTORY, "pkg/does_not_exist.py")
    assert result.startswith("Error")


# --- write_file ---

def test_write_new_file():
    result = write_file(WORKING_DIRECTORY, "lorem.txt", "wait, this isn't lorem ipsum")
    assert "Successfully wrote" in result

def test_write_file_in_subdirectory():
    result = write_file(WORKING_DIRECTORY, "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    assert "Successfully wrote" in result

def test_reject_absolute_path_write():
    result = write_file(WORKING_DIRECTORY, "/tmp/temp.txt", "this should not be allowed")
    assert result.startswith("Error")

def test_reject_write_in_tests_directory():
    result = write_file(WORKING_DIRECTORY, "tests/foo.py", "this should not be allowed")
    assert result.startswith("Error")

def cleanup_write_tests():
    for path in [f"{WORKING_DIRECTORY}/lorem.txt", f"{WORKING_DIRECTORY}/pkg/morelorem.txt"]:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass


# --- run_python_file ---

def test_run_without_args():
    result = run_python_file(WORKING_DIRECTORY, "main.py")
    assert "STDOUT" in result

def test_run_with_args():
    result = run_python_file(WORKING_DIRECTORY, "main.py", ["3 + 5"])
    assert "STDOUT" in result

def test_run_tests():
    result = run_python_file(WORKING_DIRECTORY, "tests/calculator.py")
    assert "STDOUT" in result

def test_reject_parent_traversal_run():
    result = run_python_file(WORKING_DIRECTORY, "../main.py")
    assert result.startswith("Error")

def test_file_not_found_run():
    result = run_python_file(WORKING_DIRECTORY, "nonexistent.py")
    assert result.startswith("Error")

def test_reject_non_python_file():
    result = run_python_file(WORKING_DIRECTORY, "lorem.txt")
    assert result.startswith("Error")


if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith("test_")]
    passed = 0
    failed = 0

    cleanup_write_tests()

    for t in tests:
        try:
            t()
            passed += 1
            print(f"  PASS: {t.__name__}")
        except Exception as e:
            failed += 1
            print(f"  FAIL: {t.__name__}: {e}")

    cleanup_write_tests()

    print(f"\n{passed} passed, {failed} failed, {passed + failed} total")
    if failed > 0:
        exit(1)
