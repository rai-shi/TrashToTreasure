"""Gemini API connection configuration"""
import google.generativeai as genai

# Configure Gemini API
from dotenv import load_dotenv
import os

# Load environment variables from root directory
current_directory = os.path.dirname(os.path.abspath(__file__)) # utils directory, routers
backend_directory = os.path.dirname(current_directory) # backend directory

environment_path = backend_directory + "/.env"
load_dotenv(environment_path)
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
