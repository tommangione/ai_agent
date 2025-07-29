import sys
import os

from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
client = genai.Client(api_key=api_key)

from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_files_info import schema_get_files_info

from functions.get_file_content import get_file_content
from functions.get_file_content import schema_get_file_content

from functions.run_python_file import run_python_file
from functions.run_python_file import schema_run_python_file

from functions.write_file import write_file
from functions.write_file import schema_write_file

from functions.call_function import call_function


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


if len(sys.argv) > 2 and sys.argv[2] != "--verbose":
    print("Error: too many arguments.")
    exit(1)

if len(sys.argv) > 3:
    print("Error: too many arguments. Please enclose one prompt at a time in quotation marks. You may use optional argument --verbose after prompt for token data.")
    exit(1)

messages = [
        types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]


def main():
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt),
    )
    counter = 0
    for arg in sys.argv:
        if arg == "--verbose":
            counter += 1
    if counter > 0:
        verbose = True
    else:
        verbose = False
    if response.function_calls:
        for function_call_part in response.function_calls:
            #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            try:
                function_call_result = call_function(function_call_part, verbose)

                #if function_call_result.parts[0].function_response.response == "":
                    #raise Exception("fatal error: no response")

                response_dict = function_call_result.parts[0].function_response.response
                if not response_dict:
                    raise Exception("fatal error: no response")

                #if verbose == True:
                    #print(f"-> {function_call_result.parts[0].function_response.response}")

                if verbose == True:
                    response_dict = function_call_result.parts[0].function_response.response
                    if "result" in response_dict:
                        print(f"-> {response_dict['result']}")
                    elif "error" in response_dict:
                        print(f"-> Error: {response_dict['error']}")
                    else:
                        print(f"-> {response_dict}")

            except Exception as e:
                print(f"Error: {e}")
    else:
        print(response.text)
    tokprompt = response.usage_metadata.prompt_token_count
    tokresp = response.usage_metadata.candidates_token_count
    if verbose == True:
        print(f"User prompt: {sys.argv[1]}")
        print(f"Prompt tokens: {tokprompt}")
        print(f"Response tokens: {tokresp}")

main()
