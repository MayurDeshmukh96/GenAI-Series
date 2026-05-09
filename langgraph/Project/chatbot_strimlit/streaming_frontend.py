# Streaming

# In llm, streaming means the model starts sending tokens (words) as soon as they are starting generated, 
# Instead of waiting fro the entire response to ve ready before returning it.

# Why streaming :-

# 1) Faster response time - low drop off rate
# 2) Mimic human like conversion (build trust, feels alive and keeps the user engaged)
# 3) Important for multi model UIs
# 4) Better UX for long output.
# 5) You can cancel midway savings tokens
# 6) We can interleave UI updates





import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

config = {"configurable": {"thread_id": "thread-1"}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input('Type here')

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
# Added streaming here
    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config,
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
