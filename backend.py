from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from gemini_helper import get_gemini_response  # now importing from helper
import io

app = FastAPI()

# Allow frontend (React, Streamlit, or any other client) to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (change to specific domain in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Read uploaded file into bytes
    contents = await file.read()

    # Prepare image parts for Gemini
    image_parts = [
        {
            "mime_type": file.content_type,  # e.g. "image/png"
            "data": contents
        }
    ]

    prompt = """
    You are a nutritionist. Analyze the food items in the image and calculate:
    1. Calories per food item
    2. Total calories
    3. Whether the food is healthy or not
    Format:
    1. Item 1 - calories
    2. Item 2 - calories
    ...
    Total: ___ calories
    Healthiness: ___
    """

    # Call Gemini
    response = get_gemini_response(prompt, image_parts)

    return {"result": response}
