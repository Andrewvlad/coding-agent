import os

def write_file(working_directory, file_path, content):
    # Get file info
    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(file_path_abs):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    path_parts = os.path.normpath(file_path).split(os.sep)
    if "tests" in path_parts[:-1]:
        return f'Error: Cannot write to "{file_path}" as it is inside a tests directory'

    
    # Fill any non-existing paths
    parent_dir = os.path.dirname(file_path_abs)
    try:
        os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        return f'Could not create parent directories: {parent_dir} = {e}'

    # Write to file
    try:
        with open(file_path_abs, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Failed to write to file: {file_path}, {e}'

# Info for the agent on how the function works

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites an existing file or writes a new file if it doesn't exist (and creates required parent dirs safely), constrained to the working directory. Cannot edit files within a \"tests\" directory.",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, from the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents to write to the file as a string.",
            ),
 
        },
    ),
)
