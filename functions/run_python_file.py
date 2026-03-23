import os
import subprocess
from config import TIMEOUT

def run_python_file(working_directory, file_path, args=[]):
    # Get file info
    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot excecute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_path_abs):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", file_path_abs]
    command.extend(args)

    try: 
        output = subprocess.run(
            command,
            cwd=working_dir_abs,
            timeout=TIMEOUT,
            capture_output=True,
            text=True
        )
        ret = f"""
STDOUT: {output.stdout}
STDERR: {output.stderr}
"""
        if output.stdout == "" and output.stderr == "":
            ret = f'No output produced:\n' + ret

        if output.returncode != 0:
            ret = f'Process exited with code {output.returncode}\n' + ret

        return ret

    except Exception as e:
        return f'Excecution failed: {file_path}, {e}'

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
