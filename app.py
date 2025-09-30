import streamlit as st
import google.generativeai as genai 
import os
from dotenv import load_dotenv
from PIL import Image
from gemini_helper import get_gemini_response
# Load environment variables
load_dotenv()




# Create the model once (not every call)
model = genai.GenerativeModel("gemini-2.5-flash")

def get_gemini_response(input_prompt, image):
    """
    Calls Gemini model with text + image.
    """
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    """
    Prepares image bytes for Gemini.
    """
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # e.g. "image/png"
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# --- Streamlit UI ---
st.set_page_config(page_title="Calories Calculator")

st.header("🍎 Calories Calculator")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=250)

submit = st.button("Tell me about the total calories") 

input_prompt = """
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

if submit and uploaded_file is not None:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.subheader("🔎 Analysis")
    st.write(response)
