from dotenv import load_dotenv
import os
load_dotenv()
import google.generativeai as genai

# Configure the API with your Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_llm(prompt):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    response = model.generate_content(prompt)
    return response.text