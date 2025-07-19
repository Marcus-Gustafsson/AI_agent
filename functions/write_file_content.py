"""
File Writing Module

This module provides secure file writing functionality with path validation,
automatic directory creation, and comprehensive error handling for AI agent
file manipulation tasks.
"""

import os


def write_file(working_directory, file_path, content):
    """
    Safely writes content to a file within the specified working directory.
    
    This function implements security measures to prevent directory traversal attacks,
    automatically creates parent directories if needed, and provides comprehensive
    error handling for various file system scenarios.
    
    Args:
        working_directory (str): The base directory that constrains file access
        file_path (str): The relative path to the file within working_directory
        content (str): The content to write to the file
        
    Returns:
        str: Success message with character count, or an error message if operation fails
    """
    
    # Convert paths to absolute paths for security validation
    # This prevents relative path attacks like "../../../malicious.txt"
    abs_working_dir = os.path.abspath(working_directory)
    file_full_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check: Ensure the target path is within the working_directory
    # This prevents directory traversal attacks
    if not file_full_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # Create parent directories if they don't exist
    # This allows writing to nested paths like "src/utils/helper.py"
    if not os.path.exists(file_full_path):
        try:
            # exist_ok=True prevents errors if directory already exists
            os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
        except Exception as e:
            return f"Error creating directory: {e}"
    
    # Validate that the target path is not a directory
    # Prevents accidentally trying to write content to a directory
    if os.path.exists(file_full_path) and os.path.isdir(file_full_path):
        return f'Error: "{file_path}" is a directory, not a file'
    
    # Write the content to the file with proper error handling
    try:
        # Use context manager (with statement) for automatic file closure
        with open(file_full_path, "w") as file:     
            # Write the content and provide feedback on success
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except PermissionError:
        # Handle specific permission-related errors
        return f"Error: Permission denied writing to '{file_path}'"
        
    except OSError as e:
        # Handle file system errors (disk full, invalid filename, etc.)
        return f"Error: File system error writing to '{file_path}': {e}"
        
    except Exception as e:
        # Handle any other unexpected errors
        return f"Error writing to file: {e}"
    