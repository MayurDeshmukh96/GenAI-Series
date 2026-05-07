from dotenv import load_dotenv
import os

# the .env file lives in the notebooks directory so point dotenv there
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "notebooks", ".env"))

from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError(
        "Gemini API key not found.  Set GEMINI_API_KEY or GOOGLE_API_KEY "
        "in your environment or .env file."
    )

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

st.title("AskBuddy -  AI ChatBot")
st.markdown("My QnA Bot with langchain and google gemini !")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)


query = st.chat_input("Ask anything ?")
if query:
    st.session_state.messages.append({"role":"user", "content":query})
    st.chat_message("user").markdown(query)
    res = llm.invoke(query)
    st.chat_message("ai").markdown(res.content)
    st.session_state.messages.append({"role":"ai","content":res.content})

