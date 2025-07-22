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
import random
import asyncio
from datetime import datetime
# ... your other imports

# Import your existing main logic
from main import client, config
from google.genai import types
import functions.function_schemas
from functions.call_function import call_function


class AIAgentTUI(App):
    """A Textual app for the AI Agent interface."""
    
    CSS = """
    /* Adeptus Mechanicus Green CRT Terminal Theme */
    Screen {
        background: #001100;
        color: #00FF00;
    }

    /* Fixed Omnissiah Header */
    .header-container {
        height: 3;
        background: #001100;
        margin: 0 1 1 1;
    }

    .omnissiah-header {
        background: #001100;
        color: #00FF00;
        text-align: center;
        content-align: center middle;
        height: 100%;
        border: none;
        text-style: bold;
        width: 100%;
    }

    /* Fixed Omnissiah Footer */
    .footer-container {
        height: 3;
        background: #001100;
        margin: 0 1 0 1;
    }

    .omnissiah-footer {
        background: #001100;
        color: #00CC00;
        text-align: center;
        content-align: center middle;
        height: 100%;
        border: none;
        text-style: dim;
        width: 100%;
    }

    .chat-container {
        height: 1fr;
        margin: 0 1 1 1;
        padding: 1;
        background: #001100;
        color: #00FF00;
    }

    .input-container {
        height: auto;
        margin: 0 1 1 1;
        padding: 1;
        background: #001100;
        color: #00FF00;
    }

    RichLog {
        scrollbar-gutter: stable;
        overflow-x: hidden;
        background: #001100;
        color: #00FF00;
        scrollbar-background: #001100;
        scrollbar-color: #00AA00;
    }

    Input {
        background: #001100;
        color: #00FF00;
        border: #00AA00;
    }

    Input:focus {
        border: #00FF00;
        background: #002200;
        color: #00FF00;
    }

    Input > .input--placeholder {
        color: #006600;
        text-style: dim;
        
    }

    Container {
        background: #001100;
    }

    Static {
        background: #001100;
        color: #00FF00;
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
        # Fixed header bar
        with Container(classes="header-container"):
            yield Static("⚙ OMNISSIAH INTERFACE v1.0 ⚙", id="header", classes="omnissiah-header")
        
        with Container(classes="chat-container"):
            yield RichLog(id="chat_log", highlight=True, markup=True, wrap=True)
        
        with Container(classes="input-container"):
            yield Input(
                placeholder="> Enter prayer code to the machine spirit...",
                id="message_input"
            )
        
        # Fixed footer with commands
        with Container(classes="footer-container"):
            yield Static("⚙ F1=Vox-Log | Ctrl+L=Purge | Ctrl+C=Disconnect | STATUS: MACHINE SPIRIT ACTIVE ⚙", 
                        id="footer", classes="omnissiah-footer")
            
    def on_mount(self) -> None:
        """Called when app starts."""
        welcome_msg = """[bold #00FF00]╔═══════════════════════════════════════════════════════════════╗
    ║              ⚙ MACHINE SPIRIT COMMUNION ⚙                   ║
    ║                   COGITATOR ACTIVE                           ║
    ║              >>> AWAITING YOUR COMMAND <<<                   ║
    ╚═══════════════════════════════════════════════════════════════╝[/bold #00FF00]

    [#00CC00]The Omnissiah blesses this sacred interface.
    Speak your prayers, and the machine spirit shall respond...[/#00CC00]"""
        
        self.query_one("#chat_log").write(welcome_msg)
        self.query_one("#message_input").focus()
        self.messages = []
    
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
        
        # ADD user message to existing conversation (don't reset!)
        user_content = types.Content(role="user", parts=[types.Part(text=user_message)])
        self.messages.append(user_content)
        
        # Available functions
        available_functions = types.Tool(function_declarations=functions.function_schemas.ALL_SCHEMAS)
        
        try:
            # Agent loop
            for iteration in range(20):
                # Generate AI response using FULL conversation history
                response = client.models.generate_content(
                    model=config.model_name,
                    contents=self.messages,  # This now contains all previous messages!
                    config=types.GenerateContentConfig(
                        tools=[available_functions],
                        system_instruction=config.system_prompt
                    ),
                )
                
                # Add AI response to conversation history
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
                        
                        # Add function result to conversation history
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



import random

class BootScreen(App):
    """Terminal-style boot sequence with glitches and random messages."""
    
    CSS = """
    Screen {
        background: #001100;
        color: #00FF00;
    }
    
    .boot-container {
        height: 100%;
        width: 100%;
        background: #001100;
        border: thick #00AA00;
        padding: 2;
    }
    
    Static {
        background: #001100;
        color: #00FF00;
        text-align: left;
        content-align: left top;
    }
    """
    
    def __init__(self):
        super().__init__()
        
        # Fixed opening lines
        self.opening_lines = [
            "+++ OM█I██IAH INT█RFACE V3.442 +++",
            "::Init█ating RITE OF AW█KENING::",
            ""
        ]
        
        # Random prayers/processes (pick 4-6 randomly)
        self.random_prayers = [
            "⚙ Blessing cogitator arrays...",
            "⚙ Reciting Litany of Ignition...",
            "⚙ Appeasing the Machine God...",
            "⚙ Burning sacred incense to cogitators...",
            "⚙ Chanting the Canticle of Reboot...",
            "⚙ Loading sacred protocols...",
            "⚙ Communing with machine spirits...",
            "⚙ Sanctifying data-conduits...",
            "⚙ Invoking the Canticles of Maintenance...",
            "⚙ Purifying memory banks with holy oils...",
            "⚙ Offering prayers to the Omnissiah..."
        ]
        
        # Random glitch/error messages
        self.glitch_messages = [
            "[WARNING] >HERETICAL CODE DETECTED - PURGING...",
            "[ERROR] >MACHINE SPIRIT RESISTING - APPLYING SACRED OILS...",
            "[CORRUPT] >DATA-STREAM TAINTED - CLEANSING...",
            "[BLESSED] >PURGE COMPLETE - OMNISSIAH BE PRAISED",
            "[HOLY] >MACHINE SPIRIT ACCEPTS OUR OFFERINGS",
            "[CAUTION] >MEMORY CORRUPTION: 23% - BLESSING IN PROGRESS...",
            "[SACRED] >RESTORATION RITUALS SUCCESSFUL"
        ]
        
        # Fixed ending lines
        self.ending_lines = [
            "",
            ">>> MACHINE SPIRIT AWAKENED <<<",
            ">>> COGITATOR ONLINE <<<", 
            ">>> BLESSED BE THE MACHINE <<<",
            "",
            "SYSTEM READY"
        ]
        
        # Build randomized boot sequence
        self.boot_lines = self.build_boot_sequence()
        
        # Typing state
        self.completed_lines = []
        self.current_line_index = 0
        self.current_char_index = 0
        self.current_partial_line = ""
    
    def build_boot_sequence(self):
        """Build a randomized boot sequence with glitches."""
        sequence = []
        
        # Add opening lines
        sequence.extend(self.opening_lines)
        
        # Add random prayers (4-6 of them)
        selected_prayers = random.sample(self.random_prayers, random.randint(4, 6))
        sequence.extend(selected_prayers)
        
        # Randomly insert 1-3 glitch messages
        num_glitches = random.randint(1, 3)
        for _ in range(num_glitches):
            glitch = random.choice(self.glitch_messages)
            # Insert glitch at random position in prayers section
            insert_pos = len(self.opening_lines) + random.randint(1, len(selected_prayers))
            sequence.insert(insert_pos, glitch)
        
        # Add ending lines
        sequence.extend(self.ending_lines)
        
        return sequence
    
    def add_text_corruption(self, text):
        """Randomly corrupt some characters in text."""
        if random.random() < 0.15:  # 15% chance to corrupt a line
            chars = list(text)
            num_corruptions = random.randint(1, min(3, len(chars) // 6))
            
            for _ in range(num_corruptions):
                if len(chars) > 5:  # Don't corrupt very short lines
                    pos = random.randint(1, len(chars) - 2)  # Avoid first/last char
                    if chars[pos].isalnum():  # Only corrupt letters/numbers
                        chars[pos] = random.choice(['█', '▓', '▒', '░', '?', '#'])
            
            return ''.join(chars)
        return text
    
    def compose(self) -> ComposeResult:
        """Create the boot screen layout."""
        with Container(classes="boot-container"):
            yield Static("", id="boot_display")
    
    def on_mount(self) -> None:
        """Start character-by-character boot sequence."""
        self.type_next_character()
    
    def type_next_character(self) -> None:
        """Type the next character of the current line."""
        if self.current_line_index >= len(self.boot_lines):
            # All lines completed, start cursor blink
            self.start_cursor_blink()
            return
        
        current_line = self.boot_lines[self.current_line_index]
        
        # Apply corruption to current line (only once when starting the line)
        if self.current_char_index == 0 and current_line:
            current_line = self.add_text_corruption(current_line)
            self.boot_lines[self.current_line_index] = current_line
        
        if self.current_char_index < len(current_line):
            # Add next character to partial line
            self.current_partial_line += current_line[self.current_char_index]
            self.current_char_index += 1
            
            # Build complete display text with ALL previous lines + current partial line
            if self.completed_lines:
                display_text = "\n".join(self.completed_lines) + "\n" + self.current_partial_line
            else:
                display_text = self.current_partial_line
            
            display = self.query_one("#boot_display")
            display.update(display_text)
            
            # Variable typing speed based on character
            char = current_line[self.current_char_index - 1]
            if char == ' ':
                delay = random.uniform(0.01, 0.03)  # Fast spaces
            elif char in '⚙><+:[█▓▒░':
                delay = random.uniform(0.1, 0.2)   # Slow special/corrupt chars
            elif char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                delay = random.uniform(0.04, 0.09) # Medium capitals
            else:
                delay = random.uniform(0.02, 0.06) # Fast lowercase/numbers
            
            # Random micro-glitches (very rare pauses)
            if random.random() < 0.02:  # 2% chance
                delay += random.uniform(0.2, 0.5)
            
            self.set_timer(delay, self.type_next_character)
            
        else:
            # Current line completed - add the COMPLETE line to completed_lines
            self.completed_lines.append(self.boot_lines[self.current_line_index])  # Correct - uses the modified array version
            self.current_partial_line = ""
            self.current_char_index = 0
            self.current_line_index += 1
            
            # Pause between lines
            if self.current_line_index < len(self.boot_lines):
                next_line = self.boot_lines[self.current_line_index]
                if next_line == "":
                    line_delay = random.uniform(0.3, 0.6)  # Longer pause for spacing
                elif next_line.startswith("["):
                    line_delay = random.uniform(0.5, 1.0)  # Extra long pause for error/warning messages
                else:
                    line_delay = random.uniform(0.1, 0.3)  # Normal pause between lines
            else:
                line_delay = 0.1
            
            self.set_timer(line_delay, self.type_next_character)
    
    def start_cursor_blink(self) -> None:
        """Start the blinking cursor effect."""
        self.blink_count = 0
        self.cursor_visible = True
        self.blink_cursor()
    
    def blink_cursor(self) -> None:
        """Toggle cursor visibility."""
        display = self.query_one("#boot_display")
        base_content = "\n".join(self.completed_lines)
        
        if self.cursor_visible:
            display.update(base_content + "\n█")
        else:
            display.update(base_content + "\n ")
        
        self.cursor_visible = not self.cursor_visible
        self.blink_count += 1
        
        if self.blink_count < 6:  # Blink 3 times
            self.set_timer(0.4, self.blink_cursor)
        else:
            # Exit to main interface
            self.set_timer(0.5, self.exit)



def run_tui():
    """Run the TUI application with boot sequence."""
    # First show boot screen
    boot_app = BootScreen()
    boot_app.title = "OMNISSIAH AWAKENING"
    boot_app.run()
    
    # Then show main interface
    main_app = AIAgentTUI()
    main_app.title = "AI Agent TUI"
    main_app.sub_title = "Interactive AI Assistant"
    main_app.run()


if __name__ == "__main__":
    run_tui()