"""
File Writing Module

This module provides secure file writing functionality with path validation,
automatic directory creation, and comprehensive error handling for AI agent
file manipulation tasks with line-by-line change tracking.
"""

import os
import datetime
import difflib


def write_file(working_directory, file_path, content):
    """
    Safely writes content to a file with line-by-line AI attribution for changes.
    
    This function compares the new content with existing file content (if any),
    identifies changed lines, and adds inline comments to mark AI modifications.
    
    Args:
        working_directory (str): The base directory that constrains file access
        file_path (str): The relative path to the file within working_directory
        content (str): The content to write to the file
        
    Returns:
        str: Success message with character count and change summary
    """
    
    # Convert paths to absolute paths for security validation
    abs_working_dir = os.path.abspath(working_directory)
    file_full_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Security check: Ensure the target path is within the working_directory
    if not file_full_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # Create parent directories if they don't exist
    if not os.path.exists(file_full_path):
        try:
            os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
        except Exception as e:
            return f"Error creating directory: {e}"
    
    # Validate that the target path is not a directory
    if os.path.exists(file_full_path) and os.path.isdir(file_full_path):
        return f'Error: "{file_path}" is a directory, not a file'
    
    # ========== LINE-BY-LINE ATTRIBUTION ==========
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Read existing content if file exists
    original_content = ""
    is_new_file = not os.path.exists(file_full_path)
    
    if not is_new_file:
        try:
            with open(file_full_path, 'r') as f:
                original_content = f.read()
        except Exception:
            original_content = ""
    
    # Get comment style based on file extension
    def get_comment_style(file_path):
        if file_path.endswith('.py'):
            return "# "
        elif file_path.endswith(('.js', '.ts', '.java', '.c', '.cpp', '.cs')):
            return "// "
        elif file_path.endswith(('.html', '.xml')):
            return "<!-- ", " -->"
        elif file_path.endswith('.md'):
            return "<!-- ", " -->"
        elif file_path.endswith(('.css', '.scss')):
            return "/* ", " */"
        else:
            return "# "  # Default
    
    # Process content with line-by-line attribution
    def add_line_attribution(original_content, new_content, file_path, timestamp):
        comment_style = get_comment_style(file_path)
        
        # Handle HTML-style comments (with start and end)
        if isinstance(comment_style, tuple):
            comment_start, comment_end = comment_style
            ai_comment = f" {comment_start}Modified by AI Agent on {timestamp}{comment_end}"
            file_header = f"{comment_start}File created by AI Agent on {timestamp}{comment_end}"
        else:
            ai_comment = f" {comment_style}Modified by AI Agent on {timestamp}"
            file_header = f"{comment_style}File created by AI Agent on {timestamp}"
        
        # Split into lines
        original_lines = original_content.splitlines() if original_content else []
        new_lines = new_content.splitlines()
        
        # If it's a new file, ALWAYS add attribution header
        if is_new_file:
            if new_content.strip():  # File has content
                return file_header + "\n" + new_content
            else:  # File is empty - just add the header
                return file_header + "\n"
        
        # For existing files, identify changed lines
        result_lines = []
        
        # Simple line-by-line comparison
        for i in range(len(new_lines)):
            line = new_lines[i]
            
            # Check if this line is different from original
            if i >= len(original_lines) or (i < len(original_lines) and line != original_lines[i]):
                # This line was added or modified
                if line.strip():  # Don't add comments to empty lines
                    line_with_comment = line + ai_comment
                    result_lines.append(line_with_comment)
                else:
                    result_lines.append(line)
            else:
                # Line unchanged
                result_lines.append(line)
        
        return "\n".join(result_lines)
    
    # Apply line-by-line attribution
    final_content = add_line_attribution(original_content, content, file_path, timestamp)
    
    # Write the content to the file
    try:
        with open(file_full_path, "w") as file:
            file.write(final_content)
            
            # Count changes for feedback
            original_line_count = len(original_content.splitlines()) if original_content else 0
            new_line_count = len(final_content.splitlines())
            
            action = "created" if is_new_file else "modified"
            return f'Successfully {action} "{file_path}" with line-by-line AI attribution ({len(final_content)} characters, {new_line_count} lines, {abs(new_line_count - original_line_count)} lines changed)'

    except PermissionError:
        return f"Error: Permission denied writing to '{file_path}'"
    except OSError as e:
        return f"Error: File system error writing to '{file_path}': {e}"
    except Exception as e:
        return f"Error writing to file: {e}"