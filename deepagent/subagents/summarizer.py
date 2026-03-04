"""
Summarizer Sub-Agent
Specialized sub-agent for condensing and summarizing large amounts of information.
"""

from utils.prompts import SUMMARIZER_PROMPT


def get_summarizer_config() -> dict:
    """
    Get the configuration dictionary for the summarizer sub-agent.
    
    This sub-agent is designed to take large amounts of research data
    and produce concise, accurate summaries.
    
    Returns:
        Sub-agent configuration dictionary for use with create_deep_agent
    """
    return {
        "name": "summarizer",
        "description": (
            "A specialist at summarizing large amounts of information "
            "into clear, concise summaries. Delegate to this agent when "
            "you need to condense research findings, long documents, or "
            "multiple sources into a brief overview."
        ),
        "system_prompt": SUMMARIZER_PROMPT,
        "tools": [],  # Summarizer works with provided text, no external tools needed
    }
