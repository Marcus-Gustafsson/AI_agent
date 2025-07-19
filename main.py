import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich import print # What it does: Beautiful text formatting, syntax highlighting, tables, progress bars, markdown, etc.
from prompt_toolkit import prompt # Builds interactive input prompts (autocomplete, history, validation).
from . import config # Config file with constants/other config variables.
from functions.get_files_info import schema_get_files_info


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)



def main():
    # Ensure that the correct number of arguments is provided 
    if len(sys.argv) < 2: 
        print('Error (No prompt), use: uv run main.py "<insert prompt here>" --opitional flags') 
        sys.exit(1)
    user_prompt = sys.argv[1]
    verbose_flag = None

    if len(sys.argv) > 2:
        verbose_flag = sys.argv[2]

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]), # role = "user" or "model" (AI/LLM = model)
    ]

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        ]
    )

    response = client.models.generate_content(
        model=config.model_name,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=config.system_prompt),
    )

    if verbose_flag != None:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print(f"[bold green]LLM Response:[/bold green] {response.text}")



if __name__ == "__main__":
    main()
