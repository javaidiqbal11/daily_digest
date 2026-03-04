# 🤖 DeepAgent - LangChain Deep Research Agent

A production-ready Deep Agent built with **LangChain** and **LangGraph** using the `deepagents` package. This project implements an intelligent research agent capable of planning, sub-agent delegation, web searching, file management, and context-aware conversations.

## 🌟 Features

- **🔍 Deep Research Agent** - Conducts thorough multi-step research with web search
- **📋 Task Planning** - Automatic task decomposition with TODO tracking
- **🤖 Sub-Agent Delegation** - Spawns specialized sub-agents for focused tasks
- **📁 Virtual File System** - Persistent context management through file operations
- **🌐 Web Search** - Tavily-powered internet search for real-time information
- **💬 Interactive CLI** - Beautiful terminal-based chat interface
- **🖥️ Web UI** - Modern web interface for interacting with the agent
- **🔄 Streaming** - Real-time streaming of agent responses
- **🧠 Memory** - Persistent memory across conversations
- **🛡️ Human-in-the-Loop** - Approval flow for sensitive operations

## 📁 Project Structure

```
deepagent/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── config.py                 # Configuration management
├── main.py                   # CLI entry point
├── web_app.py                # Web UI application
├── agents/
│   ├── __init__.py
│   ├── research_agent.py     # Deep research agent
│   ├── code_agent.py         # Code assistant agent
│   └── general_agent.py      # General purpose agent
├── tools/
│   ├── __init__.py
│   ├── search_tools.py       # Web search tools
│   ├── file_tools.py         # File management tools
│   └── analysis_tools.py     # Data analysis tools
├── subagents/
│   ├── __init__.py
│   ├── summarizer.py         # Summarization sub-agent
│   ├── fact_checker.py       # Fact-checking sub-agent
│   └── writer.py             # Report writing sub-agent
├── utils/
│   ├── __init__.py
│   ├── logger.py             # Logging configuration
│   ├── helpers.py            # Utility functions
│   └── prompts.py            # System prompts
├── templates/
│   └── index.html            # Web UI template
├── static/
│   ├── css/
│   │   └── style.css         # Web UI styles
│   └── js/
│       └── app.js            # Web UI JavaScript
└── output/                   # Agent output directory
    └── .gitkeep
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
copy .env.example .env
# Edit .env with your API keys
```

### 3. Run the CLI Agent

```bash
python main.py
```

### 4. Run the Web UI

```bash
python web_app.py
```

Then open `http://localhost:8000` in your browser.

## 🔧 Configuration

Edit `.env` file with your API keys:

```env
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
TAVILY_API_KEY=your-tavily-key
```

## 📖 Usage Examples

### Research Agent
```python
from agents.research_agent import create_research_agent

agent = create_research_agent()
result = agent.invoke({
    "messages": [{"role": "user", "content": "Research the latest advances in quantum computing"}]
})
```

### Code Agent
```python
from agents.code_agent import create_code_agent

agent = create_code_agent()
result = agent.invoke({
    "messages": [{"role": "user", "content": "Write a Python script that analyzes CSV data"}]
})
```

## 📝 License

MIT License
