#!/usr/bin/env python3
"""
Gemma 3 CLI Chat Application - Educational Minimal Version
A starter kit for local AI chat applications

Required packages:
pip install ollama rich

Usage:
python gemma_chat.py

Educational Philosophy:
- This is a MINIMAL starter kit, not a complete solution
- Extend it yourself: add features, improve UI, add web interface
- Learn by building: multi-user support, web API, mobile interface
- Resource-conscious: designed for low-spec hardware in developing regions

Multi-user Setup (Ubuntu):
- Multiple Ubuntu accounts can access simultaneously
- Each user runs their own instance on different ports
- Scale: 10+ users on a single 70k yen mini PC
- Access: Chrome, smartphone, Chromebook compatible

TODO for Students:
1. Add web interface (Flask/FastAPI)
2. Implement multi-user session management
3. Add authentication system
4. Create mobile-responsive UI
5. Add real-time chat features
6. Implement conversation export
7. Add system monitoring
8. Create API endpoints for external access
"""

import ollama
import sqlite3
import os
import sys
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from rich import print as rprint

class GemmaChat:
    def __init__(self, db_path="chat_history.db"):
        self.console = Console()
        self.db_path = db_path
        self.model = "gemma3:1b"
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database for chat history"""
        conn = sqlite3.connect(self.db_path)
        
        # Check existing table structure
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(chat_history)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if not columns:  # Create table if not exists
            conn.execute('''
                CREATE TABLE chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_message TEXT NOT NULL,
                    assistant_response TEXT NOT NULL
                )
            ''')
            
        conn.commit()
        conn.close()
        
    def check_ollama_connection(self):
        """Check Ollama connection and model availability"""
        try:
            # Direct model test instead of list() to handle version differences
            test_response = ollama.generate(model=self.model, prompt="test")
            if test_response:
                self.console.print(f"[green]✅ Ollama connected - {self.model}[/green]")
                return True
            
        except Exception as e:
            self.console.print(f"[red]❌ Ollama connection error: {e}[/red]")
            
            # TODO: Add automatic model detection and download
            # TODO: Add multiple model support
            # TODO: Add fallback model selection
            
            try:
                models_response = ollama.list()
                self.console.print(f"[yellow]Debug info: {models_response}[/yellow]")
                
                # Handle different response structures
                available_models = []
                if isinstance(models_response, dict):
                    if 'models' in models_response:
                        available_models = [m.get('name', m.get('model', str(m))) for m in models_response['models']]
                    elif 'data' in models_response:
                        available_models = [m.get('name', m.get('model', str(m))) for m in models_response['data']]
                
                self.console.print(f"[yellow]Available models: {available_models}[/yellow]")
                
                # Auto-detect Gemma models
                gemma_models = [m for m in available_models if 'gemma' in str(m).lower()]
                if gemma_models:
                    self.console.print(f"[cyan]Found Gemma models: {gemma_models}[/cyan]")
                    self.model = gemma_models[0]
                    self.console.print(f"[green]Switched to {self.model}[/green]")
                    return True
                    
            except Exception as debug_e:
                self.console.print(f"[red]Debug error: {debug_e}[/red]")
            
            self.console.print("[yellow]💡 Run: ollama pull gemma3:1b[/yellow]")
            return False
    
    def send_message(self, message):
        """Send message to Gemma and get response"""
        try:
            with self.console.status("[bold blue]🤔 Gemma is thinking..."):
                response = ollama.generate(model=self.model, prompt=message)
                assistant_response = response['response']
            
            # Save to history
            self.save_to_history(message, assistant_response)
            return assistant_response
            
        except Exception as e:
            error_msg = f"Error: {e}"
            self.console.print(f"[red]{error_msg}[/red]")
            return error_msg
    
    def save_to_history(self, user_message, assistant_response):
        """Save conversation to SQLite database"""
        # TODO: Add user session tracking
        # TODO: Add conversation threading
        # TODO: Add message categorization
        # TODO: Add full-text search indexing
        
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT INTO chat_history (timestamp, user_message, assistant_response)
            VALUES (?, ?, ?)
        ''', (datetime.now().isoformat(), user_message, assistant_response))
        conn.commit()
        conn.close()
    
    def search_history(self, query):
        """Search chat history with keywords"""
        # TODO: Implement advanced search (date range, regex, categories)
        # TODO: Add search result ranking
        # TODO: Add search highlighting
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute('''
            SELECT timestamp, user_message, assistant_response 
            FROM chat_history 
            WHERE user_message LIKE ? OR assistant_response LIKE ?
            ORDER BY timestamp DESC
            LIMIT 20
        ''', (f'%{query}%', f'%{query}%'))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def show_recent_history(self, limit=10):
        """Show recent chat history"""
        # TODO: Add pagination
        # TODO: Add date filtering
        # TODO: Add export functionality
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute('''
            SELECT timestamp, user_message, assistant_response 
            FROM chat_history 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def display_history(self, history_data, title="History"):
        """Display history in table format"""
        if not history_data:
            self.console.print(f"[yellow]📝 No {title.lower()} found[/yellow]")
            return
        
        table = Table(title=title, show_header=True, header_style="bold blue")
        table.add_column("Time", style="dim", width=20)
        table.add_column("User", style="green", width=30)
        table.add_column("Gemma", style="cyan", width=50)
        
        for timestamp, user_msg, assistant_msg in history_data:
            # Truncate long messages
            user_display = (user_msg[:25] + "...") if len(user_msg) > 25 else user_msg
            assistant_display = (assistant_msg[:45] + "...") if len(assistant_msg) > 45 else assistant_msg
            
            table.add_row(
                timestamp.split('T')[1][:8],  # Time only
                user_display,
                assistant_display
            )
        
        self.console.print(table)
    
    def display_welcome(self):
        """Display welcome message with educational notes"""
        welcome_text = """
