import os

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    if not os.path.isdir(working_dir_abs):
        return f'Error: "{directory}" is not a directory'

    # Will be True or False
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    ret = []
    
    directory_abs = os.path.abspath(directory)
    print(directory_abs)
    

    for content in os.listdir(target_dir):
        content_path = os.path.join(target_dir, content)
        if os.path.isfile(content_path) or os.path.isdir(content_path):
            is_dir = os.path.isdir(content_path)
            size = os.path.getsize(content_path)
            ret.append(f'- {content}: file_size={size}, is_dir={is_dir}')

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
