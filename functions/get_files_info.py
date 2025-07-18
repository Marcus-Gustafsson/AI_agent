import os
from pathlib import Path


def get_files_info(working_directory, directory="."):
    abs_dir = os.path.abspath(directory)
    if abs_dir.startswith(working_directory) and abs_dir.__contains__("/AI_agent"):
        full_path = os.path.join(working_directory, directory)
        dir_contents = os.listdir(full_path)
        print("DBG: dir_contents = ", dir_contents)
        for file in dir_contents:
            file_path = f"{full_path}/{file}"
            print("DBG: file = ", file)
            print("DBG file size = ", os.path.getsize(file_path))
            print("DBG: is_dir = ", os.path.isdir(file_path))

    elif not os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    
    else:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'


print(get_files_info(os.getcwd()))