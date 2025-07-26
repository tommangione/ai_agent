import os

def write_file(working_directory, file_path, content):
    
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)

    if abs_file_path.startswith(abs_working_directory) == False:
        return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    
    try:
#        if os.path.dirname(abs_file_path) == '':
#            with open(abs_file_path, "w") as f: f.write(content)
#        elif os.path.exists(os.path.dirname(abs_file_path)) == False:
#            os.makedirs(os.path.dirname(abs_file_path))
#            with open(abs_file_path, "w") as f: f.write(content)
#        else:
#            with open(abs_file_path, "w") as f: f.write(content)
        dir_name = os.path.dirname(abs_file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(abs_file_path, "w") as f: f.write(content)

        return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    
    except Exception as e:
        return(f"Error: {e}")

