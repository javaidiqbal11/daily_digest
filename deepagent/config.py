"""
DeepAgent Configuration Module
Centralizes all configuration and environment variable management.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

# ─── Project Paths ───────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


class LLMConfig(BaseModel):
    """LLM provider configuration."""
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    anthropic_api_key: str = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    default_model: str = Field(default_factory=lambda: os.getenv("DEFAULT_MODEL", "openai:gpt-4o"))


class SearchConfig(BaseModel):
    """Search tool configuration."""
    tavily_api_key: str = Field(default_factory=lambda: os.getenv("TAVILY_API_KEY", ""))
    max_search_results: int = Field(default=5)


class AgentConfig(BaseModel):
    """Agent behavior configuration."""
    default_agent_type: str = Field(
        default_factory=lambda: os.getenv("DEFAULT_AGENT_TYPE", "research")
    )
    max_iterations: int = Field(
        default_factory=lambda: int(os.getenv("MAX_ITERATIONS", "50"))
    )
    output_dir: str = Field(default_factory=lambda: str(OUTPUT_DIR))


class WebConfig(BaseModel):
    """Web UI configuration."""
    host: str = Field(default_factory=lambda: os.getenv("WEB_HOST", "0.0.0.0"))
    port: int = Field(default_factory=lambda: int(os.getenv("WEB_PORT", "8000")))


class AppConfig(BaseModel):
    """Main application configuration."""
    llm: LLMConfig = Field(default_factory=LLMConfig)
    search: SearchConfig = Field(default_factory=SearchConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    web: WebConfig = Field(default_factory=WebConfig)

    def validate_api_keys(self) -> list[str]:
        """Validate that required API keys are set. Returns list of warnings."""
        warnings = []
        if not self.llm.openai_api_key and not self.llm.anthropic_api_key:
            warnings.append(
                "⚠️  No LLM API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env"
            )
        if not self.search.tavily_api_key:
            warnings.append(
                "⚠️  No TAVILY_API_KEY found. Web search will be disabled."
            )
        return warnings


# ─── Global Config Instance ──────────────────────────────────────────────────
config = AppConfig()
