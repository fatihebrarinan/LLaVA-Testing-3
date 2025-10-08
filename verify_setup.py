"""
Quick setup verification script for LLaVA Image Search
Checks if all components are properly installed and can be imported
"""

print("=" * 60)
print("LLaVA Image Search - Setup Verification")
print("=" * 60)
print()

# Track any errors
errors = []
warnings = []

# 1. Check Python version
print("1. Checking Python version...")
import sys
if sys.version_info >= (3, 8):
    print(f"   ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
else:
    errors.append("Python 3.8+ required")
    print(f"   ✗ Python version too old: {sys.version_info}")
print()

# 2. Check Flask
print("2. Checking Flask...")
try:
    import flask
    print(f"   ✓ Flask {flask.__version__}")
except ImportError:
    errors.append("Flask not installed")
    print("   ✗ Flask not found")
print()

# 3. Check PyTorch
print("3. Checking PyTorch...")
try:
    import torch
    print(f"   ✓ PyTorch {torch.__version__}")
    
    # Check CUDA availability
    if torch.cuda.is_available():
        print(f"   ✓ CUDA available: {torch.cuda.get_device_name(0)}")
        print(f"   ✓ CUDA version: {torch.version.cuda}")
    else:
        warnings.append("CUDA not available - will use CPU (slower)")
        print("   ⚠ CUDA not available - will use CPU mode")
except ImportError:
    errors.append("PyTorch not installed")
    print("   ✗ PyTorch not found")
print()

# 4. Check Transformers
print("4. Checking Transformers...")
try:
    import transformers
    print(f"   ✓ Transformers {transformers.__version__}")
except ImportError:
    errors.append("Transformers not installed")
    print("   ✗ Transformers not found")
print()

# 5. Check ChromaDB
print("5. Checking ChromaDB...")
try:
    import chromadb
    print(f"   ✓ ChromaDB {chromadb.__version__}")
except ImportError:
    errors.append("ChromaDB not installed")
    print("   ✗ ChromaDB not found")
print()

# 6. Check Sentence Transformers
print("6. Checking Sentence Transformers...")
try:
    import sentence_transformers
    print(f"   ✓ Sentence Transformers {sentence_transformers.__version__}")
except ImportError:
    errors.append("Sentence Transformers not installed")
    print("   ✗ Sentence Transformers not found")
print()

# 7. Check PIL
print("7. Checking Pillow (PIL)...")
try:
    import PIL
    print(f"   ✓ Pillow {PIL.__version__}")
except ImportError:
    errors.append("Pillow not installed")
    print("   ✗ Pillow not found")
print()

# 8. Check file structure
print("8. Checking file structure...")
import os
required_files = [
    "app.py",
    "llava_backend.py",
    "vector_db.py",
    "requirements.txt",
    "templates/base.html",
    "templates/upload.html",
    "templates/search.html",
    "templates/gallery.html"
]

for file in required_files:
    if os.path.exists(file):
        print(f"   ✓ {file}")
    else:
        errors.append(f"Missing file: {file}")
        print(f"   ✗ {file} not found")
print()

# 9. Check LLaVA-NeXT directory
print("9. Checking LLaVA-NeXT...")
if os.path.exists("LLaVA-NeXT"):
    print("   ✓ LLaVA-NeXT directory exists")
    
    # Try to import LLaVA modules
    sys.path.insert(0, "LLaVA-NeXT")
    try:
        from llava.model.builder import load_pretrained_model
        print("   ✓ LLaVA modules can be imported")
    except ImportError as e:
        warnings.append(f"LLaVA import issue: {e}")
        print(f"   ⚠ LLaVA import issue: {e}")
else:
    errors.append("LLaVA-NeXT directory not found")
    print("   ✗ LLaVA-NeXT directory not found")
print()

# 10. Create necessary directories
print("10. Creating required directories...")
dirs_to_create = ["uploads", "chroma_db"]
for dir_name in dirs_to_create:
    os.makedirs(dir_name, exist_ok=True)
    print(f"   ✓ {dir_name}/")
print()

# Summary
print("=" * 60)
print("SUMMARY")
print("=" * 60)

if errors:
    print(f"\n❌ {len(errors)} ERROR(S) FOUND:")
    for error in errors:
        print(f"   - {error}")
    print("\n⚠️  Please install missing dependencies:")
    print("   pip install -r requirements.txt")
    
    if "LLaVA-NeXT directory not found" in errors:
        print("\n⚠️  Please clone LLaVA-NeXT:")
        print("   git clone https://github.com/LLaVA-VL/LLaVA-NeXT.git")
        print("   cd LLaVA-NeXT && pip install -e . && cd ..")

if warnings:
    print(f"\n⚠️  {len(warnings)} WARNING(S):")
    for warning in warnings:
        print(f"   - {warning}")

if not errors:
    print("\n✅ All checks passed! You're ready to run the application.")
    print("\nTo start the server:")
    print("   python app.py")
    print("\nThen open your browser to:")
    print("   http://localhost:5000")
    print("\nNote: The first request will download the LLaVA model (~3GB)")

print("=" * 60)

