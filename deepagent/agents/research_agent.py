"""
Deep Research Agent
A fully-configured research agent with web search, sub-agents, and file management.
"""

from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

from config import config
from utils.prompts import RESEARCH_AGENT_PROMPT
from utils.logger import logger
from tools.search_tools import internet_search, news_search
from tools.file_tools import save_report, read_report, list_reports
from tools.analysis_tools import analyze_text, compare_sources
from subagents.summarizer import get_summarizer_config
from subagents.fact_checker import get_fact_checker_config
from subagents.writer import get_writer_config


def create_research_agent(
    model: str | None = None,
    enable_memory: bool = True,
    enable_subagents: bool = True,
):
    """
    Create a fully-configured deep research agent.
    
    This agent is equipped with:
    - Web search (Tavily) for real-time information
    - News search for current events  
    - File management for saving/reading reports
    - Text analysis tools
    - Sub-agents for summarization, fact-checking, and writing
    - Persistent memory across conversations
    
    Args:
        model: LLM model identifier (e.g., "openai:gpt-4o", "anthropic:claude-sonnet-4-6").
               Defaults to config.
        enable_memory: Whether to enable persistent memory via checkpointer
        enable_subagents: Whether to include specialized sub-agents
        
    Returns:
        A compiled LangGraph deep agent ready to invoke
    """
    logger.info("🔬 Creating [bold cyan]Research Agent[/bold cyan]...")

    # Resolve model
    model_id = model or config.llm.default_model

    # Assemble tools
    tools = [
        internet_search,
        news_search,
        save_report,
        read_report,
        list_reports,
        analyze_text,
        compare_sources,
    ]

    # Configure sub-agents
    subagents = []
    if enable_subagents:
        subagents = [
            get_summarizer_config(),
            get_fact_checker_config(),
            get_writer_config(),
        ]
        logger.info(f"  📦 Loaded {len(subagents)} sub-agents: "
                     f"{', '.join(s['name'] for s in subagents)}")

    # Build agent kwargs
    agent_kwargs = {
        "name": "research-agent",
        "model": model_id,
        "tools": tools,
        "system_prompt": RESEARCH_AGENT_PROMPT,
    }

    # Add sub-agents if enabled
    if subagents:
        agent_kwargs["subagents"] = subagents

    # Add memory/checkpointer if enabled
    if enable_memory:
        checkpointer = MemorySaver()
        agent_kwargs["checkpointer"] = checkpointer
        logger.info("  🧠 Memory enabled (MemorySaver)")

    # Create the deep agent
    agent = create_deep_agent(**agent_kwargs)
    
    logger.info(f"  🤖 Model: [bold]{model_id}[/bold]")
    logger.info(f"  🛠️  Tools: {len(tools)} loaded")
    logger.info("✅ Research Agent [bold green]ready[/bold green]!\n")
    
    return agent
