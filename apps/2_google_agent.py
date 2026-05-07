from dotenv import load_dotenv
load_dotenv()

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
search = GoogleSerperAPIWrapper()
memory = MemorySaver()

system_prompt = """
You are a helpful AI agent.

For ANY question about:
- current events
- sports results
- recent information

You MUST ALWAYS use the google_search tool before answering.
Do NOT answer from your own knowledge.
"""

# print(search.run("India cricket news"))

@tool
def google_search(query: str) -> str:
    """Search Google for real-time information."""
    return search.run(query)

agent = create_agent(
    model=model,
    tools=[google_search],
    checkpointer=memory,
    system_prompt=system_prompt
)

while True:
    query = input("User:")
    if query.lower() == "quit":
        print("Good bye")
        break

    res = agent.invoke(
         {"messages":[{"role":"user","content":query}]},
    {
        "configurable": {"thread_id": "1"},
        "recursion_limit": 10
    }
    )

    print("AI:", res["messages"][-1].content[0]["text"])