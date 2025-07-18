import os, sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)



def main():
    # Ensure that the correct number of arguments is provided 
    if len(sys.argv) < 2: 
        print('Error (No prompt), use: uv run main.py "<insert prompt here>"') 
        sys.exit(1) 
    cmd_args = sys.argv
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=cmd_args[1])
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