🤖 **Gemma 3 CLI Chat - Educational Starter Kit**

**This is a MINIMAL version. Extend it yourself!**

**Commands:**
- `/help` - Show help
- `/history` - Show recent history
- `/search <keyword>` - Search history
- `/clear` - Clear screen
- `/exit` or `/quit` - Exit

**Educational Goals:**
- Learn Python, SQLite, Rich library
- Understand AI integration patterns
- Practice CLI application development
- Build multi-user systems

**Expansion Ideas:**
- Web interface (Flask/FastAPI)
- Multi-user chat rooms
- Mobile-responsive UI
- Real-time features
- API endpoints
- Authentication system

**Multi-User Setup:**
- Experiment with SSH access from various devices
- Test limits and learn resource management
- Perfect for hands-on learning environments
        """
        
        panel = Panel(
            Markdown(welcome_text),
            title="[bold blue]Educational AI Chat Starter[/bold blue]",
            border_style="blue"
        )
        self.console.print(panel)
    
    def display_help(self):
        """Display help with expansion hints"""
        help_table = Table(title="Commands & Extension Ideas", show_header=True, header_style="bold magenta")
        help_table.add_column("Command", style="green")
        help_table.add_column("Description", style="white")
        help_table.add_column("TODO: Extend with...", style="yellow")
        
        commands = [
            ("/help", "Show this help", "Context-sensitive help, tutorials"),
            ("/history [num]", "Show recent history", "Pagination, date filters, export"),
            ("/search <keyword>", "Search history", "Advanced search, regex, ranking"),
            ("/clear", "Clear screen", "Theme switching, layout options"),
            ("/exit, /quit", "Exit app", "Session saving, graceful shutdown"),
            ("Regular message", "Chat with Gemma", "Conversation threading, context")
        ]
        
        for cmd, desc, todo in commands:
            help_table.add_row(cmd, desc, todo)
        
        self.console.print(help_table)
        
        self.console.print("\n[bold cyan]🚀 Next Steps for Students:[/bold cyan]")
        self.console.print("1. Add web interface using Flask or FastAPI")
        self.console.print("2. Implement user authentication and sessions")
        self.console.print("3. Create mobile-responsive design")
        self.console.print("4. Add real-time chat features with WebSockets")
        self.console.print("5. Build API endpoints for external access")
        self.console.print("6. Implement conversation export (JSON, CSV, PDF)")
        self.console.print("7. Add system monitoring and resource usage")
        self.console.print("8. Create multi-language support")
    
    def run(self):
        """Main application loop"""
        # Connection check
        if not self.check_ollama_connection():
            return
        
        self.display_welcome()
        
        try:
            while True:
                # User input
                user_input = Prompt.ask("\n[bold green]You[/bold green]").strip()
                
                if not user_input:
                    continue
                
                # Command processing
                if user_input.startswith('/'):
                    command_parts = user_input.split(' ', 1)
                    command = command_parts[0].lower()
                    args = command_parts[1] if len(command_parts) > 1 else ""
                    
                    if command in ['/exit', '/quit']:
                        self.console.print("[yellow]👋 Goodbye! Keep building![/yellow]")
                        break
                    
                    elif command == '/help':
                        self.display_help()
                    
                    elif command == '/history':
                        try:
                            limit = int(args) if args else 10
                            history = self.show_recent_history(limit)
                            self.display_history(history, f"Recent History ({limit} items)")
                        except ValueError:
                            self.console.print("[red]❌ Please enter a number: /history 20[/red]")
                    
                    elif command == '/search':
                        if not args:
                            self.console.print("[red]❌ Please enter search term: /search keyword[/red]")
                        else:
                            results = self.search_history(args)
                            self.display_history(results, f"Search Results: '{args}'")
                    
                    elif command == '/clear':
                        os.system('clear' if os.name == 'posix' else 'cls')
                        self.display_welcome()
                    
                    else:
                        self.console.print(f"[red]❌ Unknown command: {command}[/red]")
                        self.console.print("[yellow]💡 Type /help for available commands[/yellow]")
                
                else:
                    # Regular chat
                    response = self.send_message(user_input)
                    
                    # Display Gemma's response
                    response_panel = Panel(
                        Markdown(response),
                        title="[bold cyan]🤖 Gemma[/bold cyan]",
                        border_style="cyan"
                    )
                    self.console.print(response_panel)
        
        except KeyboardInterrupt:
            self.console.print("\n[yellow]👋 Interrupted with Ctrl+C[/yellow]")
        except Exception as e:
            self.console.print(f"\n[red]❌ Unexpected error: {e}[/red]")

def main():
    """Main function with educational information"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("""
Gemma 3 CLI Chat Application - Educational Starter Kit

This is a MINIMAL version designed for learning and extension.

Usage:
    python gemma_chat.py

Prerequisites:
    pip install ollama rich

Ollama Setup:
    1. Install Ollama: https://ollama.ai/
    2. Download Gemma 3: ollama pull gemma3:1b
    3. Start Ollama server: ollama serve

Educational Philosophy:
    - Learn by doing, not by using complete solutions
    - Build features yourself: web UI, multi-user, authentication
    - Understand the fundamentals before adding complexity
    - Resource-conscious design for developing regions

Multi-User Setup (Ubuntu):
    - Each Ubuntu account can run their own instance
    - Access from any device: Chrome, smartphone, Chromebook
    - Concurrent users: 10+ on a 70k yen mini PC
    - Perfect for educational institutions with limited resources

TODO for Students:
    1. Add Flask/FastAPI web interface
    2. Implement WebSocket for real-time chat
    3. Create user authentication system
    4. Build mobile-responsive UI
    5. Add conversation export features
    6. Implement advanced search
    7. Create API documentation
    8. Add monitoring and logging

Remember: This is a foundation, not a destination!
            """)
            return
    
    app = GemmaChat()
    app.run()

if __name__ == "__main__":
    main()
