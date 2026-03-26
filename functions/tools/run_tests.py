import os
import subprocess
from config import TIMEOUT


def run_tests(working_directory: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)

    try:
        result = subprocess.run(
            ["python3", "-m", "pytest", working_dir_abs, "-v"],
            cwd=working_dir_abs,
            timeout=TIMEOUT,
            capture_output=True,
            text=True,
        )

        output = result.stdout + result.stderr

        return output if output.strip() else "(no output)"
    except subprocess.TimeoutExpired:
        return f"Error: Tests timed out after {TIMEOUT} seconds"
    except Exception as e:
        return f"Execution failed: {e}"


# Info for the agent on how the function works

from google.genai import types

schema_run_tests = types.FunctionDeclaration(
    name="run_tests",
    description="Run all tests in the working directory. Returns test results including pass/fail counts and failure details.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={},
    ),
)
