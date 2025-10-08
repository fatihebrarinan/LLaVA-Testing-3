# System Workflow Diagrams

## Overall System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│                         (Web Browser)                        │
└───────────────┬────────────────┬────────────────┬───────────┘
                │                │                │
        Upload Page      Search Page      Gallery Page
                │                │                │
                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                      FLASK WEB SERVER                        │
│                         (app.py)                             │
├─────────────────────────────────────────────────────────────┤
│  Routes:                                                     │
│  • POST /api/index-image                                    │
│  • POST /api/search-images                                  │
│  • GET  /api/get-all-images                                 │
│  • GET  /api/stats                                          │
└────────┬──────────────────────────┬──────────────┬──────────┘
         │                          │              │
         ▼                          ▼              ▼
┌─────────────────┐    ┌─────────────────────┐   ┌──────────┐
│  LLaVA Backend  │    │   Vector Database   │   │  Uploads │
│(llava_backend.py)│    │   (vector_db.py)    │   │ Folder   │
│                 │    │                     │   │          │
│ • Model: 0.5B   │    │ • ChromaDB          │   │ • Images │
│ • Captioning    │    │ • Embeddings        │   │ • Files  │
│ • GPU/CPU       │    │ • Similarity Search │   │          │
└─────────────────┘    └─────────────────────┘   └──────────┘
```

## Upload & Index Workflow

```
┌──────────────┐
│ User selects │
│ image file   │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────┐
│ Browser uploads file            │
│ POST /api/index-image           │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Flask receives file             │
│ Saves to uploads/photo.jpg      │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ LLaVA processes image           │
│ Generates caption:              │
│ "A man holding a gun in         │
│  an urban setting at night"     │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Sentence-Transformer converts   │
│ caption to vector:              │
│ [0.23, -0.45, 0.67, 0.12, ...]  │
│ (384 dimensions)                │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ ChromaDB stores:                │
│ • Image path: photo.jpg         │
│ • Caption: "A man holding..."   │
│ • Embedding: [0.23, -0.45, ...] │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Response sent to browser:       │
│ {success: true,                 │
│  caption: "A man holding...",   │
│  filename: "photo.jpg"}         │
└──────┬──────────────────────────┘
       │
       ▼
┌──────────────┐
│ User sees    │
│ caption and  │
│ confirmation │
└──────────────┘
```

## Search Workflow

```
┌──────────────┐
│ User enters  │
│ search query │
│ "man with    │
│  a gun"      │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────┐
│ Browser sends query             │
│ POST /api/search-images         │
│ {query: "man with a gun",       │
│  n_results: 10}                 │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Sentence-Transformer converts   │
│ query to vector:                │
│ [0.25, -0.43, 0.69, 0.10, ...]  │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ ChromaDB calculates similarity  │
│ with all stored embeddings:     │
│                                 │
│ photo1.jpg: 0.89 (89% match) ✓  │
│ photo2.jpg: 0.67 (67% match) ✓  │
│ photo3.jpg: 0.45 (45% match)    │
│ photo4.jpg: 0.12 (12% match)    │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Return top results sorted       │
│ by similarity:                  │
│ [{image: photo1.jpg,            │
│   similarity: 0.89,             │
│   caption: "A man holding..."}  │
│  {...}]                         │
└──────┬──────────────────────────┘
       │
       ▼
┌──────────────┐
│ Browser      │
│ displays     │
│ results in   │
│ grid layout  │
└──────────────┘
```

## Vector Similarity Concept

```
Imagine a 384-dimensional space (simplified to 2D here):

    High
     ^
     |
     |    • "cat"          • "kitten"
     |         (close together = similar)
     |
     |
     |              • "car"
     |
     |    • "dog"           • "automobile"
     |         (close together)
     |
     |
     |                            • "building"
     |
     +----------------------------------------> Low
                    Dimension 1

When you search for "kitten":
1. Convert "kitten" to a point in this space
2. Find the closest points
3. "cat" will be very close → High similarity!
4. "building" will be far → Low similarity

