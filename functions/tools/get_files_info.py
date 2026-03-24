import os

from functions.util.check_path import check_path

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        path_abs = check_path(working_directory, directory)
    except Exception as e:
        return str(e)

    if not os.path.isdir(path_abs):
        return f'Error: "{directory}" is not a directory'

    ret = []

    for entry in os.scandir(path_abs):
        if entry.is_file() or entry.is_dir():
            size = entry.stat().st_size
            ret.append(f'- {entry.name}: file_size={size}, is_dir={entry.is_dir()}')

    return '\n'.join(ret)


# Info for the agent on how the function works

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
