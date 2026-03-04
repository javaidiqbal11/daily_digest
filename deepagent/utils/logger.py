"""
DeepAgent Logging Configuration
Sets up rich-formatted logging for the application.
"""

import logging
import sys
from rich.logging import RichHandler
from rich.console import Console

console = Console()


def setup_logger(name: str = "deepagent", level: int = logging.INFO) -> logging.Logger:
    """
    Create and configure a logger with rich formatting.
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = RichHandler(
            console=console,
            show_time=True,
            show_path=False,
            markup=True,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
        )
        handler.setLevel(level)
        
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        logger.setLevel(level)

    return logger


# ─── Default Logger ──────────────────────────────────────────────────────────
logger = setup_logger()
