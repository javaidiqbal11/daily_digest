# GOT-OCR2.0 (CPU Inference)

This repository provides a **CPU-compatible implementation of GOT-OCR2.0** to extract text from images. It is lightweight, easy to set up, and runs without requiring a GPU.

---

## Features

* Runs GOT-OCR2.0 **fully on CPU**
* Extracts text directly from images
* Easy setup with `requirements.txt`
* Works on Windows

---

## Setup Instructions (Windows)

Follow these steps to set up and run the project:

### 1. Clone the repository

```bash
git clone https://github.com/javaidiqbal11/javaidiqbal11/daily_digest/tree/main/GOT-OCR2.0%20(CPU%20Inference).git
cd GOT-OCR2.0%20(CPU%20Inference)
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Code

1. Place your input image (e.g., `example.jpg`) in the project folder.
2. Run the script:

```bash
python main.py
```

3. The extracted text will be printed in the terminal.

---

## Example Output

```
Extracted text: "This is the detected text from the image."
```

---

## Model Reference

This project uses the **CPU fork of GOT-OCR2.0** available on Hugging Face:
👉 [srimanth-d/GOT\_CPU](https://huggingface.co/srimanth-d/GOT_CPU)

---

## License

This repository is under the **MIT License**.
The GOT-OCR2.0 model itself belongs to its original authors. Please review their license before using it commercially.
