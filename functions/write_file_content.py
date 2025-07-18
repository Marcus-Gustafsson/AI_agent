import os

def write_file(working_directory, file_path, content):

        abs_working_dir = os.path.abspath(working_directory)
        file_full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Ensure the target path is within the working_directory
        if not file_full_path.startswith(abs_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(file_full_path):
            
            try:
                os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
            except Exception as e:
                return f"Error: creating directory: {e}"
            
        if os.path.exists(file_full_path) and os.path.isdir(file_full_path):
            return f'Error: "{file_path}" is a directory, not a file'
        
        try:
            with open(file_full_path, "w") as file:
                print("DBG: Writing to file at path: ", file_full_path)
                file.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

        except Exception as E:
            return f"Error: {E}"
        
        finally:
            file.close()