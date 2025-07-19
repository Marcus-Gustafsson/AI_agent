"""
File System Information Module

This module provides secure directory listing functionality with path validation
for AI agent file system operations. It prevents directory traversal attacks
while providing detailed file and directory information.
"""

import os

def get_files_info(working_directory, directory="."):
    """
    Safely lists files and directories within the specified working directory.
    
    This function implements security measures to prevent directory traversal attacks
    and provides detailed information about each file/directory including size and type.
    
    Args:
        working_directory (str): The base directory that constrains file access
        directory (str, optional): The relative path to list within working_directory. 
                                 Defaults to "." (current directory)
        
    Returns:
        str: A formatted string listing all files/directories with their properties,
             or an error message if the operation fails
    """
    try:
        # Convert paths to absolute paths for security validation
        # This prevents relative path attacks like "../../../etc/passwd"
        abs_working_dir = os.path.abspath(working_directory)
        target_full_path = os.path.abspath(os.path.join(working_directory, directory))

        # Security check: Ensure the target path is within the working_directory
        # This prevents directory traversal attacks using '..' or absolute paths
        if not target_full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Validate that the target path exists and is actually a directory
        if not os.path.isdir(target_full_path):
            # This handles cases where 'directory' might be a file or non-existent path
            return f'Error: "{directory}" is not a directory'
    
        # Additional security check: Ensure we're working within the AI_agent project
        # This provides an extra layer of protection for the specific project structure
        if abs_working_dir.__contains__("/AI_agent") and target_full_path.startswith(abs_working_dir):
            
            # Get all items in the target directory
            dir_contents = os.listdir(target_full_path)
            
            # Build a formatted string representation of directory contents
            content_representation = ""
            
            # Iterate through each item and gather detailed information
            for file_name in dir_contents:
                # Use os.path.join for cross-platform path handling
                file_path = os.path.join(target_full_path, file_name)
                
                # Get file/directory properties
                file_size = os.path.getsize(file_path)  # Size in bytes
                file_is_dir = os.path.isdir(file_path)  # True if directory, False if file
                
                # Format the information in a consistent, readable way
                content_representation += f"- {file_name}: file_size={file_size} bytes, is_dir={file_is_dir}\n"
            
            return content_representation
        
        # If we reach here, the security check failed
        return f'Error: Access denied - not within permitted project directory'

    except Exception as e:
        # Handle any unexpected errors (permissions, I/O errors, etc.)
        return f"Error: {e}"