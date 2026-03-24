import os

from functions.util.check_path import check_path

def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000

    try:
        path_abs = check_path(working_directory, file_path)
    except Exception as e:
        return str(e)
    
    if not os.path.isfile(path_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(path_abs, "r") as f:
            contents = f.read(MAX_CHARS)

            # Indicate it was truncated by checking if there is more
            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return contents
    except Exception as e:
        return f'Exception reading file: {e}'

# Info for the agent on how the function works

from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of the given file as a string, constrained to the working directory.",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, from the working directory.",
            ),
        },
    ),
)
