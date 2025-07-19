import os, subprocess

def run_python_file(working_directory, file_path, args=[]):

        abs_working_dir = os.path.abspath(working_directory)
        file_full_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Ensure the targeted file path is within the working_directory
        if not file_full_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        

        # Ensure the target file actually exists
        if not os.path.exists(file_full_path):
            return f'Error: File "{file_path}" not found.'
        

        # Ensure the target file is a python file (ends with ".py")
        if not (file_full_path.endswith(".py")):
            return f'Error: "{file_path}" is not a Python file.'
        
        try:
            complete_args = ["python3", file_full_path] + args
            #print("DBG: complete_args=", complete_args)
            completed_process = subprocess.run(complete_args, timeout=30, capture_output=True, text=True, cwd=abs_working_dir)

            output = []
            if completed_process.stdout:
                output.append(f"STDOUT:\n{completed_process.stdout}")
            if completed_process.stderr:
                output.append(f"STDERR:\n{completed_process.stderr}")

            if completed_process.returncode != 0:
                output.append(f"Process exited with code {completed_process.returncode}")

            return "\n".join(output) if output else "No output produced."
                 
        except Exception as e:
             return f"Error: executing Python file: {e}"