This is why semantic search works!
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     IMAGE UPLOAD                             │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│  File System                                                 │
│  uploads/photo.jpg (original image saved)                   │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│  LLaVA Model (GPU/CPU)                                      │
│  Analyzes image → Generates caption                         │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│  Sentence-Transformer Model (CPU)                           │
│  Caption → 384-dimensional vector                           │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│  ChromaDB (Persistent Storage)                              │
│  chroma_db/                                                 │
│  ├── image_path: "photo.jpg"                                │
│  ├── caption: "A man holding a gun..."                      │
│  └── embedding: [0.23, -0.45, 0.67, ...]                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      SEARCH QUERY                            │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│  Sentence-Transformer Model                                 │
│  Query text → 384-dimensional vector                        │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│  ChromaDB Vector Search                                     │
│  Cosine similarity with all stored vectors                  │
│  Returns: Top N most similar                                │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│  Results                                                     │
│  [{image_path, caption, similarity_score}, ...]             │
└─────────────────────────────────────────────────────────────┘
```

## Three-Page Structure

```
┌───────────────────────────────────────────────────────────┐
│                    NAVIGATION BAR                          │
│  [Upload & Index] [Search Images] [Gallery] [42 images]   │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                   PAGE 1: Upload & Index                   │
├───────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────┐          │
│  │  Drag & Drop Images Here or Click to Browse │          │
│  │                                             │          │
│  │              📁 Upload Zone                 │          │
│  └─────────────────────────────────────────────┘          │
│                                                           │
│  Progress: [████████░░] 80%                              │
│  ✓ photo1.jpg: "A man holding a gun..."                 │
│  ✓ photo2.jpg: "Outdoor landscape with trees..."        │
│  ⏳ photo3.jpg: Processing...                           │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                   PAGE 2: Search Images                    │
├───────────────────────────────────────────────────────────┤
│  [Search: "a man holding a gun"_______________] [Search]  │
│                                                           │
│  Example searches: [person] [outdoor] [food] [animal]    │
│                                                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                 │
│  │ Image 1  │ │ Image 2  │ │ Image 3  │                 │
│  │ 89% match│ │ 67% match│ │ 45% match│                 │
│  └──────────┘ └──────────┘ └──────────┘                 │
│  "A man..."   "Person..."   "Urban..."                   │
└───────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────┐
│                   PAGE 3: Gallery                          │
├───────────────────────────────────────────────────────────┤
│  Total: 42 images          View: [⊞ Grid] [☰ List]       │
│                                                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ Image 1  │ │ Image 2  │ │ Image 3  │ │ Image 4  │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
│  "Caption 1" "Caption 2"   "Caption 3"  "Caption 4"     │
│                                                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │ Image 5  │ │ Image 6  │ │ Image 7  │ │ Image 8  │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │
└───────────────────────────────────────────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND                              │
│  • HTML5 (templates/base.html, upload, search, gallery) │
│  • CSS3 (embedded styles, responsive)                   │
│  • JavaScript (vanilla, no frameworks)                  │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST API
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    BACKEND                               │
│  • Flask 3.0.0 (web framework)                          │
│  • Python 3.8+ (programming language)                   │
└────┬────────────────┬─────────────────┬─────────────────┘
     │                │                 │
     ▼                ▼                 ▼
┌─────────┐   ┌──────────────┐   ┌────────────────┐
│  LLaVA  │   │   Vector DB   │   │  Text Embed   │
│  0.5B   │   │   ChromaDB    │   │  MiniLM-L6    │
│ Model   │   │   0.4.22      │   │               │
└─────────┘   └──────────────┘   └────────────────┘
     │                │                 │
     ▼                ▼                 ▼
┌─────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE                         │
│  • PyTorch 2.2.0 (ML framework)                         │
│  • CUDA / CPU (compute)                                 │
│  • File System (image storage)                          │
│  • Persistent Storage (vector database)                 │
└─────────────────────────────────────────────────────────┘
```

This complete workflow shows how all components work together to create a powerful semantic image search system!

