import os

def check_path(working_directory, path='.'):
    working_dir_abs = os.path.abspath(working_directory)
    path_abs = os.path.normpath(os.path.join(working_dir_abs, path))

    valid_target_dir = os.path.commonpath([working_dir_abs, path_abs]) == working_dir_abs
    if not valid_target_dir:
        raise PermissionError(f'Error: "{path}" is outside the permitted working directory')

    return path_abs
