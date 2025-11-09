import os
from dotenv import load_dotenv

load_dotenv()

# === API KEYS ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# === MODEL CONFIG ===
GROQ_MODEL = "llama-3.1-70b-versatile"

 # === SEARCH CONFIG ===
SERPAPI_KEY = os.getenv("SERPAPI_KEY")  