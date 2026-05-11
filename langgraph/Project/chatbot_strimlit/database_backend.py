from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage,HumanMessage
import sqlite3

load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite')


# Initialize state
class ChatState(TypedDict):

    messages : Annotated[list[BaseMessage],add_messages]

# Creating node
def chat_node(state:ChatState):

    user_message = state['messages']

    response =  llm.invoke(user_message)

    return {'messages':[response]}

# Initialize graph
graph = StateGraph(ChatState)

# Initialized Database
conn = sqlite3.connect(database='connect.db',check_same_thread=False)


# Initialize Checkpointer SqliteSaver
checkpointer = SqliteSaver(conn=conn)

# Adding Nodes
graph.add_node('chat_node',chat_node)

# Adding edges
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrive_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)