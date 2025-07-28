# from DIRNAME.FILENAME import FUNCTION_NAME
import os

from google import genai

from google.genai import types

def get_files_info(working_directory, directory="."):
    # directory parameter is treated as a relative path within the working directory
    dir_full_path = os.path.join(working_directory, directory)
    dir_absolute_path = os.path.abspath(dir_full_path)
    wkdir_absolute_path = os.path.abspath(working_directory)
    # Error handling:

    if dir_absolute_path.startswith(wkdir_absolute_path) == False:
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if os.path.isdir(dir_absolute_path) == False:
        return(f'Error: "{directory}" is not a directory')

    # The goal: to build and return a string representing the contents of the directory
    # example for what's returned:
    # - README.md: file_size=1032 bytes, is_dir=False
    # - src: file_size=128 bytes, is_dir=True
    # - package.json: file_size=1234 bytes, is_dir=False
    try:
        dir_contents = os.listdir(dir_absolute_path)
        output_block = ""
        if len(dir_contents) == 0:
            return("")
        for object in dir_contents:
            object_path = os.path.join(dir_absolute_path, object)
            object_size = os.path.getsize(object_path)
            if os.path.isdir(object_path) == True:
                is_dir = True
            else:
                is_dir = False
            output_block = output_block + f"- {object}: file_size={object_size} bytes, is_dir={is_dir}\n"  
        return output_block
    except Exception as e:
        return(f"Error: {e}")

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
