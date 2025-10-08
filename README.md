# LLaVA One Vision UI

A beautiful and modern web interface for LLaVA One Vision - a powerful multimodal AI that understands images, text, and can handle multiple images simultaneously.

## Features

- 🎨 Modern, responsive UI with separated CSS/JS
- 📸 Multiple image upload support (drag-and-drop)
- 🔍 Compare and analyze multiple images simultaneously
- 💬 Interactive chat interface
- 🧠 **Powered by LLaVA One Vision** - State-of-the-art vision-language model
- 🖼️ Image gallery with lightbox view
- 🚀 Direct model integration (no external API needed)

## What is LLaVA One Vision?

LLaVA One Vision is a cutting-edge multimodal model that can:
- Process single and multiple images
- Handle high-resolution images (up to 2304x2304)
- Understand complex visual reasoning tasks
- Perform OCR, chart analysis, and document understanding
- Compare and analyze relationships between multiple images

## Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU recommended (CPU mode available)
- 4GB+ GPU memory for 0.5B model, 16GB+ for 7B model

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install LLaVA-NeXT package:**
```bash
cd LLaVA-NeXT
pip install -e .
cd ..
```

The model will be automatically downloaded from HuggingFace on first run (~2GB for the 0.5B model).

## Usage

1. Start the Flask application:
```bash
python app.py
```

The first request will trigger model loading (this may take a minute).

3. Open your browser and navigate to:
```
http://localhost:5000
```

4. Upload an image and start chatting!

## How to Use

1. **Upload Images**: Click on the upload area or drag and drop one or multiple image files
2. **Ask Questions**: Type your question about the image(s) in the chat input
3. **Get Answers**: LLaVA will analyze the image(s) and respond to your questions
4. **Compare Images**: Upload multiple images and ask LLaVA to compare them!

## Example Questions

### Single Image:
- "What's in this image?"
- "Describe what you see in detail"
- "What colors are present in this image?"
- "Can you identify any objects or people?"
- "What is the mood or atmosphere of this image?"

### Multiple Images:
- "What are the differences between these images?"
- "Which image has more people?"
- "Compare the colors in these images"
- "What do these images have in common?"
- "Describe each image briefly"

## Model Options

By default, the app uses the lightweight `0.5B` model. You can change this in `llava_backend.py`:

```python
# For more powerful analysis (requires more VRAM):
model_path="lmms-lab/llava-onevision-qwen2-7b-si"  # 7B model
model_path="lmms-lab/llava-onevision-qwen2-72b-si"  # 72B model
```

## Troubleshooting

### Out of Memory
- Use the 0.5B model (default)
- Reduce image resolution
- Use CPU mode by setting `device="cpu"` in `llava_backend.py`

### Model Download Issues
- Check internet connection
- Ensure HuggingFace access is not blocked
- Model will be cached in `~/.cache/huggingface/`

### Port Already in Use
- Change port in `app.py`: `app.run(debug=True, port=5001)`

## Performance

- **0.5B Model**: ~4GB VRAM, fast inference
- **7B Model**: ~16GB VRAM, better accuracy
- **72B Model**: ~80GB VRAM, best performance

## Architecture

```
app.py                  # Flask web server
llava_backend.py        # LLaVA One Vision model interface
static/
  ├── css/style.css     # UI styling
  └── js/app.js         # Frontend logic
templates/
  └── index.html        # HTML structure
LLaVA-NeXT/             # LLaVA One Vision repository
```

## License

MIT License
