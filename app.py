from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from pathlib import Path
import llava_backend
import vector_db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Create uploads folder if it doesn't exist
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

# Model and database will be lazy-loaded on first request
model = None
db = None

@app.route('/')
def index():
    """Main page - redirect to upload page"""
    return render_template('upload.html')

@app.route('/upload')
def upload_page():
    """Upload and index images page"""
    return render_template('upload.html')

@app.route('/search')
def search_page():
    """Search for images by caption page"""
    return render_template('search.html')

@app.route('/gallery')
def gallery_page():
    """View all indexed image-caption pairs"""
    return render_template('gallery.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/index-image', methods=['POST'])
def index_image():
    """Upload an image, generate caption with LLaVA, and index it"""
    global model, db
    try:
        # Lazy load model and database
        if model is None:
            print("Loading LLaVA One Vision model...")
            model = llava_backend.get_model()
            print("Model ready!")
        
        if db is None:
            print("Loading vector database...")
            db = vector_db.get_db()
            print("Database ready!")
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file part'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No selected file'}), 400
        
        # Save the file
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Generate caption using LLaVA
        caption_prompt = "Describe this image in detail."
        caption = model.chat(caption_prompt, [filepath])
        
        # Index in vector database
        db.add_image(filename, caption)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'caption': caption,
            'url': f'/uploads/{filename}'
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error in index_image: {error_msg}")
        print(traceback_str)
        
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/search-images', methods=['POST'])
def search_images():
    """Search for images by text query"""
    global db
    try:
        # Lazy load database
        if db is None:
            db = vector_db.get_db()
        
        data = request.json
        query = data.get('query', '')
        n_results = data.get('n_results', 10)
        
        if not query:
            return jsonify({'success': False, 'error': 'No query provided'}), 400
        
        # Search in vector database
        results = db.search(query, n_results)
        
        # Add full URL to each result
        for result in results:
            result['url'] = f"/uploads/{result['image_path']}"
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error in search_images: {error_msg}")
        print(traceback_str)
        
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/get-all-images', methods=['GET'])
def get_all_images():
    """Get all indexed image-caption pairs"""
    global db
    try:
        # Lazy load database
        if db is None:
            db = vector_db.get_db()
        
        # Get all from database
        results = db.get_all()
        
        # Add full URL to each result
        for result in results:
            result['url'] = f"/uploads/{result['image_path']}"
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback_str = traceback.format_exc()
        print(f"Error in get_all_images: {error_msg}")
        print(traceback_str)
        
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    global db
    try:
        if db is None:
            db = vector_db.get_db()
        
        return jsonify({
            'success': True,
            'total_images': db.count()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

