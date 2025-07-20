"""
AI Agent CLI Tool

This module provides a command-line interface for interacting with an AI agent
that can perform file system operations using function calls. The agent uses
Google's Gemini API to process user requests and can iteratively call functions
to gather information and complete tasks.

Features:
- Interactive AI agent with function calling capabilities
- Beautiful console output with Rich formatting
- Verbose mode with detailed execution visualization
- Syntax highlighting for code files
- Progress indicators with spinners
- Error handling and iteration limits

Usage:
    python main.py "your prompt here" [--verbose]

Example:
    python main.py "how does the calculator render results to the console?" --verbose
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
    Main function that orchestrates the AI agent's operation.
    
    This function:
    1. Parses command line arguments for user prompt and flags
    2. Initializes the conversation with the user's prompt
    3. Runs an iterative loop where the AI can:
       - Generate responses
       - Call functions to gather information
       - Build up context through conversation history
    4. Displays beautiful formatted output in verbose mode
    5. Handles errors gracefully
    
    The agent continues iterating until either:
    - The AI provides a final text response (no more function calls)
    - Maximum iterations (20) are reached
    - An error occurs
    
    Args:
        None (uses sys.argv for command line arguments)
        
    Returns:
        None (outputs results to console)
        
    Raises:
        SystemExit: If no prompt is provided
        Exception: Various exceptions during AI processing (handled gracefully)
    """
    
    # ========== ARGUMENT PARSING ==========
    # Validate command line arguments - require at least one prompt argument
    if len(sys.argv) < 2: 
        print('Error (No prompt), use: uv run main.py "<insert prompt here>" --optional flags') 
        sys.exit(1)
    
    # Extract user prompt from command line arguments
    user_prompt = sys.argv[1]
    verbose_flag = None

    # Check for optional verbose flag for detailed output
    verbose_flag = "--verbose" in sys.argv

    # ========== CONVERSATION SETUP ==========
    # Create message structure for the AI model
    # The Content object represents a single message in the conversation
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),  # role = "user" or "model" (AI/LLM = model)
    ]

    # Define available functions that the AI can call
    # This tells the AI what tools it has access to
    available_functions = types.Tool(function_declarations=functions.function_schemas.ALL_SCHEMAS)

    # ========== MAIN AGENT LOOP ==========
    # The agent loop allows the AI to make multiple "moves" and build up context
    for iteration in range(20):  # Max 20 iterations to prevent infinite loops
        try:
            # ========== AI RESPONSE GENERATION ==========
            # Generate content from the AI model with function calling capabilities
            response = client.models.generate_content(
                model=config.model_name,
                contents=messages,  # Pass entire conversation history for context
                config=types.GenerateContentConfig(
                    tools=[available_functions],  # Provide available functions to the AI
                    system_instruction=config.system_prompt  # System-level instructions for the AI
                ),
            )

            # Add AI's response to the conversation history
            # This ensures the AI remembers what it just "said" or "thought"
            for candidate in response.candidates:
                messages.append(candidate.content)

            # ========== CHECK IF AGENT IS DONE ==========
            # If AI provides text response and no function calls, it's finished
            if not response.function_calls:
                from rich.panel import Panel
                print(Panel(response.text, title="🎯 Final Answer", style="bold green"))
                break  # Exit the loop - agent is done!

            # ========== VERBOSE OUTPUT DISPLAY ==========
            # Show detailed information about the AI's thinking process
            if verbose_flag:
                from rich.panel import Panel
                
                # Create a beautiful iteration header
                print(Panel(f"🤖 Agent Iteration #{iteration}", style="cyan bold"))
                print(f"📝 Conversation: {len(messages)} messages")
                
                # Show AI thinking with nice formatting
                # Extract the AI's reasoning text from the response
                for candidate in response.candidates:
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text and part.text.strip():
                            # Truncate long thoughts for readability
                            thinking_text = part.text[:200] + "..." if len(part.text) > 200 else part.text
                            print(Panel(thinking_text, title="💭 AI Thinking", style="yellow"))
                            break
                
                # Show which functions the AI wants to call
                if response.function_calls:
                    function_names = [f"🔧 {fc.name}" for fc in response.function_calls]
                    print(f"[bold green]Calling:[/bold green] {', '.join(function_names)}")
                print()  # Add some spacing for readability

            # Handle the AI response - check if it wants to call a function
            if response.function_calls:
                # Process each function call the AI wants to make
                for function_call_part in response.function_calls:

                    # ========== FUNCTION EXECUTION WITH SPINNER ==========
                    # Show spinner while function is executing (if verbose)
                    if verbose_flag:
                        from rich.console import Console
                        from rich.spinner import Spinner
                        from rich.live import Live
                        import time
                        
                        console = Console()
                        
                        # Show animated spinner while function executes
                        with Live(Spinner("dots", text=f"⚙️  Executing {function_call_part.name}..."), 
                                console=console, refresh_per_second=10):
                            function_call_result = call_function(function_call_part, verbose=verbose_flag)
                            time.sleep(0.2)  # Brief pause to show the spinner
                    else:
                        # No spinner for non-verbose mode (clean output)
                        function_call_result = call_function(function_call_part, verbose=verbose_flag)

                    # Extract the function response from the result
                    function_response_part = function_call_result.parts[0].function_response

                    # Validate that we got a proper function response
                    if function_response_part is None:
                        raise Exception("Fatal: No function response found in function_call_result")
                    
                    # ========== BEAUTIFUL FUNCTION RESULT DISPLAY ==========
                    # Format and display function results with syntax highlighting and panels
                    if verbose_flag:
                        from rich.panel import Panel
                        from rich.syntax import Syntax
                        
                        result = function_response_part.response
                        if isinstance(result, dict) and 'result' in result:
                            content = result['result']
                            
                            # Syntax highlighting for Python code files
                            if content.startswith('#') and ('def ' in content or 'import ' in content):
                                lines = content.split('\n')[:10]  # Show first 10 lines
                                code_preview = '\n'.join(lines)
                                syntax = Syntax(code_preview, "python", theme="monokai", line_numbers=True)
                                print(Panel(syntax, title="📄 Code Preview"))
                                # Show count of remaining lines if file is longer
                                if len(content.split('\n')) > 10:
                                    remaining = len(content.split('\n')) - 10
                                    print(f"[dim]... and {remaining} more lines[/dim]")
                            
                            # Nice formatted panel for file/directory listings
                            elif 'file_size=' in content:
                                print(Panel(content, title="📁 Directory Contents", style="blue"))
                            
                            # Regular content in green panel with smart truncation
                            else:
                                display_content = content[:300] + "..." if len(content) > 300 else content
                                print(Panel(display_content, title="📄 Function Result", style="green"))
                        else:
                            # Fallback for non-dict results
                            print(Panel(str(result), title="📄 Function Result", style="green"))

                    # ========== ADD FUNCTION RESULT TO CONVERSATION ==========
                    # Convert function result to a message and add to conversation history
                    # This allows the AI to see the results of its function calls in the next iteration
                    tool_message = types.Content(role="tool", parts=function_call_result.parts)
                    messages.append(tool_message)
                    
        except Exception as e:
            # ========== ERROR HANDLING ==========
            # Gracefully handle any errors during processing
            print(f"[red]Error in iteration {iteration}:[/red] {e}")
            break  # Exit the loop on error


# ========== SCRIPT ENTRY POINT ==========
# Standard Python idiom to ensure main() only runs when script is executed directly
# (not when imported as a module)
if __name__ == "__main__":
    main()