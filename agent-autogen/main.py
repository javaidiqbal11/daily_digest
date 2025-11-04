import os
import asyncio
import gradio as gr
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# --- Load API key ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set OPENAI_API_KEY in your .env file")

# --- Create model client ---
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=api_key)

# --- Create assistant agent ---
assistant = AssistantAgent(
    name="assistant",
    model_client=model_client,
    system_message="You are a helpful coding assistant. Respond clearly with code and concise explanations.",
    description="Python code helper agent"
)

# --- Define async chat logic ---
async def ask_agent(message: str):
    """Send user message to AutoGen agent and get streamed response."""
    response_text = ""
    async for chunk in assistant.run_stream(task=message):
        if hasattr(chunk, "content") and chunk.content:
            response_text += chunk.content
            yield response_text  # Stream partial results to Gradio

# --- Gradio async wrapper ---
async def chat_with_agent(message, history):
    response = ""
    async for partial in ask_agent(message):
        response = partial
        yield response  # Send incremental response back to UI

# --- Gradio Interface ---
chat_ui = gr.ChatInterface(
    fn=chat_with_agent,
    title="🤖 AutoGen Code Assistant",
    description="Ask coding or AI questions — powered by AutoGen + OpenAI",
    theme="soft",
    examples=[
        ["Write a Python function to compute Fibonacci numbers."],
        ["Explain Python decorators with an example."],
        ["Optimize a Python loop for better performance."],
    ],
)

if __name__ == "__main__":
    chat_ui.launch(server_name="0.0.0.0", server_port=7860, share=True)
