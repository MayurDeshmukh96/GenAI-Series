import streamlit as st
from database_backend import chatbot,retrive_all_threads
from langchain_core.messages import HumanMessage
import uuid


def generate_thread_id():
    # It generate random thread ID for our conversation.
    thread_uuid = uuid.uuid4()
    return thread_uuid

def reset_chat():
    thread_id =  generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_threads(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_threads(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(
        config={'configurable':{'thread_id':thread_id}}
        )
    
    if state and 'messages' in state.values:
        return state.values['messages']
    
    return []


# ---------------------------------- Session setup --------------------------------------------
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Here if thread_id is not present in the session state means it is a new thread_id
# Now we want to add it in session state
# That's the meaning of belows code - if thread_id not in session state then in st.session_state['thread_id'] generate new thread_id

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

# Here we are buildeing conversation thread display functionality
# If chat_threads list is not present in session_state then create new thread 
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrive_all_threads()

add_threads(st.session_state['thread_id'])

# ---------------------------------- Sidebar UI ----------------------------------------------

st.sidebar.title("Langgraph chatbot")

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My conversation')
for thread_id in st.session_state['chat_threads']:
    if st.sidebar.button(str(thread_id)): # Showing thread IDs of conversation
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        temp_messages = []

        for message in messages:
            if isinstance(message,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role,'content':message.content})
        st.session_state['message_history'] = temp_messages
# ---------------------------------- Main UI -------------------------------------------------
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input('Type here')

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})

    
    CONFIG = {'configurable':{'thread_id':st.session_state['thread_id']}}

    with st.chat_message('user'):
        st.text(user_input)
    
    response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=CONFIG)

    ai_message = response['messages'][-1].content

    st.session_state['message_history'].append({'role':'assistant','content':ai_message})

    with st.chat_message('assistant'):
        st.text(ai_message)