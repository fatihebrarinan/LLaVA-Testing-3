# LLaVA Simple UI

A beautiful and modern web interface for LLaVA (Large Language and Vision Assistant) using Ollama.

## Features

- 🎨 Modern, responsive UI
- 📸 Multiple image upload support (drag-and-drop)
- 🔍 Compare and analyze multiple images simultaneously
- 💬 Interactive chat interface
- 🚀 Easy to use and deploy

## Prerequisites

- Python 3.8 or higher
- Ollama installed with LLaVA model
- Run `ollama run llava:latest` to ensure the model is downloaded

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Make sure Ollama is running (it should be running on `http://localhost:11434`)

2. Start the Flask application:
```bash
python app.py
```

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

## Troubleshooting

- If you get connection errors, make sure Ollama is running: `ollama serve`
- Make sure the LLaVA model is installed: `ollama run llava:latest`
- Check that port 5000 is not being used by another application

## License

MIT License
