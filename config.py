import os

#local 
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

#Streamlit api 

# Gemini API Key (set in Streamlit secrets or env var)
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

TEMP_DIR = "temp"
FRAMES_DIR = f"{TEMP_DIR}/frames"
AUDIO_PATH = f"{TEMP_DIR}/audio.wav"
