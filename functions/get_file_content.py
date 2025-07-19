"""
File Content Reader Module

This module provides secure file reading functionality with path validation
and content length limiting for AI agent file operations.
"""

import os
from config import MAX_FILE_CHAR_LENGTH


def get_file_content(working_directory, file_path):
    """
    Safely reads the content of a file within the specified working directory.
    
    This function implements security measures to prevent directory traversal attacks
    and limits file content length to avoid overwhelming the AI model.
    
    Args:
        working_directory (str): The base directory that constrains file access
        file_path (str): The relative path to the file within working_directory
        
    Returns:
        str: The file content (truncated to MAX_FILE_CHAR_LENGTH) or an error message
    """
    
    # Convert paths to absolute paths for security validation
    # This prevents relative path attacks like "../../../etc/passwd"
    abs_working_dir = os.path.abspath(working_directory)
    target_full_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check: Ensure the target path is within the working_directory
    # This prevents directory traversal attacks
    if not target_full_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Validate that the target path exists and is actually a file (not a directory)
    if not os.path.isfile(target_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # Attempt to read the file content with proper error handling
    try:
        # Use context manager (with statement) for automatic file closure
        with open(target_full_path, "r") as file:
            
            # Read file content with length limitation to prevent memory issues
            # and avoid overwhelming the AI model with extremely large files
            file_content_string = file.read(MAX_FILE_CHAR_LENGTH)
            
            return file_content_string

    except Exception as E:
        # Return user-friendly error message for any file reading issues
        # (permissions, encoding errors, etc.)
        return f"Error: {E}"