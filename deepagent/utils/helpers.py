"""
DeepAgent Helper Utilities
Common utility functions used across the project.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from config import OUTPUT_DIR


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()


def save_output(content: str, filename: str, subdir: str = "") -> str:
    """
    Save content to the output directory.
    
    Args:
        content: Content to save
        filename: Name of the file
        subdir: Optional subdirectory within output
        
    Returns:
        Full path to the saved file
    """
    output_path = OUTPUT_DIR
    if subdir:
        output_path = output_path / subdir
        output_path.mkdir(parents=True, exist_ok=True)

    filepath = output_path / filename
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def save_json(data: dict | list, filename: str, subdir: str = "") -> str:
    """
    Save data as JSON to the output directory.
    
    Args:
        data: Data to serialize
        filename: Name of the file
        subdir: Optional subdirectory within output
        
    Returns:
        Full path to the saved file
    """
    content = json.dumps(data, indent=2, ensure_ascii=False, default=str)
    return save_output(content, filename, subdir)


def load_json(filepath: str) -> dict | list:
    """Load JSON data from a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def format_search_results(results: dict) -> str:
    """
    Format Tavily search results into a readable string.
    
    Args:
        results: Raw Tavily search results
        
    Returns:
        Formatted string of search results
    """
    if not results or "results" not in results:
        return "No results found."

    formatted = []
    for i, result in enumerate(results["results"], 1):
        title = result.get("title", "No title")
        url = result.get("url", "")
        snippet = result.get("content", "No content available")
        formatted.append(f"### Result {i}: {title}\n**URL**: {url}\n{snippet}\n")

    return "\n---\n".join(formatted)


def _content_to_str(content) -> str:
    """
    Convert message content to a plain string.
    
    LLM models can return content as:
    - A plain string: "Hello world"
    - A list of content blocks: [{"type": "text", "text": "Hello world"}, ...]
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return str(content)


def extract_final_response(result: dict) -> str:
    """
    Extract the final text response from an agent result.
    
    Args:
        result: Agent invocation result
        
    Returns:
        Final response text
    """
    if not result or "messages" not in result:
        return "No response generated."

    messages = result["messages"]
    # Find the last AI message
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            if hasattr(msg, "type") and msg.type == "ai":
                return _content_to_str(msg.content)
        elif isinstance(msg, dict) and msg.get("content"):
            if msg.get("role") == "assistant":
                return _content_to_str(msg["content"])

    return "No response generated."


def count_tokens_approx(text: str) -> int:
    """
    Approximate token count (rough estimate: 1 token ≈ 4 characters).
    
    Args:
        text: Input text
        
    Returns:
        Approximate token count
    """
    return len(text) // 4


def create_session_id() -> str:
    """Generate a unique session ID based on timestamp."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
