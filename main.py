import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages)

    if verbose_flag != None:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print(response.text) # Prints LLM:s response



if __name__ == "__main__":
    main()
