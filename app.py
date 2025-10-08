from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import base64
import os
from pathlib import Path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# API URL for Ollama (using /api/generate as per official docs)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        image_paths = data.get('image_paths', [])
        
        # Prepare the request to Ollama (matching official API documentation)
        payload = {
            "model": "llava",
            "prompt": prompt,
            "stream": False
        }
        
        # If there are images, encode them all in base64 and add to payload
        if image_paths:
            encoded_images = []
            for image_path in image_paths:
                full_path = os.path.join(app.config['UPLOAD_FOLDER'], image_path)
                with open(full_path, 'rb') as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                    encoded_images.append(img_data)
            payload["images"] = encoded_images
        
        # Send request to Ollama
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return jsonify({
            'success': True,
            'response': result.get('response', '')
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file part'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'}), 400
        
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'url': f'/uploads/{filename}'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

