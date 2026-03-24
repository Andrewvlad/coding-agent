import os
import subprocess
from config import TIMEOUT

from functions.util.check_path import check_path

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []

    try:
        path_abs = check_path(working_directory, file_path)
    except Exception as e:
        return str(e)

    if not os.path.isfile(path_abs):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python3", path_abs]
    command.extend(args)

    try: 
        output = subprocess.run(
            command,
            cwd=os.path.abspath(working_directory),
            timeout=TIMEOUT,
            capture_output=True,
            text=True
        )

        ret = ""

        if output.returncode != 0:
            ret += f'Process exited with code {output.returncode}\n'

        if output.stdout == "" and output.stderr == "":
            ret += 'No output produced:\n'

        ret += f"""
STDOUT: {output.stdout}
STDERR: {output.stderr}
"""

        return ret

    except Exception as e:
        return f'Execution failed: {file_path}, {e}'

# Info for the agent on how the function works

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with the python3 interpreter. Accepts additional CLI args as an optional array.",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, from the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of strings to be used as the CLI args for the Python file.",
                items=types.Schema(
                    type=types.Type.STRING,
                
                )
            ),
        },
    ),
)
