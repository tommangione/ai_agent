import os

from google import genai

from google.genai import types

from functions.config import *

def get_file_content(working_directory, file_path):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)

    if abs_file_path.startswith(abs_working_directory) == False:
        return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

    if os.path.isfile(abs_file_path) == False:
        return(f'Error: File not found or is not a regular file: "{file_path}"')

    try:
        with open(abs_file_path) as f: content = f.read()
        if len(content) > CHAR_LIMIT:
            content = content[0:CHAR_LIMIT]
            content = content + f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return(f"Error: {e}")

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read from files, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The text file to read from.",
            ),
        },
    ),
)
