"""
A simple example to demonstrate how an LLM (Large Language Model) works:
1. Loads a pretrained Transformer model (GPT-2)
2. Tokenizes input text
3. Passes tokens through the model
4. Generates text token by token
"""

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch


def explain_model_details(model_name="gpt2"):
    """
    Loads a tokenizer and model, prints key details about the LLM.
    """
    print("🔹 Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    print(f"\n✅ Model Loaded: {model_name}")
    print(f"📊 Number of Parameters: {model.num_parameters():,}")
    print(f"🧠 Model Type: {model.config.model_type}")
    print(f"🗣️ Context Window (max tokens): {model.config.n_positions}")
    print(f"🧩 Hidden Layers: {model.config.n_layer}")
    print(f"⚙️ Attention Heads: {model.config.n_head}")

    return tokenizer, model


def generate_text(prompt, tokenizer, model, max_length=50):
    """
    Generates text from a given prompt using the LLM.
    """

    print("\n🔹 Tokenizing input text...")
    inputs = tokenizer(prompt, return_tensors="pt")

    print(f"🧾 Tokens: {inputs['input_ids']}")
    print(f"🧩 Decoded Tokens: {tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])}")

    print("\n🔹 Generating text...")
    output_ids = model.generate(
        **inputs,
        max_length=max_length,  
        temperature=0.9,
        top_p=0.95,
        do_sample=True
    )

    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    print("\n✅ Generated Text:")
    print("──────────────────────────────")
    print(generated_text)
    print("──────────────────────────────")

    return generated_text


def quick_pipeline(prompt, model_name="gpt2"):
    """
    Simple text generation using Hugging Face pipeline (high-level API).
    """
    print("\n⚡ Using high-level pipeline for quick generation...")
    generator = pipeline("text-generation", model=model_name)
    result = generator(prompt, max_length=40, num_return_sequences=1)
    print(result[0]["generated_text"])


def main():
    """
    Main driver function.
    """
    print("\n🚀 Understanding How an LLM Works (Using GPT-2)\n")

    # Step 1: Load model and tokenizer
    tokenizer, model = explain_model_details("gpt2")

    # Step 2: Define prompt
    prompt = "Artificial intelligence will change the"

    # Step 3: Generate text manually
    generate_text(prompt, tokenizer, model)

    # Step 4: (Optional) Use pipeline shortcut
    quick_pipeline(prompt)


if __name__ == "__main__":
    main()
