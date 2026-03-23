import os
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

WORKING_DIR = "calculator"


# --- get_files_info ---

def test_list_working_directory():
    result = get_files_info(WORKING_DIR, ".")
    assert "main.py" in result

def test_list_subdirectory():
    result = get_files_info(WORKING_DIR, "pkg")
    assert "calculator.py" in result

def test_reject_absolute_path_files_info():
    result = get_files_info(WORKING_DIR, "/bin")
    assert result.startswith("Error")

def test_reject_parent_traversal_files_info():
    result = get_files_info(WORKING_DIR, "../")
    assert result.startswith("Error")


# --- get_file_content ---

def test_read_file():
    result = get_file_content(WORKING_DIR, "main.py")
    assert not result.startswith("Error")

def test_read_file_in_subdirectory():
    result = get_file_content(WORKING_DIR, "pkg/calculator.py")
    assert not result.startswith("Error")

def test_reject_absolute_path_file_content():
    result = get_file_content(WORKING_DIR, "/bin/cat")
    assert result.startswith("Error")

def test_file_not_found():
    result = get_file_content(WORKING_DIR, "pkg/does_not_exist.py")
    assert result.startswith("Error")


# --- write_file ---

def test_write_new_file():
    result = write_file(WORKING_DIR, "lorem.txt", "wait, this isn't lorem ipsum")
    assert "Successfully wrote" in result

def test_write_file_in_subdirectory():
    result = write_file(WORKING_DIR, "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    assert "Successfully wrote" in result

def test_reject_absolute_path_write():
    result = write_file(WORKING_DIR, "/tmp/temp.txt", "this should not be allowed")
    assert result.startswith("Error")

def test_reject_write_in_tests_directory():
    result = write_file(WORKING_DIR, "tests/foo.py", "this should not be allowed")
    assert result.startswith("Error")

def cleanup_write_tests():
    for path in ["calculator/lorem.txt", "calculator/pkg/morelorem.txt"]:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass


# --- run_python_file ---

def test_run_without_args():
    result = run_python_file(WORKING_DIR, "main.py")
    assert "STDOUT" in result

def test_run_with_args():
    result = run_python_file(WORKING_DIR, "main.py", ["3 + 5"])
    assert "STDOUT" in result

def test_run_tests():
    result = run_python_file(WORKING_DIR, "tests/calculator.py")
    assert "STDOUT" in result

def test_reject_parent_traversal_run():
    result = run_python_file(WORKING_DIR, "../main.py")
    assert result.startswith("Error")

def test_file_not_found_run():
    result = run_python_file(WORKING_DIR, "nonexistent.py")
    assert result.startswith("Error")

def test_reject_non_python_file():
    result = run_python_file(WORKING_DIR, "lorem.txt")
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
