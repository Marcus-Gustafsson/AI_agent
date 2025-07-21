"""
AI Agent TUI (Terminal User Interface)

This module provides a beautiful terminal user interface for interacting with
the AI agent using Textual. Features include real-time chat, verbose mode toggle,
and beautiful formatting of agent responses.
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Header, Footer, Input, RichLog, Switch, Static
from textual.binding import Binding
from textual import events
import asyncio
from datetime import datetime

# Import your existing main logic
from main import client, config
from google.genai import types
import functions.function_schemas
from functions.call_function import call_function


class AIAgentTUI(App):
    """A Textual app for the AI Agent interface."""
    
    CSS = """
    .chat-container {
        height: 1fr;
        border: solid $primary;
        margin: 1;
        padding: 1;
    }

    .input-container {
        height: auto;
        margin: 1;
        border: solid $secondary;
        padding: 1;
    }

    .user-message {
        background: $primary 20%;
        color: $text;
        margin: 1 0;
        padding: 1;
    }

    .agent-message {
        background: $secondary 20%;
        color: $text;
        margin: 1 0;
        padding: 1;
    }

    .system-message {
        background: $warning 20%;
        color: $text;
        margin: 1 0;
        padding: 1;
    }

    RichLog {
        scrollbar-gutter: stable;
        overflow-x: hidden;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+l", "clear", "Clear Chat"),
        Binding("f1", "toggle_verbose", "Toggle Verbose"),
    ]
    
    def __init__(self):
        super().__init__()
        self.messages = []
        self.verbose_mode = False
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        
        with Container(classes="chat-container"):
            yield RichLog(id="chat_log", highlight=True, markup=True, wrap=True)
        
        with Container(classes="input-container"):
            yield Input(
                placeholder="Type your message to the AI agent...",
                id="message_input"
            )
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when app starts."""
        self.query_one("#chat_log").write("🤖 AI Agent Ready! Type your message below.")
        self.query_one("#message_input").focus()
    
    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Called when user submits input."""
        if event.input.id == "message_input":
            message = event.value.strip()
            if message:
                await self.process_user_message(message)
                event.input.value = ""
    
    def action_toggle_verbose(self) -> None:
        """Toggle verbose mode."""
        self.verbose_mode = not self.verbose_mode
        mode = "ON" if self.verbose_mode else "OFF"
        self.query_one("#chat_log").write(f"[yellow]🔧 Verbose mode: {mode}[/yellow]")
    
    async def process_user_message(self, user_message: str) -> None:
        """Process user message and get AI response."""
        chat_log = self.query_one("#chat_log")
        
        # Display user message
        timestamp = datetime.now().strftime("%H:%M:%S")
        chat_log.write(f"[bold blue]👤 You ({timestamp}):[/bold blue] {user_message}")
        
        # Initialize conversation
        self.messages = [
            types.Content(role="user", parts=[types.Part(text=user_message)])
        ]
        
        # Available functions
        available_functions = types.Tool(function_declarations=functions.function_schemas.ALL_SCHEMAS)
        
        try:
            # Agent loop
            for iteration in range(20):
                # Generate AI response
                response = client.models.generate_content(
                    model=config.model_name,
                    contents=self.messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions],
                        system_instruction=config.system_prompt
                    ),
                )
                
                # Add AI response to conversation
                for candidate in response.candidates:
                    self.messages.append(candidate.content)
                
                # Check if AI is done
                if not response.function_calls:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    chat_log.write(f"[bold green]🤖 Agent ({timestamp}):[/bold green] {response.text}")
                    break
                
                # Show verbose information
                if self.verbose_mode:
                    chat_log.write(f"[cyan]🔄 Iteration {iteration}[/cyan]")
                    
                    # Show AI thinking
                    for candidate in response.candidates:
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text and part.text.strip():
                                thinking = part.text[:150] + "..." if len(part.text) > 150 else part.text
                                chat_log.write(f"[yellow]💭 Thinking: {thinking}[/yellow]")
                                break
                    
                    # Show function calls
                    if response.function_calls:
                        functions_called = [fc.name for fc in response.function_calls]
                        chat_log.write(f"[magenta]🔧 Calling: {', '.join(functions_called)}[/magenta]")
                
                # Execute function calls
                if response.function_calls:
                    for function_call_part in response.function_calls:
                        if self.verbose_mode:
                            chat_log.write(f"[dim]⚙️ Executing {function_call_part.name}...[/dim]")
                        
                        # Call function
                        function_call_result = call_function(function_call_part, verbose=False)
                        function_response_part = function_call_result.parts[0].function_response
                        
                        if function_response_part is None:
                            chat_log.write("[red]❌ Error: No function response[/red]")
                            continue
                        
                        # Show function result in verbose mode
                        if self.verbose_mode:
                            result = function_response_part.response
                            if isinstance(result, dict) and 'result' in result:
                                content = result['result']
                                preview = content[:100] + "..." if len(content) > 100 else content
                                chat_log.write(f"[green]📄 Result: {preview}[/green]")
                        
                        # Add to conversation
                        tool_message = types.Content(role="tool", parts=function_call_result.parts)
                        self.messages.append(tool_message)
        
        except Exception as e:
            timestamp = datetime.now().strftime("%H:%M:%S")
            chat_log.write(f"[red]❌ Error ({timestamp}): {str(e)}[/red]")
    
    def action_clear(self) -> None:
        """Clear the chat log."""
        self.query_one("#chat_log").clear()
        self.query_one("#chat_log").write("🤖 AI Agent Ready! Type your message below.")
        self.messages = []
    
    def action_toggle_verbose(self) -> None:
        """Toggle verbose mode."""
        self.verbose_mode = not self.verbose_mode
        mode = "ON" if self.verbose_mode else "OFF"
        self.query_one("#chat_log").write(f"[yellow]🔧 Verbose mode: {mode}[/yellow]")


def run_tui():
    """Run the TUI application."""
    app = AIAgentTUI()
    app.title = "AI Agent TUI"
    app.sub_title = "Interactive AI Assistant"
    app.run()


if __name__ == "__main__":
    run_tui()