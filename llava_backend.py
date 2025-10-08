"""
LLaVA One Vision Backend
Handles model loading and inference for LLaVA One Vision
"""
import sys
import os
import torch
import warnings
from pathlib import Path
from PIL import Image
import copy

# Add LLaVA-NeXT to path
LLAVA_PATH = Path(__file__).parent / "LLaVA-NeXT"
sys.path.insert(0, str(LLAVA_PATH))

from llava.model.builder import load_pretrained_model
from llava.mm_utils import get_model_name_from_path, process_images, tokenizer_image_token
from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN
from llava.conversation import conv_templates

warnings.filterwarnings("ignore")


class LLaVABackend:
    """Backend for LLaVA One Vision model"""
    
    def __init__(self, model_path="lmms-lab/llava-onevision-qwen2-0.5b-si", device=None):
        """
        Initialize the LLaVA model
        
        Args:
            model_path: HuggingFace model ID or local path
            device: Device to run on ('cuda' or 'cpu'). Auto-detects if None.
        """
        self.model_path = model_path
        self.model_name = "llava_qwen"
        self.conv_template = "qwen_1_5"
        
        # Auto-detect device (prefer CUDA if available)
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            #Sets the variable device to device passes in as variable.
            self.device = device
        
        print(f"Loading LLaVA One Vision model on {self.device}...")
        print(f"Model: {model_path}")
        
        # Load model (disable flash attention for compatibility)
        self.tokenizer, self.model, self.image_processor, self.max_length = load_pretrained_model(
            self.model_path,
            None,
            self.model_name,
            attn_implementation=None,
            device_map="auto" if self.device == "cuda" else self.device
        )
        
        self.model.eval()
        print("Model loaded successfully!")
    
    def process_images_for_model(self, image_paths):
        """
        Process multiple images for the model
        
        Args:
            image_paths: List of paths to images
            
        Returns:
            Tuple of (image_tensors, image_sizes)
        """
        images = []
        for img_path in image_paths:
            try:
                image = Image.open(img_path).convert('RGB')
                images.append(image)
            except Exception as e:
                print(f"Error loading image {img_path}: {e}")
                continue
        
        if not images:
            return None, None
        
        # Process images
        image_tensors = process_images(images, self.image_processor, self.model.config)
        
        # Move to device with appropriate dtype
        if self.device == "cuda":
            image_tensors = [
                _image.to(dtype=torch.float16, device=self.device) 
                for _image in image_tensors
            ]
        else:
            image_tensors = [
                _image.to(device=self.device) 
                for _image in image_tensors
            ]
        
        image_sizes = [img.size for img in images]
        
        return image_tensors, image_sizes
    
    def generate_response(self, prompt, image_paths=None, max_new_tokens=2048, temperature=0.2, do_sample=True):
        """
        Generate a response from the model
        
        Args:
            prompt: Text prompt
            image_paths: Optional list of image paths
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            do_sample: Whether to use sampling
            
        Returns:
            Generated text response
        """
        # Build the question with image tokens if images provided
        if image_paths and len(image_paths) > 0:
            # Add image token for each image
            image_tokens = DEFAULT_IMAGE_TOKEN * len(image_paths)
            #First gives the image tokens, then the prompt.
            question = f"{image_tokens}\n{prompt}"
            
            # Process images
            image_tensors, image_sizes = self.process_images_for_model(image_paths)
            
            if image_tensors is None:
                return "Error: Could not process images!"
        else:
            question = prompt
            image_tensors = None
            image_sizes = None
        
        # Setup conversation
        conv = copy.deepcopy(conv_templates[self.conv_template])
        conv.append_message(conv.roles[0], question)
        conv.append_message(conv.roles[1], None)
        prompt_question = conv.get_prompt()
        
        # Tokenize the prompt
        input_ids = tokenizer_image_token(
            prompt_question,
            self.tokenizer,
            IMAGE_TOKEN_INDEX,
            return_tensors="pt"
        ).unsqueeze(0).to(self.device)
        
        # Generate the response
        with torch.inference_mode():
            output_ids = self.model.generate(
                input_ids,
                images=image_tensors,
                image_sizes=image_sizes,
                do_sample=do_sample,
                temperature=temperature if do_sample else 0,
                max_new_tokens=max_new_tokens,
                use_cache=True,
            )
        
        # Decode output
        outputs = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0].strip()
        
        return outputs
    
    def chat(self, prompt, image_paths=None):
        """
        Simple chat interface
        
        Args:
            prompt: User question/prompt
            image_paths: Optional list of image file paths
            
        Returns:
            Model response
        """
        return self.generate_response(prompt, image_paths)


# Global model instance (lazy loaded)
_model_instance = None


def get_model():
    """Get or create the global model instance"""
    global _model_instance
    if _model_instance is None:
        _model_instance = LLaVABackend()
    return _model_instance


def chat(prompt, image_paths=None):
    """
    Convenience function for chat
    
    Args:
        prompt: User question
        image_paths: Optional list of image paths
        
    Returns:
        Model response
    """
    model = get_model()
    return model.chat(prompt, image_paths)

