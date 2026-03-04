"""
Fact Checker Sub-Agent
Specialized sub-agent for verifying claims and information accuracy.
"""

from utils.prompts import FACT_CHECKER_PROMPT
from tools.search_tools import internet_search


def get_fact_checker_config() -> dict:
    """
    Get the configuration dictionary for the fact-checker sub-agent.
    
    This sub-agent verifies claims, cross-references information,
    and rates confidence levels for accuracy.
    
    Returns:
        Sub-agent configuration dictionary for use with create_deep_agent
    """
    return {
        "name": "fact-checker",
        "description": (
            "A specialist at verifying facts and claims. Delegate to this "
            "agent when you need to verify specific claims, cross-reference "
            "data points, or check the accuracy of information from research. "
            "Has access to web search for verification."
        ),
        "system_prompt": FACT_CHECKER_PROMPT,
        "tools": [internet_search],  # Needs search to verify claims
    }
