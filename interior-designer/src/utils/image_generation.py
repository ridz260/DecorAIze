import requests
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load API key securely
load_dotenv()
API_KEY = os.getenv("TOGETHER_AI")  # Store in a .env file or set as an environment variable


def generate_image(style :str, room_type : str, object_input : str, details : str):
    prompt = f"generate an interior design for {style}, {room_type} with {object_input}. Extra details include {details}"

    client = InferenceClient(
    provider="together",
    api_key="1ae66c63da71094c2bafa36ac7c06d5ca6478e98afc23e75c7fddae8eaa99126"
    )

    # output is a PIL.Image object
    image = client.text_to_image(
        prompt = prompt,
        model="stabilityai/stable-diffusion-xl-base-1.0"
    )

    if image:
        image.save('./src/static/generated_image.png')
    else:
        return 'Error Generating Image.'
    