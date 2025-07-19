"""
Python File Execution Module

This module provides secure Python file execution functionality with path validation,
timeout protection, and comprehensive output capture for AI agent code execution tasks.
"""

import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    """
    Safely executes a Python file within the specified working directory.
    
    This function implements multiple security measures including path validation,
    file type verification, and execution timeout to prevent malicious code execution
    while capturing both stdout and stderr for comprehensive feedback.
    
    Args:
        working_directory (str): The base directory that constrains file access
        file_path (str): The relative path to the Python file within working_directory
        args (list, optional): Command line arguments to pass to the Python script.
                              Defaults to empty list.
        
    Returns:
        str: The combined stdout/stderr output from the executed script,
             or an error message if execution fails
    """
    
    # Convert paths to absolute paths for security validation
    # This prevents relative path attacks like "../../../malicious.py"
    abs_working_dir = os.path.abspath(working_directory)
    file_full_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check: Ensure the target file is within the working_directory
    # This prevents directory traversal attacks
    if not file_full_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Validate that the target file exists
    if not os.path.exists(file_full_path):
        return f'Error: File "{file_path}" not found.'
    
    # Security check: Ensure the target file is actually a Python file
    # This prevents execution of arbitrary file types
    if not file_full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        # Build the complete command with python3 interpreter and arguments
        complete_args = ["python3", file_full_path] + args
        # Uncomment for debugging: print("DBG: complete_args=", complete_args)
        
        # Execute the Python file with security constraints:
        # - timeout=30: Prevents infinite loops or long-running processes
        # - capture_output=True: Captures both stdout and stderr
        # - text=True: Returns output as strings instead of bytes
        # - cwd=abs_working_dir: Sets the working directory for execution
        completed_process = subprocess.run(
            complete_args, 
            timeout=30, 
            capture_output=True, 
            text=True, 
            cwd=abs_working_dir
        )

        # Collect and format output from the executed process
        output = []
        
        # Capture standard output if present
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
            
        # Capture error output if present
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")

        # Report non-zero exit codes (indicating errors or failures)
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")

        # Return combined output or indicate no output was produced
        return "\n".join(output) if output else "No output produced."
                 
    except subprocess.TimeoutExpired:
        # Handle timeout specifically for better error messaging
        return f"Error: Python file execution timed out after 30 seconds"
        
    except Exception as e:
        # Handle any other unexpected errors during execution
        return f"Error executing Python file: {e}"
