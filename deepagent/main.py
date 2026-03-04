"""
DeepAgent CLI - Interactive Command Line Interface
A rich terminal interface for interacting with the DeepAgent system.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

from config import config
from utils.logger import logger
from utils.helpers import create_session_id, extract_final_response


console = Console()

# ─── Banner ──────────────────────────────────────────────────────────────────
BANNER = r"""
[bold cyan]
  ____                    _                    _   
 |  _ \  ___  ___ _ __   / \   __ _  ___ _ __ | |_ 
 | | | |/ _ \/ _ \ '_ \ / _ \ / _` |/ _ \ '_ \| __|
 | |_| |  __/  __/ |_) / ___ \ (_| |  __/ | | | |_ 
 |____/ \___|\___| .__/_/   \_\__, |\___|_| |_|\__|
                 |_|          |___/                 
[/bold cyan]
[dim]Powered by LangChain DeepAgents • Planning • Sub-Agents • File System[/dim]
"""

AGENT_TYPES = {
    "research": ("🔬 Research Agent", "Deep multi-step research with web search"),
    "code": ("💻 Code Agent", "Programming assistant & software engineering"),
    "general": ("🌐 General Agent", "Versatile multi-purpose assistant"),
}


def display_banner():
    """Display the application banner."""
    console.print(BANNER)
    console.print()


def select_agent_type() -> str:
    """Prompt user to select an agent type."""
    console.print(Panel(
        "\n".join(
            f"  [bold]{key}[/bold] - {emoji} {desc}"
            for key, (emoji, desc) in AGENT_TYPES.items()
        ),
        title="[bold]Select Agent Type[/bold]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print()
    
    choice = Prompt.ask(
        "[bold cyan]Agent type[/bold cyan]",
        choices=list(AGENT_TYPES.keys()),
        default=config.agent.default_agent_type,
    )
    return choice


def create_agent(agent_type: str):
    """Create the selected agent type."""
    if agent_type == "research":
        from agents.research_agent import create_research_agent
        return create_research_agent()
    elif agent_type == "code":
        from agents.code_agent import create_code_agent
        return create_code_agent()
    elif agent_type == "general":
        from agents.general_agent import create_general_agent
        return create_general_agent()
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")


def run_agent_with_streaming(agent, user_input: str, thread_id: str) -> str:
    """
    Run the agent and display streaming output.
    
    Args:
        agent: The compiled deep agent
        user_input: User's message
        thread_id: Conversation thread ID for memory
        
    Returns:
        The agent's final response text
    """
    config_dict = {"configurable": {"thread_id": thread_id}}
    
    final_response = ""
    
    try:
        with console.status("[bold cyan]🤔 Thinking...[/bold cyan]", spinner="dots"):
            result = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config=config_dict,
            )
        
        final_response = extract_final_response(result)
        
    except Exception as e:
        logger.error(f"Agent error: {e}")
        final_response = f"❌ An error occurred: {str(e)}"
    
    return final_response


def display_response(response: str):
    """Display the agent's response with rich formatting."""
    console.print()
    console.print(Panel(
        Markdown(response),
        title="[bold green]🤖 Agent Response[/bold green]",
        border_style="green",
        padding=(1, 2),
    ))
    console.print()


def main():
    """Main CLI entry point."""
    display_banner()
    
    # Validate API keys
    warnings = config.validate_api_keys()
    for warning in warnings:
        console.print(f"[yellow]{warning}[/yellow]")
    if warnings:
        console.print()

    # Select agent type
    agent_type = select_agent_type()
    emoji, desc = AGENT_TYPES[agent_type]
    console.print(f"\n{emoji} Starting [bold]{desc}[/bold]...\n")
    
    # Create agent
    try:
        agent = create_agent(agent_type)
    except Exception as e:
        console.print(f"[bold red]❌ Failed to create agent: {e}[/bold red]")
        console.print("[dim]Check your API keys in the .env file[/dim]")
        sys.exit(1)
    
    # Create session
    session_id = create_session_id()
    console.print(Panel(
        f"[dim]Session: {session_id}[/dim]\n"
        f"[dim]Type [bold]quit[/bold] or [bold]exit[/bold] to end the conversation[/dim]\n"
        f"[dim]Type [bold]clear[/bold] to start a new conversation thread[/dim]\n"
        f"[dim]Type [bold]reports[/bold] to list saved reports[/dim]",
        title=f"[bold]{emoji} {desc}[/bold]",
        border_style="cyan",
        padding=(1, 2),
    ))
    console.print()
    
    # Chat loop
    thread_id = session_id
    
    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]")
            
            if not user_input.strip():
                continue
                
            # Handle special commands
            if user_input.strip().lower() in ("quit", "exit", "q"):
                console.print("\n[bold cyan]👋 Goodbye! Thanks for using DeepAgent.[/bold cyan]\n")
                break
                
            if user_input.strip().lower() == "clear":
                thread_id = create_session_id()
                console.print("[dim]🔄 Started new conversation thread[/dim]\n")
                continue
                
            if user_input.strip().lower() == "reports":
                from tools.file_tools import list_reports
                result = list_reports()
                console.print(Markdown(result))
                console.print()
                continue
            
            # Run agent
            response = run_agent_with_streaming(agent, user_input, thread_id)
            display_response(response)
            
        except KeyboardInterrupt:
            console.print("\n\n[bold cyan]👋 Interrupted. Goodbye![/bold cyan]\n")
            break
        except Exception as e:
            console.print(f"\n[bold red]❌ Error: {e}[/bold red]\n")
            logger.error(f"CLI error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
