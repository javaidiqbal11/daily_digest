import torch
from transformers import AutoModel, AutoTokenizer

def got_ocr_infer(image_path: str, ocr_type="ocr"):
    """
    Run GOT-OCR2.0 using the CPU-compatible fork.
    """
    tokenizer = AutoTokenizer.from_pretrained(
        "srimanth-d/GOT_CPU",
        trust_remote_code=True
    )

    # Force CPU execution
    model = AutoModel.from_pretrained(
        "srimanth-d/GOT_CPU",
        trust_remote_code=True,
        low_cpu_mem_usage=True,
        device_map="cpu",
        use_safetensors=True,
        pad_token_id=tokenizer.eos_token_id
    ).eval()

    # Direct inference
    result = model.chat(
        tokenizer,
        image_path,
        ocr_type=ocr_type
    )

    return result


if __name__ == "__main__":
    img_path = "example.jpg"
    text = got_ocr_infer(img_path, ocr_type="ocr")
    print("Extracted text:", text)
