import os
from functions.config import MAX_FILE_CHAR_LENGTH


def get_files_info(working_directory, directory="."):
    try:

        abs_working_dir = os.path.abspath(working_directory)
        target_full_path = os.path.abspath(os.path.join(working_directory, directory))

        # Ensure the target path is within the working_directory
        # This also handles '..' and '/' based paths that try to escape
        if not target_full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Ensure the target path is actually a directory
        if not os.path.isdir(target_full_path):
            # This handles cases where 'directory' might be a file or non-existent
            return f'Error: "{directory}" is not a directory'
    
        if abs_working_dir.__contains__("/AI_agent") and target_full_path.startswith(abs_working_dir):
            dir_contents = os.listdir(target_full_path)
            content_representation = ""
            for file_name in dir_contents:
                file_path = os.path.join(target_full_path, file_name) # Use os.path.join for robustness
                file_size = os.path.getsize(file_path)
                file_is_dir = os.path.isdir(file_path)
                content_representation += f"- {file_name}: file_size={file_size} bytes, is_dir={file_is_dir}\n"
            return content_representation

    except Exception as e:
        return f"Error: {e}"
    


def get_file_content(working_directory, file_path):

        abs_working_dir = os.path.abspath(working_directory)
        target_full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Ensure the target path is within the working_directory
        if not target_full_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure the target path is actually a file
        if not os.path.isfile(target_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        

        try:
            print("DBG: trying to open file at path: ", target_full_path)
            with open(target_full_path, "r") as file:
                print("DBG: Reading file at path: ", target_full_path)
                file_content_string = file.read(MAX_FILE_CHAR_LENGTH)
                print("DBG: file_content_string len = ", len(file_content_string))
                return file_content_string

        except Exception as E:
            return f"Error: {E}"
        
        finally:
            file.close()

