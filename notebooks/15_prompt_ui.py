from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

st.header("Research Tool")
user_input = st.text_input('Enter your prompt')
if st.button('Summarize'):
    result = model.invoke(user_input)
    st.write(result.content)