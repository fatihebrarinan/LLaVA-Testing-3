# LLaVA Image Search System

## Overview

This application implements a semantic image search system using LLaVA-NeXT for image captioning and ChromaDB for vector-based similarity search. You can upload images, automatically generate captions using LLaVA, and then search for images using natural language queries.

## How It Works

### The Technology Stack

1. **LLaVA-NeXT** - Generates detailed captions for uploaded images
2. **Sentence Transformers** - Converts captions to vector embeddings
3. **ChromaDB** - Stores and searches image-caption pairs using vector similarity
4. **Flask** - Web framework for the user interface

### The Process

```
1. Upload Image → 2. LLaVA Generates Caption → 3. Convert to Vector → 4. Store in Database
                                                        ↓
                                                   Search Query
                                                        ↓
                                              Convert Query to Vector
                                                        ↓
                                            Find Similar Vectors (Images)
```

## Features

### 🔍 Three Main Pages

1. **Upload & Index** (`/upload`)
   - Drag-and-drop or browse to upload images
   - Automatically generates captions using LLaVA
   - Stores image-caption pairs in vector database
   - Shows real-time progress and results

2. **Search Images** (`/search`)
   - Search for images using natural language
   - Example: "a man holding a gun", "outdoor scene", "animal"
   - Results ranked by similarity score
   - Click images for full-size preview

3. **Gallery** (`/gallery`)
   - View all indexed image-caption pairs
   - Switch between grid and list views
   - Click to view full image with caption

### 🎯 Key Capabilities

- **Semantic Search**: Finds images based on meaning, not just keywords
- **Batch Upload**: Upload multiple images at once
- **Similarity Scores**: See how well each result matches your query
- **Persistent Storage**: Images and captions are saved between sessions
- **Real-time Stats**: See how many images are indexed

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

New dependencies added:
- `chromadb==0.4.22` - Vector database
- `sentence-transformers==2.5.1` - Text embeddings

### 2. Download LLaVA Model

The application uses `lmms-lab/llava-onevision-qwen2-0.5b-si` which will download automatically on first run.

### 3. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## Usage Guide

### Uploading and Indexing Images

1. Navigate to the **Upload & Index** page
2. Drag-and-drop images or click to browse
3. Wait for LLaVA to generate captions (this may take a few seconds per image)
4. Images are automatically indexed in the database

**Tips:**
- You can upload multiple images at once
- The first upload will be slower as the model loads
- Captions are generated automatically - no manual input needed

### Searching for Images

1. Navigate to the **Search Images** page
2. Enter a natural language description (e.g., "a person smiling")
3. Click Search or press Enter
4. View results ranked by similarity

**Example Queries:**
- "a man holding a gun"
- "outdoor landscape with mountains"
- "food on a plate"
- "red car"
- "group of people"
- "cat or dog"

**How Similarity Works:**
- The search converts your query to a vector
- Compares it with all stored caption vectors
- Returns images with the most similar captions
- Similarity score shown as a percentage

### Viewing the Gallery

1. Navigate to the **Gallery** page
2. Browse all indexed images with their captions
3. Switch between grid and list views
4. Click any image to see it full-size

## API Endpoints

### POST `/api/index-image`
Upload and index a new image.

**Request:** Form-data with `file` field
**Response:**
```json
{
  "success": true,
  "filename": "image.jpg",
  "caption": "A detailed description of the image",
  "url": "/uploads/image.jpg"
}
```

### POST `/api/search-images`
Search for images by text query.

**Request:**
```json
{
  "query": "a man holding a gun",
  "n_results": 10
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "image_path": "image.jpg",
      "caption": "The generated caption",
      "similarity": 0.85,
      "url": "/uploads/image.jpg"
    }
  ],
  "count": 1
}
```

### GET `/api/get-all-images`
Get all indexed images.

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "image_path": "image.jpg",
      "caption": "The caption",
      "url": "/uploads/image.jpg"
    }
  ],
  "count": 1
}
```

### GET `/api/stats`
Get database statistics.

**Response:**
```json
{
  "success": true,
  "total_images": 42
}
```

## File Structure

```
LLaVA-Testing-3/
├── app.py                  # Flask application with routes
├── llava_backend.py        # LLaVA model wrapper
├── vector_db.py            # Vector database wrapper (ChromaDB)
├── requirements.txt        # Python dependencies
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── upload.html        # Upload & index page
│   ├── search.html        # Search page
│   └── gallery.html       # Gallery page
├── uploads/               # Uploaded images (created automatically)
└── chroma_db/            # Vector database (created automatically)
```

## Understanding the Vector Search

### What are Vectors?

When you upload an image:
1. LLaVA generates a caption: "A man holding a gun in an urban setting"
2. Sentence-transformers converts this to a 384-dimensional vector
3. This vector represents the semantic meaning of the caption

Example (simplified to 3 dimensions):
```
"a man with a gun" → [0.23, -0.45, 0.67]
"outdoor scene"    → [-0.12, 0.78, -0.34]
```

### How Search Works

When you search for "a man holding a gun":
1. Your query is converted to a vector: `[0.25, -0.43, 0.69]`
2. The database finds the closest vectors using cosine similarity
3. Returns the images with the most similar caption vectors

**Why This Works:**
- Similar meanings have similar vectors
- "man with gun" and "person holding weapon" will have close vectors
- The search understands semantics, not just exact word matches

## Performance Tips

1. **First Load**: The first image upload will be slow as models load (~30 seconds)
2. **Batch Processing**: Upload multiple images at once for efficiency
3. **GPU Acceleration**: If you have CUDA, the app will automatically use it
4. **Database Size**: ChromaDB handles thousands of images efficiently

## Troubleshooting

### "Loading model..." takes too long
- First load can take 30-60 seconds
- Model is ~3GB, download happens once
- Subsequent loads are much faster

### Search returns no results
- Make sure you've uploaded and indexed images first
- Check the Gallery to see what's been indexed
- Try broader search terms

### Out of memory errors
- Reduce batch size when uploading
- Close other GPU applications
- Consider using CPU mode (slower but more stable)

## Technical Details

### Embedding Model
- Model: `all-MiniLM-L6-v2`
- Dimensions: 384
- Fast and efficient for semantic search

### Vector Database
- Engine: ChromaDB
- Distance Metric: Cosine Similarity
- Persistent: Data saved to disk at `./chroma_db`

### LLaVA Model
- Model: `lmms-lab/llava-onevision-qwen2-0.5b-si`
- Size: ~500MB
- Fast inference on modern GPUs

## Future Enhancements

Potential improvements:
- [ ] Delete images from database
- [ ] Re-index images with custom captions
- [ ] Filters (date, file type, etc.)
- [ ] Image-to-image search
- [ ] Export search results
- [ ] Advanced search with multiple queries
- [ ] User authentication

## Credits

- **LLaVA-NeXT**: Vision-language model for image understanding
- **ChromaDB**: Vector database for similarity search
- **Sentence Transformers**: Text embedding model
- **Flask**: Web framework

## License

Same as the main project.

