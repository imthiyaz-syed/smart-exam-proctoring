# 1. Make sure you load the .env file (very common oversight)
from dotenv import load_dotenv
load_dotenv()               # ← Add this if not already present

# 2. Now import and use the modern Google Gen AI SDK
from google import genai

# The client automatically reads GEMINI_API_KEY from environment
client = genai.Client()

# Generate content (your model name is valid for preview access)
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain how AI works in a few words"
)

print(response.text)