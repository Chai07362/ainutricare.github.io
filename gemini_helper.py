import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create Gemini model once (v1 API)
model = genai.GenerativeModel("gemini-2.5-flash")

def get_gemini_response(input_prompt, image_parts):
    response = model.generate_content([input_prompt, image_parts[0]])
    return response.text
