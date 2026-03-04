"""Sub-agents package for DeepAgent."""

from subagents.summarizer import get_summarizer_config
from subagents.fact_checker import get_fact_checker_config
from subagents.writer import get_writer_config

__all__ = [
    "get_summarizer_config",
    "get_fact_checker_config",
    "get_writer_config",
]
