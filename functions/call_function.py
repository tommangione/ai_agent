import os

from google import genai

from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_files_info import schema_get_files_info

from functions.get_file_content import get_file_content
from functions.get_file_content import schema_get_file_content

from functions.run_python_file import run_python_file
from functions.run_python_file import schema_run_python_file

from functions.write_file import write_file
from functions.write_file import schema_write_file

from functions.config import WORKING_DIRECTORY

def call_function(function_call_part, verbose=False):
    
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    func_dict = {
        "get_files_info": get_files_info, 
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
           }

    function_call_part.args['working_directory'] = WORKING_DIRECTORY
    function_name = function_call_part.name

    if function_name not in func_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    try:
        function_result = func_dict[function_call_part.name](**function_call_part.args) 
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )

    except Exception as e:
        # This handles actual function execution errors
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": str(e)},
                )
            ],
        )


