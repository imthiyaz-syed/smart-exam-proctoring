import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure your API key from environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List available models and check their supported methods
for m in genai.list_models():
    print(f"Model Name: {m.name}")
    print(f"Supported Methods: {m.supported_generation_methods}")
    if "generateContent" in m.supported_generation_methods:
        print(f"Model {m.name} supports content generation.")
    if "generateImage" in m.supported_generation_methods:
        print(f"Model {m.name} supports image generation.")
    print("-" * 30)
