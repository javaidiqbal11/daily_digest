"""
Code Assistant Agent
A deep agent specialized for coding tasks, debugging, and software engineering.
"""

from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

from config import config
from utils.prompts import CODE_AGENT_PROMPT
from utils.logger import logger
from tools.search_tools import internet_search
from tools.file_tools import save_report, read_report, list_reports


def create_code_agent(
    model: str | None = None,
    enable_memory: bool = True,
):
    """
    Create a code assistant deep agent.
    
    This agent is specialized for:
    - Writing clean, production-ready code
    - Debugging and troubleshooting
    - Code review and explanations
    - Software architecture design
    - Searching for documentation and best practices
    
    Args:
        model: LLM model identifier. Defaults to config.
        enable_memory: Whether to enable persistent memory
        
    Returns:
        A compiled LangGraph deep agent ready to invoke
    """
    logger.info("💻 Creating [bold yellow]Code Agent[/bold yellow]...")

    model_id = model or config.llm.default_model

    # Code agent tools - focused subset
    tools = [
        internet_search,
        save_report,
        read_report,
        list_reports,
    ]

    agent_kwargs = {
        "name": "code-agent",
        "model": model_id,
        "tools": tools,
        "system_prompt": CODE_AGENT_PROMPT,
    }

    if enable_memory:
        checkpointer = MemorySaver()
        agent_kwargs["checkpointer"] = checkpointer
        logger.info("  🧠 Memory enabled")

    agent = create_deep_agent(**agent_kwargs)
    
    logger.info(f"  🤖 Model: [bold]{model_id}[/bold]")
    logger.info(f"  🛠️  Tools: {len(tools)} loaded")
    logger.info("✅ Code Agent [bold green]ready[/bold green]!\n")
    
    return agent
