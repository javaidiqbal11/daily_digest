# import os
# from dotenv import load_dotenv
# import requests
# import json

# load_dotenv()
# API_KEY = os.getenv("OLLAMA_API_KEY")

# url = "https://ollama.com/api/generate"

# payload = {
#     "model": "gpt-oss:20b-cloud",
#     "prompt": "Write a Python function to check prime numbers",
#     "temperature": 0.1,
#     "max_tokens": 500
# }

# headers = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }

# response = requests.post(url, json=payload, headers=headers, stream=True)

# final_text = ""

# for line in response.iter_lines():
#     if line:
#         chunk = json.loads(line.decode("utf-8"))
#         final_text += chunk.get("response", "")
#         if chunk.get("done"):
#             break

# print("AI Response:\n", final_text)



import os
import json
import requests
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_URL = "https://ollama.com/api/generate"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def generate_response(prompt, temperature, max_tokens):
    """
    Streams response from Ollama API and yields partial output for Gradio
    """
    payload = {
        "model": "gpt-oss:120b-cloud",  # gpt-oss:20b-cloud
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        headers=HEADERS,
        stream=True,
        timeout=300
    )

    final_text = ""

    for line in response.iter_lines():
        if not line:
            continue

        chunk = json.loads(line.decode("utf-8"))
        final_text += chunk.get("response", "")
        yield final_text

        if chunk.get("done"):
            break


# Gradio UI
with gr.Blocks(title="Ollama AI Web Interface") as demo:
    gr.Markdown("## Ollama AI – Web Interface")

    with gr.Row():
        with gr.Column(scale=1):
            prompt = gr.Textbox(
                label="Prompt",
                lines=6,
                placeholder="Write a Python function to check prime numbers"
            )
            temperature = gr.Slider(
                0.0, 1.0, value=0.1, step=0.05, label="Temperature"
            )
            max_tokens = gr.Slider(
                50, 2000, value=500, step=50, label="Max Tokens"
            )
            submit = gr.Button("Generate")

        with gr.Column(scale=2):
            output = gr.Textbox(
                label="AI Response",
                lines=15
            )

    submit.click(
        fn=generate_response,
        inputs=[prompt, temperature, max_tokens],
        outputs=output
    )


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",   # accessible on network
        server_port=8080,
        show_error=True,
        share=True
    )
