"""
Example API usage script for LLaVA Image Search
Demonstrates how to interact with the API programmatically
"""
import requests
import json
import os
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:5000"

def index_image(image_path):
    """Upload and index an image"""
    print(f"\n📤 Indexing image: {image_path}")
    
    url = f"{API_BASE_URL}/api/index-image"
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✅ Success!")
            print(f"   Caption: {data['caption']}")
            print(f"   URL: {data['url']}")
            return data
        else:
            print(f"❌ Error: {data.get('error', 'Unknown error')}")
            return None
    else:
        print(f"❌ HTTP Error {response.status_code}")
        return None

def search_images(query, n_results=5):
    """Search for images by text query"""
    print(f"\n🔍 Searching for: '{query}'")
    
    url = f"{API_BASE_URL}/api/search-images"
    payload = {
        "query": query,
        "n_results": n_results
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✅ Found {data['count']} result(s)")
            for i, result in enumerate(data['results'], 1):
                similarity = result['similarity'] * 100
                print(f"\n   {i}. Similarity: {similarity:.1f}%")
                print(f"      Image: {result['image_path']}")
                print(f"      Caption: {result['caption'][:80]}...")
            return data['results']
        else:
            print(f"❌ Error: {data.get('error', 'Unknown error')}")
            return None
    else:
        print(f"❌ HTTP Error {response.status_code}")
        return None

def get_all_images():
    """Get all indexed images"""
    print("\n📚 Retrieving all indexed images...")
    
    url = f"{API_BASE_URL}/api/get-all-images"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            print(f"✅ Total images in database: {data['count']}")
            for i, image in enumerate(data['results'][:5], 1):  # Show first 5
                print(f"   {i}. {image['image_path']}")
                print(f"      Caption: {image['caption'][:60]}...")
            
            if data['count'] > 5:
                print(f"   ... and {data['count'] - 5} more")
            
            return data['results']
        else:
            print(f"❌ Error: {data.get('error', 'Unknown error')}")
            return None
    else:
        print(f"❌ HTTP Error {response.status_code}")
        return None

def get_stats():
    """Get database statistics"""
    url = f"{API_BASE_URL}/api/stats"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            return data['total_images']
    return 0

def main():
    """Main example workflow"""
    print("=" * 70)
    print("LLaVA Image Search - API Usage Example")
    print("=" * 70)
    
    # Check if server is running
    try:
        stats = get_stats()
        print(f"\n✅ Server is running")
        print(f"📊 Current database size: {stats} images")
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Server is not running!")
        print("Please start the server with: python app.py")
        return
    
    # Example 1: Index an image (if you have one)
    print("\n" + "=" * 70)
    print("Example 1: Index an Image")
    print("=" * 70)
    
    # Check if there are any images in uploads folder
    uploads_dir = Path("uploads")
    if uploads_dir.exists():
        images = list(uploads_dir.glob("*.jpg")) + list(uploads_dir.glob("*.png"))
        if images:
            # Index the first image
            sample_image = images[0]
            print(f"Using existing image: {sample_image}")
            result = index_image(sample_image)
        else:
            print("No images found in uploads/ folder")
            print("Please upload some images first using the web UI")
    else:
        print("uploads/ folder doesn't exist yet")
        print("Please upload some images first using the web UI")
    
    # Example 2: Get all images
    print("\n" + "=" * 70)
    print("Example 2: Get All Images")
    print("=" * 70)
    all_images = get_all_images()
    
    # Example 3: Search
    if all_images and len(all_images) > 0:
        print("\n" + "=" * 70)
        print("Example 3: Search for Images")
        print("=" * 70)
        
        # Try a few example queries
        queries = [
            "a person",
            "outdoor scene",
            "object on table"
        ]
        
        for query in queries:
            results = search_images(query, n_results=3)
            if results:
                break  # Found some results, stop
    else:
        print("\n⚠️  No images in database yet. Upload some first!")
    
    # Example 4: Batch indexing (commented out - uncomment to use)
    print("\n" + "=" * 70)
    print("Example 4: Batch Indexing (example code)")
    print("=" * 70)
    print("""
# To batch index multiple images:

image_folder = Path("my_images/")
for image_path in image_folder.glob("*.jpg"):
    result = index_image(image_path)
    if result:
        print(f"Indexed: {image_path.name}")
    """)
    
    print("\n" + "=" * 70)
    print("Examples complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()

