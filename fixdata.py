import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Now the Vision API will find the credentials
from google.cloud import vision

client = vision.ImageAnnotatorClient()

