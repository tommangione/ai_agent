import os

from google import genai

from google.genai import types

import subprocess

def run_python_file(working_directory, file_path, args=[]):
    
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)

    if abs_file_path.startswith(abs_working_directory) == False:
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

    if os.path.isfile(abs_file_path) == False:
        return(f'Error: File "{file_path}" not found.')

    if file_path[-3:] != ".py":
        return(f'Error: "{file_path}" is not a Python file.')

    try:
        command_args = ["python", abs_file_path]
        args = command_args + args
        std_output = subprocess.run(args, capture_output=True, cwd=abs_working_directory, timeout=30, check=False, text=True)

        if std_output.stdout == "" and std_output.returncode == 0 and std_output.stderr == "":
            return(f"No output produced.")

        output_parts = []
        if std_output.stdout.strip():
            output_parts.append(std_output.stdout.strip())
        if std_output.stderr.strip():
            # Don't add "STDERR:" prefix for successful runs (returncode == 0)
            if std_output.returncode == 0:
                output_parts.append(std_output.stderr.strip())
            else:
                output_parts.append(f"STDERR: {std_output.stderr.strip()}")
        if std_output.returncode != 0:
            output_parts.append(f"Process exited with code {std_output.returncode}")

        return "\n".join(output_parts) if output_parts else "No output produced."

    except Exception as e:
        return(f"Error: executing Python file: {e}")

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python script, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the Python script. If none are specified, run the python file with no further arguments without prompting the user.",
            ),
        },
    ),
)
