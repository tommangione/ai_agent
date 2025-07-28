import os

from google import genai

from google.genai import types

def write_file(working_directory, file_path, content):
    
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)

    if abs_file_path.startswith(abs_working_directory) == False:
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    
    try:
        dir_name = os.path.dirname(abs_file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(abs_file_path, "w") as f: f.write(content)

        return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    
    except Exception as e:
        return(f"Error: {e}")

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a text file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory where the file should be written.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path (from the working directory) of the file to write.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["working_directory", "file_path", "content"],
    ),
)
