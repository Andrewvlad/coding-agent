from google.genai import types
from config import WORKING_DIRECTORY

from functions.tools.get_files_info import get_files_info
from functions.tools.get_file_content import get_file_content
from functions.tools.write_file import write_file
from functions.tools.run_python_file import run_python_file
from functions.tools.run_tests import run_tests

function_map = {
    "get_files_info"  : get_files_info,
    "get_file_content": get_file_content,
    "write_file"      : write_file,
    "run_python_file" : run_python_file,
    "run_tests"       : run_tests,
}

def call_function(function_call: types.FunctionCall, verbose: bool = False) -> types.Content:
    if verbose:
        print(f" - Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = WORKING_DIRECTORY

    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
