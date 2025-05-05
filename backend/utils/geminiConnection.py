"""Gemini API connection configuration"""
import google.generativeai as genai

# Configure Gemini API
from dotenv import load_dotenv
import os

# Load environment variables from root directory
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

# Get API key from environment variable
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise ValueError('GEMINI_API_KEY environment variable is not set')
genai.configure(api_key=API_KEY)

# Model configuration
GEMINI_MODEL = "gemini-1.5-flash"


def get_gemini_model():
    """Returns the configured Gemini model."""
    return genai.GenerativeModel(GEMINI_MODEL)
