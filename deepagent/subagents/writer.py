"""
Writer Sub-Agent
Specialized sub-agent for producing polished reports and documents.
"""

from utils.prompts import WRITER_PROMPT


def get_writer_config() -> dict:
    """
    Get the configuration dictionary for the writer sub-agent.
    
    This sub-agent transforms raw notes and research findings
    into polished, well-structured reports and documents.
    
    Returns:
        Sub-agent configuration dictionary for use with create_deep_agent
    """
    return {
        "name": "writer",
        "description": (
            "A professional writer and editor. Delegate to this agent when "
            "you have gathered all your research and notes and need them "
            "transformed into a polished, well-structured report or document. "
            "Provide all raw material and the writer will produce the final output."
        ),
        "system_prompt": WRITER_PROMPT,
        "tools": [],  # Writer works with provided content
    }
