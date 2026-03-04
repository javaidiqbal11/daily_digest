"""
DeepAgent Search Tools
Web search tools powered by Tavily for real-time information gathering.
"""

import os
from typing import Literal, Optional

from tavily import TavilyClient

from config import config
from utils.logger import logger


def _get_tavily_client() -> TavilyClient:
    """Get or create Tavily client."""
    api_key = config.search.tavily_api_key or os.environ.get("TAVILY_API_KEY", "")
    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY is required for search functionality. "
            "Set it in your .env file or as an environment variable."
        )
    return TavilyClient(api_key=api_key)


def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
) -> dict:
    """
    Search the internet for information on any topic.
    
    Use this tool to find current information, facts, data, documentation,
    and more from the web. Returns search results with titles, URLs, and
    content snippets.
    
    Args:
        query: The search query - be specific and descriptive for best results
        max_results: Maximum number of results to return (1-10, default 5)
        topic: Search category - "general" for broad searches, 
               "news" for current events, "finance" for financial data
        include_raw_content: If True, includes the full page content
                           (slower but more comprehensive)
    
    Returns:
        Dictionary with search results including titles, URLs, and content
    """
    logger.info(f"🔍 Searching: [bold]{query}[/bold]")
    try:
        client = _get_tavily_client()
        results = client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic=topic,
        )
        logger.info(f"✅ Found {len(results.get('results', []))} results")
        return results
    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        return {"results": [], "error": str(e)}


def news_search(
    query: str,
    max_results: int = 5,
    include_raw_content: bool = False,
) -> dict:
    """
    Search for recent news articles on a specific topic.
    
    This is optimized for finding current news and events. Use this when
    the user asks about recent developments, breaking news, or current events.
    
    Args:
        query: The news search query
        max_results: Maximum number of news articles to return (1-10)
        include_raw_content: If True, includes full article content
    
    Returns:
        Dictionary with news search results
    """
    logger.info(f"📰 News search: [bold]{query}[/bold]")
    try:
        client = _get_tavily_client()
        results = client.search(
            query,
            max_results=max_results,
            include_raw_content=include_raw_content,
            topic="news",
        )
        logger.info(f"✅ Found {len(results.get('results', []))} news articles")
        return results
    except Exception as e:
        logger.error(f"❌ News search failed: {e}")
        return {"results": [], "error": str(e)}
