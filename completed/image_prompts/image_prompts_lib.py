# Import required AWS and utility libraries
import boto3
import json
import base64
from io import BytesIO
from random import randint

def get_image_generation_request_body(prompt, negative_prompt=None):
    """
    Prepares the JSON request body for Nova Canvas image generation
    Args:
        prompt (str): The main text prompt describing what to generate
        negative_prompt (str, optional): Text describing what to avoid in the image
    Returns:
        str: JSON formatted request body
    """
    # Create the base request structure
    body = {
        "taskType": "TEXT_IMAGE",  # Specify we want text-to-image generation
        "textToImageParams": {
            "text": prompt,  # Main prompt text
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,    # Generate single image
            "quality": "premium",   # Use highest quality setting
            "height": 512,          # Image height in pixels
            "width": 512,           # Image width in pixels
            "cfgScale": 8.0,       # Controls how closely the image follows the prompt
            "seed": randint(0, 100000),  # Random seed for variety
        },
    }
    
    # Add negative prompt if provided
    if negative_prompt:
        body['textToImageParams']['negativeText'] = negative_prompt
    
    # Convert dictionary to JSON string
    return json.dumps(body)

def get_response_image(response):
    """
    Processes the Nova Canvas response and extracts the image
    Args:
        response: Raw response from Bedrock API
    Returns:
        BytesIO: Image data as a bytes stream
    """
    # Parse the JSON response body
    response = json.loads(response.get('body').read())
    
    # Extract the base64 encoded image array
    images = response.get('images')
    
    # Decode the first (and only) image from base64
    image_data = base64.b64decode(images[0])

    # Return as BytesIO object for easy handling
    return BytesIO(image_data)

def get_image_from_model(prompt_content, negative_prompt=None):
    """
    Main function to generate images using Nova Canvas
    Args:
        prompt_content (str): Main prompt describing desired image
        negative_prompt (str, optional): Things to avoid in the image
    Returns:
        BytesIO: Generated image as bytes stream
    """
    # Create AWS session and Bedrock client
    session = boto3.Session()
    bedrock = session.client(service_name='bedrock-runtime', region_name='us-east-1')
    
    # Prepare the request body
    body = get_image_generation_request_body(prompt_content, negative_prompt=negative_prompt)
    
    # Call Nova Canvas model through Bedrock
    response = bedrock.invoke_model(
        body=body,
        modelId="amazon.nova-canvas-v1:0",  # Specify Nova Canvas model
        contentType="application/json",
        accept="application/json"
    )
    
    # Process the response and return image
    output = get_response_image(response)
    
    return output