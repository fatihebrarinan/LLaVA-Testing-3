from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from pathlib import Path
import llava_backend

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Create uploads folder if it doesn't exist
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# Model will be lazy-loaded on first request
model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/chat', methods=['POST'])
def chat():
    global model
    try:
        # Lazy load the model on first request
        if model is None:
            print("Loading LLaVA One Vision model...")
            model = llava_backend.get_model()
            print("Model ready!")
        
        data = request.json
        prompt = data.get('prompt', '')
        image_paths = data.get('image_paths', [])
        
        # Convert relative paths to absolute paths
        absolute_paths = []
        if image_paths:
            for image_path in image_paths:
                full_path = os.path.join(app.config['UPLOAD_FOLDER'], image_path)
                if os.path.exists(full_path):
                    absolute_paths.append(full_path)
        
        # Generate response using LLaVA One Vision
        response_text = model.chat(prompt, absolute_paths if absolute_paths else None)
        
        return jsonify({
            'success': True,
            'response': response_text
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error in chat: {error_msg}")
        print(traceback_str)
        
        return jsonify({
            'success': False,
            'error': error_msg
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

