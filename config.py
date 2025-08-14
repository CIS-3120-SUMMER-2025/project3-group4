import os
from dotenv import load_dotenv

load_dotenv()

# EXERCISE API
NINJA_API_TOKEN = os.getenv("NINJA_API_TOKEN")

# Ollama model because llama2 was too big
OLLAMA_MODEL = "llama3.2:1b"  

# Goal mapping for exercises based on ninja api types
GOAL_MAP = {
    "strength": ["strength", "olympic_weightlifting", "powerlifting", "strongman"],
    "flexibility": ["stretching"],
    "cardio": ["cardio", "plyometrics"],
}