"""
DeepAgent File Tools
Tools for managing reports and output files.
"""

import os
from datetime import datetime
from pathlib import Path

from config import OUTPUT_DIR
from utils.logger import logger


def save_report(
    content: str,
    filename: str = "",
    title: str = "Research Report",
) -> str:
    """
    Save a research report or document to the output directory.
    
    Use this to save completed reports, code files, analysis results,
    or any other work product that should be persisted.
    
    Args:
        content: The content to save (markdown, code, text, etc.)
        filename: Optional filename. If not provided, auto-generates one
                  based on the title and timestamp
        title: Title of the report (used for auto-generating filename)
    
    Returns:
        Message confirming the save location
    """
    if not filename:
        # Auto-generate filename from title
        safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title)
        safe_title = safe_title.strip().replace(" ", "_").lower()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_title}_{timestamp}.md"

    filepath = OUTPUT_DIR / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Add header with metadata
    header = f"# {title}\n\n"
    header += f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n---\n\n"
    
    full_content = header + content
    filepath.write_text(full_content, encoding="utf-8")
    
    logger.info(f"💾 Report saved: [bold]{filepath}[/bold]")
    return f"Report saved successfully to: {filepath}"


def read_report(filename: str) -> str:
    """
    Read a previously saved report from the output directory.
    
    Use this to review reports or documents that were saved earlier
    in the conversation.
    
    Args:
        filename: Name of the file to read from the output directory
    
    Returns:
        The content of the file
    """
    filepath = OUTPUT_DIR / filename
    
    if not filepath.exists():
        available = list_reports()
        return f"File '{filename}' not found.\n\nAvailable files:\n{available}"

    content = filepath.read_text(encoding="utf-8")
    logger.info(f"📖 Reading report: [bold]{filename}[/bold]")
    return content


def list_reports() -> str:
    """
    List all saved reports and files in the output directory.
    
    Use this to see what reports and documents have been saved
    during the current session or previously.
    
    Returns:
        Formatted list of available files with sizes and dates
    """
    files = sorted(OUTPUT_DIR.glob("*"), key=lambda f: f.stat().st_mtime, reverse=True)
    files = [f for f in files if f.is_file() and f.name != ".gitkeep"]

    if not files:
        return "No reports found in the output directory."

    lines = ["## 📁 Available Reports\n"]
    for f in files:
        size_kb = f.stat().st_size / 1024
        modified = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        lines.append(f"- **{f.name}** ({size_kb:.1f} KB, modified: {modified})")

    result = "\n".join(lines)
    logger.info(f"📋 Listed {len(files)} report(s)")
    return result
