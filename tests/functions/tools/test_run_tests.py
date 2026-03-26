from functions.tools.run_tests import run_tests
from config import WORKING_DIRECTORY


def test_run_all_tests():
    result = run_tests(WORKING_DIRECTORY)
    assert "passed" in result
