"""
Vector Database for Image-Caption Storage and Search
Uses ChromaDB for vector storage and sentence-transformers for embeddings
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os
from pathlib import Path
import json
from typing import List, Dict, Optional


class ImageCaptionVectorDB:
    """Vector database for storing and searching image-caption pairs"""
    
    def __init__(self, persist_directory="./chroma_db"):
        """
        Initialize the vector database
        
        Args:
            persist_directory: Directory to persist the database
        """
        self.persist_directory = persist_directory
        Path(persist_directory).mkdir(exist_ok=True)
        
        # Initialize ChromaDB with persistent storage
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Load embedding model (lightweight but effective)
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Embedding model loaded!")
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection("image_captions")
            print(f"Loaded existing collection with {self.collection.count()} items")
        except:
            self.collection = self.client.create_collection(
                name="image_captions",
                metadata={"description": "Image-caption pairs for semantic search"}
            )
            print("Created new collection")
    
    def add_image(self, image_path: str, caption: str, metadata: Optional[Dict] = None):
        """
        Add an image-caption pair to the database
        
        Args:
            image_path: Path to the image file (relative to uploads folder)
            caption: Caption/description of the image
            metadata: Optional additional metadata
        """
        # Generate embedding from caption
        embedding = self.embedding_model.encode(caption).tolist()
        
        # Prepare metadata
        meta = {
            "image_path": image_path,
            "caption": caption
        }
        if metadata:
            meta.update(metadata)
        
        # Use image path as unique ID (replace slashes and special chars)
        doc_id = image_path.replace("/", "_").replace("\\", "_").replace(".", "_")
        
        # Add to collection
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[caption],
            metadatas=[meta]
        )
        
        print(f"Added image: {image_path}")
    
    def search(self, query_text: str, n_results: int = 10) -> List[Dict]:
        """
        Search for images by text query
        
        Args:
            query_text: Text query to search for
            n_results: Number of results to return
            
        Returns:
            List of dictionaries containing image_path, caption, and similarity
        """
        if self.collection.count() == 0:
            return []
        
        # Generate embedding for query
        query_embedding = self.embedding_model.encode(query_text).tolist()
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self.collection.count())
        )
        
        # Format results
        formatted_results = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'image_path': results['metadatas'][0][i]['image_path'],
                    'caption': results['metadatas'][0][i]['caption'],
                    'similarity': 1 - results['distances'][0][i],  # Convert distance to similarity
                    'distance': results['distances'][0][i]
                })
        
        return formatted_results
    
    def get_all(self) -> List[Dict]:
        """
        Get all image-caption pairs in the database
        
        Returns:
            List of dictionaries containing image_path and caption
        """
        if self.collection.count() == 0:
            return []
        
        # Get all items from collection
        results = self.collection.get()
        
        # Format results
        formatted_results = []
        if results['ids']:
            for i in range(len(results['ids'])):
                formatted_results.append({
                    'image_path': results['metadatas'][i]['image_path'],
                    'caption': results['metadatas'][i]['caption']
                })
        
        return formatted_results
    
    def delete_image(self, image_path: str):
        """
        Delete an image-caption pair from the database
        
        Args:
            image_path: Path to the image file
        """
        doc_id = image_path.replace("/", "_").replace("\\", "_").replace(".", "_")
        try:
            self.collection.delete(ids=[doc_id])
            print(f"Deleted image: {image_path}")
        except Exception as e:
            print(f"Error deleting image {image_path}: {e}")
    
    def clear_all(self):
        """Clear all data from the database"""
        # Delete and recreate collection
        self.client.delete_collection("image_captions")
        self.collection = self.client.create_collection(
            name="image_captions",
            metadata={"description": "Image-caption pairs for semantic search"}
        )
        print("Database cleared")
    
    def count(self) -> int:
        """Get the number of items in the database"""
        return self.collection.count()


# Global database instance
_db_instance = None


def get_db():
    """Get or create the global database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = ImageCaptionVectorDB()
    return _db_instance

