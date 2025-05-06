import os
import base64
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
import google.generativeai as generativeai
import io
import argparse

environment_path = os.path.dirname(os.path.abspath(__file__)) + "/.env"
load_dotenv(environment_path)

API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise ValueError('GEMINI_API_KEY environment variable is not set')

generativeai.configure(api_key=API_KEY) 

MODEL = generativeai.GenerativeModel('gemini-2.0-flash' )

CLIENT = genai.Client(api_key=API_KEY)


def create_system_prompt():
    """Create the system prompt for Gemini."""
    return """
    You are an assistant that generates upcycling 3 DIY project ideas from an item image.

    Return your response strictly as a JSON array. Each element must have:
    - title (string)
    - description (string)
    - materials (list of strings)
    - roadmap (list of step strings)

    Example format:
    [
      {
        "title": "Project Name",
        "description": "Project short description",
        "materials": ["Material 1", "Material 2"],
        "roadmap": [
            "Step 1",
            "Step 2",
            "Step 3"
        ]
      }
    ]

    Input will be an image of a recyclable item.
    Respond have to be only in the above JSON format.
    """

def load_image(image_path):
    with open(image_path, 'rb') as f:
      image_bytes = f.read()
    return image_bytes

def process_image_with_gemini(image_path):
    prompt = create_system_prompt()
    image = load_image(image_path)
    try:
        response = CLIENT.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=[
                        types.Part.from_bytes(
                            data=image,
                            mime_type='image/jpeg',
                        ),
                        prompt
                    ]
                )
        response_text = response.text
        response_text = response_text.replace("`", "")
        response_text = response_text.replace("json", "")

        try:
            upcycling_ideas = json.loads(response_text)
            return upcycling_ideas
        except json.JSONDecodeError:
            print("Error: Gemini did not return valid JSON. Raw response:")
            print(response.text)
            return None
            
    except Exception as e:
        print(f"Error processing image with Gemini: {e}")
        return None