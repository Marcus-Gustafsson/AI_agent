"""
Function Schema Definitions Module

This module contains all the function declaration schemas for AI model integration.
These schemas tell the AI how to use each available function, including parameter
types, descriptions, and requirements for proper function calling.

Each schema corresponds to a function in the functions/ directory and defines:
- Function name and description
- Parameter specifications with types and descriptions
- Required vs optional parameters
"""

from google.genai import types


# File reading functionality schema
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file within the working directory, with content length limiting for AI processing.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to read within the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

# Directory listing functionality schema
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
        # Note: 'directory' parameter is optional, defaults to current directory
    ),
)

# Python file execution functionality schema
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory with optional command line arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the Python file to execute within the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command line arguments to pass to the Python script.",
                items=types.Schema(type=types.Type.STRING),  # Array of strings
            ),
        },
        required=["file_path"],  # Only file_path is required, args are optional
    ),
)

# File writing functionality schema
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory, creating parent directories if needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to write within the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],  # Both parameters are required for writing
    ),
)


# List of all available function schemas for easy import and management
ALL_SCHEMAS = [
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
]