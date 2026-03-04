"""
DeepAgent - Deep Research AI powered by LangChain DeepAgents

A production-ready deep agent system with planning, sub-agents,
web search, file management, and a modern web interface.

Usage:
    CLI:  python main.py
    Web:  python web_app.py
    
Quick:
    from agents import create_research_agent
    agent = create_research_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": "Research quantum computing"}]})
"""

__version__ = "1.0.0"
__author__ = "DeepAgent"
