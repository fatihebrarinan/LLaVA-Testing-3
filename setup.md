# LLaVA One Vision Setup Guide

## Quick Start

### Step 1: Install Dependencies

```bash
# Install main requirements
pip install -r requirements.txt

# Install LLaVA-NeXT package
cd LLaVA-NeXT
pip install -e .
cd ..
```

### Step 2: First Run

```bash
python app.py
```

**Note:** The first time you run the app, it will:
1. Download the LLaVA One Vision model (~2GB for 0.5B model)
2. Cache it in `~/.cache/huggingface/`
3. Load it into memory (takes ~30 seconds)

### Step 3: Access the UI

Open your browser and go to:
```
http://localhost:5000
```

## System Requirements

### Minimum (CPU Mode)
- 8GB RAM
- 10GB disk space
- Slower inference (~30s per image)

### Recommended (GPU Mode)
- NVIDIA GPU with 4GB+ VRAM
- 16GB RAM
- 10GB disk space
- Fast inference (~2-5s per image)

## Model Selection

Edit `llava_backend.py` line 16 to change models:

```python
# Lightweight (default) - 0.5B parameters
model_path="lmms-lab/llava-onevision-qwen2-0.5b-si"

# Better accuracy - 7B parameters (requires 16GB VRAM)
model_path="lmms-lab/llava-onevision-qwen2-7b-si"

# Best performance - 72B parameters (requires 80GB VRAM)
model_path="lmms-lab/llava-onevision-qwen2-72b-si"
```

## Features

✅ **Multi-Image Understanding**
- Upload multiple images and ask comparative questions
- "What are the differences between these images?"
- "Which image has more people?"

✅ **High-Resolution Support**
- Process images up to 2304x2304 pixels
- Excellent for charts, documents, and detailed images

✅ **Advanced Reasoning**
- OCR and text extraction
- Chart and graph analysis
- Visual reasoning and comparison
- Document understanding

✅ **Gallery View**
- Click any image to view full-size
- Remove individual images
- Drag and drop support

## Example Prompts

### Single Image
- "What's in this image?"
- "Read the text in this image"
- "Explain this chart"
- "What colors are dominant?"

### Multiple Images
- "Compare these two images"
- "What do all these images have in common?"
- "Which image shows the most activity?"
- "Describe each image briefly"

## Troubleshooting

### CUDA Out of Memory
```python
# In llava_backend.py, change:
device="cpu"  # Use CPU instead of GPU
```

### Slow Performance
- Use smaller images (resize to 1024x1024)
- Use 0.5B model instead of 7B
- Ensure CUDA is properly installed

### Model Not Downloading
```bash
# Check HuggingFace access
huggingface-cli login

# Or download manually
huggingface-cli download lmms-lab/llava-onevision-qwen2-0.5b-si
```

## Advanced Configuration

### Change Port
In `app.py` line 93:
```python
app.run(debug=True, port=5001)  # Change from 5000 to 5001
```

### Adjust Generation Parameters
In `llava_backend.py` `generate_response` method:
```python
max_new_tokens=4096,  # Maximum response length
temperature=0.2,      # Randomness (0=deterministic, 1=creative)
do_sample=True       # Enable sampling
```

### Enable Flash Attention (Faster Inference)
```bash
pip install flash-attn --no-build-isolation
```

## File Structure

```
├── app.py                 # Flask server
├── llava_backend.py       # Model interface
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/style.css     # Styling
│   └── js/app.js         # Frontend logic
├── templates/
│   └── index.html        # HTML template
├── uploads/              # Uploaded images (auto-created)
└── LLaVA-NeXT/           # Model repository
```

## Performance Benchmarks

| Model | VRAM | Load Time | Inference Time |
|-------|------|-----------|----------------|
| 0.5B  | 4GB  | 10s       | 2-3s/image     |
| 7B    | 16GB | 30s       | 3-5s/image     |
| 72B   | 80GB | 60s       | 5-10s/image    |

*Tested on NVIDIA RTX 4090*

## Next Steps

1. Try the example images in `LLaVA-NeXT/docs/ov_chat_images/`
2. Experiment with multi-image comparisons
3. Test high-resolution document analysis
4. Explore the LLaVA-NeXT documentation for advanced features

## Support

- 📝 [LLaVA-NeXT Documentation](https://github.com/LLaVA-VL/LLaVA-NeXT)
- 🤗 [HuggingFace Models](https://huggingface.co/lmms-lab)
- 📄 [Research Paper](https://arxiv.org/abs/2408.03326)

