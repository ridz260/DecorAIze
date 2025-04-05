import os
import requests
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw, ImageFont
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

API_KEY = os.getenv("TOGETHER_AI")

def generate_placeholder_image(style, room_type, object_input, details):
    """Generate a placeholder image with design details as text"""
    try:
        # Create a white canvas
        image = Image.new('RGB', (1280, 720), color='white')
        draw = ImageDraw.Draw(image)
        
        # Prepare text content
        content = f"Style: {style}\nRoom: {room_type}\nObjects: {object_input}\nDetails: {details}"
        
        # Try to load a font
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = None  # fallback to default font
            
        # Draw text on image
        draw.text((50, 50), content, fill="black", font=font)
        
        return image
    except Exception as e:
        logger.error(f"Error generating placeholder image: {str(e)}")
        return None

def generate_image_with_api(style, room_type, object_input, details):
    """Generate image using Together AI API"""
    if not API_KEY:
        logger.error("API key not found in environment variables")
        return None
        
    try:
        prompt = f"generate an interior design for {style}, {room_type} with {object_input}. Extra details include {details}"
        
        client = InferenceClient(
            provider="together",
            api_key=API_KEY
        )
        
        return client.text_to_image(
            prompt=prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0"
        )
    except Exception as e:
        logger.error(f"API image generation failed: {str(e)}")
        return None

def generate_image(style: str, room_type: str, object_input: str, details: str):
    """Main image generation function with fallback mechanism"""
    # First try API generation
    image = generate_image_with_api(style, room_type, object_input, details)
    
    # If API fails, use placeholder
    if image is None:
        logger.info("Falling back to placeholder image")
        image = generate_placeholder_image(style, room_type, object_input, details)
    
    # Save the image
    if image:
        try:
            output_dir = os.path.join(os.getcwd(), 'src', 'static')
            os.makedirs(output_dir, exist_ok=True)
            image_path = os.path.join(output_dir, 'generated_image.png')
            image.save(image_path)
            return True
        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            return False
    return False
