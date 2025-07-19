"""
AI Agent CLI Tool

This module provides a command-line interface for interacting with an AI agent
that can perform file system operations using function calls.
"""

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich import print  # Beautiful text formatting, syntax highlighting, tables, progress bars, markdown, etc.
from prompt_toolkit import prompt  # Builds interactive input prompts (autocomplete, history, validation).
import config  # Config file with constants/other config variables.
import functions.function_schemas
from functions.call_function import call_function

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini API client with the API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    """
    Main function that handles CLI arguments, processes user prompts,
    and manages AI agent interactions with function calling capabilities.
    """
    # Validate command line arguments - require at least one prompt argument
    if len(sys.argv) < 2: 
        print('Error (No prompt), use: uv run main.py "<insert prompt here>" --optional flags') 
        sys.exit(1)
    
    # Extract user prompt from command line arguments
    user_prompt = sys.argv[1]
    verbose_flag = None

    # Check for optional verbose flag
    verbose_flag = "--verbose" in sys.argv

    # Create message structure for the AI model
    # The Content object represents a single message in the conversation
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),  # role = "user" or "model" (AI/LLM = model)
    ]

    # Define available functions that the AI can call
    # This tells the AI what tools it has access to
    available_functions = types.Tool(function_declarations=functions.function_schemas.ALL_SCHEMAS)

    # Generate content from the AI model with function calling capabilities
    response = client.models.generate_content(
        model=config.model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],  # Provide available functions to the AI
            system_instruction=config.system_prompt  # System-level instructions for the AI
        ),
    )

    # Display verbose information if requested
    if verbose_flag is not None:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Handle the AI response - check if it wants to call a function
    if response.function_calls:
        # AI decided to call one or more functions
        for function_call_part in response.function_calls:

            function_call_result = call_function(function_call_part, verbose=verbose_flag)
            function_response_part = function_call_result.parts[0].function_response
            
            if function_response_part is None:
                raise Exception("Fatal: No function response found in function_call_result")
            if verbose_flag:
                print(f"-> {function_response_part.response}")
    else:
        # AI provided a text response instead of calling a function
        print(f"[bold green]LLM Response:[/bold green] {response.text}")


# Standard Python idiom to ensure main() only runs when script is executed directly
if __name__ == "__main__":
    main()