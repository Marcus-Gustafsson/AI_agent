import os
from functions.config import MAX_FILE_CHAR_LENGTH


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