from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .write_file_content import write_file
from .run_python import run_python_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    # STEP 1: Prepare a dictionary mapping function names (as strings) to the actual function objects.
    # The keys MUST match the 'name' property in your function schemas (used by the LLM).
    functions = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    # STEP 2: Print the function call information, more detailed if 'verbose' is True
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # STEP 3: If the function name doesn't exist, return an error-wrapped response
    if function_call_part.name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    # STEP 4: Make a copy of the arguments to avoid changing the original!
    args_copy = function_call_part.args.copy()

    # STEP 5: Add the required working directory argument.
    # This ensures all file operations happen inside './calculator'
    args_copy["working_directory"] = "./calculator"

    # STEP 6: Look up the function to call by name, then call it using keyword unpacking (**)
    # This is equivalent to selected_func(file_path=..., working_directory=...).
    selected_func = functions[function_call_part.name]
    func_result = selected_func(**args_copy)

    # STEP 7: Wrap the function result using the required Part/Content format for the LLM tool response
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,          # The function you called
                response={"result": func_result}       # The result, wrapped in a dict as required
            )
        ],
    )