"""
General Purpose Agent
A versatile deep agent that can handle a wide variety of tasks.
"""

from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

from config import config
from utils.prompts import GENERAL_AGENT_PROMPT
from utils.logger import logger
from tools.search_tools import internet_search, news_search
from tools.file_tools import save_report, read_report, list_reports
from tools.analysis_tools import analyze_text
from subagents.summarizer import get_summarizer_config


def create_general_agent(
    model: str | None = None,
    enable_memory: bool = True,
    custom_prompt: str | None = None,
    custom_tools: list | None = None,
):
    """
    Create a general-purpose deep agent.
    
    This is the most flexible agent type, suitable for a wide variety
    of tasks including research, analysis, writing, and more.
    
    Args:
        model: LLM model identifier. Defaults to config.
        enable_memory: Whether to enable persistent memory
        custom_prompt: Optional custom system prompt to override default
        custom_tools: Optional additional tools to include
        
    Returns:
        A compiled LangGraph deep agent ready to invoke
    """
    logger.info("🌐 Creating [bold magenta]General Agent[/bold magenta]...")

    model_id = model or config.llm.default_model

    # Base tools
    tools = [
        internet_search,
        news_search,
        save_report,
        read_report,
        list_reports,
        analyze_text,
    ]

    # Add custom tools if provided
    if custom_tools:
        tools.extend(custom_tools)
        logger.info(f"  ➕ Added {len(custom_tools)} custom tool(s)")

    # Sub-agents
    subagents = [get_summarizer_config()]

    agent_kwargs = {
        "name": "general-agent",
        "model": model_id,
        "tools": tools,
        "system_prompt": custom_prompt or GENERAL_AGENT_PROMPT,
        "subagents": subagents,
    }

    if enable_memory:
        checkpointer = MemorySaver()
        agent_kwargs["checkpointer"] = checkpointer
        logger.info("  🧠 Memory enabled")

    agent = create_deep_agent(**agent_kwargs)
    
    logger.info(f"  🤖 Model: [bold]{model_id}[/bold]")
    logger.info(f"  🛠️  Tools: {len(tools)} loaded")
    logger.info("✅ General Agent [bold green]ready[/bold green]!\n")
    
    return agent
