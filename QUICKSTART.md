# Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- PyTorch (ML framework)
- Transformers (HuggingFace models)
- ChromaDB (vector database)
- Sentence-transformers (text embeddings)
- And other dependencies

### Step 2: Verify Setup
```bash
python verify_setup.py
```

This will check that everything is installed correctly.

### Step 3: Start the Application
```bash
python app.py
```

**Note:** The first time you run this, it will download the LLaVA model (~3GB). This is a one-time download.

### Step 4: Open in Browser
Navigate to: http://localhost:5000

---

## Using the Image Search System

### Page 1: Upload & Index Images

1. Click on the "Upload & Index" tab
2. Drag and drop images or click to browse
3. Wait for LLaVA to generate captions
4. Images are automatically saved to the database

**First Upload:**
- The very first upload will be slower (model loading)
- Subsequent uploads are faster

### Page 2: Search Images

1. Click on the "Search Images" tab
2. Enter a description in natural language
3. Click "Search" or press Enter
4. View results sorted by relevance

**Example Searches:**
- "a man holding a gun"
- "outdoor landscape with trees"
- "food on a plate"
- "group of people smiling"
- "red car on street"

### Page 3: Gallery

1. Click on the "Gallery" tab
2. Browse all indexed images with their captions
3. Switch between grid and list views
4. Click any image to view full-size

---

## How It Works (Simple Explanation)

```
┌─────────────────┐
│  Upload Image   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  LLaVA generates        │
│  caption automatically  │
│  "A man holding a gun"  │
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────┐
│  Caption converted to    │
│  mathematical vector     │
│  [0.23, -0.45, 0.67...] │
└────────┬─────────────────┘
         │
         ▼
┌────────────────────┐
│  Stored in vector  │
│  database (ChromaDB)│
└────────────────────┘

When you search:
┌────────────────┐
│ Your search:   │
│ "man with gun" │
└────────┬───────┘
         │
         ▼
┌─────────────────────────┐
│  Converted to vector    │
│  [0.25, -0.43, 0.69...] │
└────────┬────────────────┘
         │
         ▼
┌────────────────────────────┐
│  Find similar vectors      │
│  in database               │
│  (closest = most relevant) │
└────────┬───────────────────┘
         │
         ▼
┌──────────────┐
│ Show results │
│ ranked by    │
│ similarity   │
└──────────────┘
```

### Why Vector Search?

Traditional search: "man with gun" ≠ "person holding weapon" ❌

Vector search: Both convert to similar vectors, so they match! ✅

This is called **semantic search** - it understands meaning, not just exact words.

---

## Troubleshooting

### "Model loading takes forever"
- First load downloads ~3GB model (one time only)
- Subsequent loads are much faster (~30 seconds)
- Model is cached at `~/.cache/huggingface/`

### "Out of memory error"
- You're using GPU mode but don't have enough VRAM
- Solution 1: Use smaller 0.5B model (default)
- Solution 2: Switch to CPU mode (edit `llava_backend.py`, set `device="cpu"`)
- Solution 3: Close other GPU applications

### "No results found"
- Make sure you've uploaded images first
- Check the Gallery to see what's been indexed
- Try simpler/broader search terms

### "Port 5000 already in use"
- Edit `app.py`, change: `app.run(debug=True, port=5001)`

### "ChromaDB errors"
- Delete the `chroma_db/` folder and restart
- It will create a fresh database

---

## Tips for Best Results

### Uploading Images
- ✅ Clear, well-lit images work best
- ✅ Upload a variety of images for better search diversity
- ✅ You can upload multiple images at once
- ✅ Supported formats: JPG, PNG (up to 50MB each)

### Searching
- ✅ Use descriptive phrases: "a red car on a street"
- ✅ Be specific: "person wearing sunglasses" vs just "person"
- ✅ Try different phrasings if you don't find what you want
- ❌ Don't use just single words (e.g., "car" - try "red car" instead)

### Performance
- 🚀 GPU: ~2-5 seconds per image caption
- 🐌 CPU: ~10-30 seconds per image caption
- 💾 Database: Handles thousands of images efficiently
- 🔍 Search: Nearly instant (even with thousands of images)

---

## What's Next?

Once you're comfortable with the basics:

1. **Read the detailed docs**: [IMAGE_SEARCH_README.md](IMAGE_SEARCH_README.md)
2. **Try the API**: Use the REST API endpoints for integration
3. **Customize captions**: Edit the caption prompt in `app.py` line 72
4. **Try different models**: Edit `llava_backend.py` to use 7B or 72B models

---

## Need Help?

- Check [IMAGE_SEARCH_README.md](IMAGE_SEARCH_README.md) for detailed documentation
- Check [README.md](README.md) for general information
- Run `python verify_setup.py` to diagnose issues

Enjoy your semantic image search! 🎉

