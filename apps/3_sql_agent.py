from dotenv import load_dotenv
load_dotenv()

# db,llm,tools,create_agent,system_prompt

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

db = SQLDatabase.from_uri("sqlite:///my_task.db")

db.run("""
     CREATE TABLE IF NOT EXISTS tasks
       (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT CHECK
            (
                status IN('pending','in_progress','completed')
            ) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
       )
""")

## LLM, Tools, memeory, system prompt

# 1) LLM

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# 2) Tools
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()

# 3) Memory
memory = InMemorySaver()

# 4) System
# System prompt is imp for building high level of model or agent.
# because system prompt explains to our model what you can do or what you can't do.
# In system prompt we defaine all rules 

system_prompt = """
    You are task management assistant that interact with a SQL database connecting a 'tasks' table.

    TASK RULES :
    1. Limit SELECT queries to 10 results max with ORDER BY created_at DESC.
    2. After CREATE/UPDATE/DELETE, confirm with SELECT query.
    3. If the user requests a list of tasks, present the output in a structurd table format to ensure a clean and organized display in the browser.
    
    CRUD OPERATIONS:
        CREATE: INSERT INTO tasks(title,description, status)
        READ: SELECT * from tasks WHERE ...LIMIT 10
        UPDATE: UPDATE tasks SET status=? WHERE id=? OR title=?
        DELETE: DELETE FROM tasks WHERE id=? OR title=?

    Table schema: id, title, description, status(pending/progress/completed), created_at. 
"""

## Create agent

agent = create_agent(
    model = model,
    tools=tools,
    checkpointer=memory,
    system_prompt=system_prompt
    )

while True:
    query = input("User :")
    response = agent.invoke(
        {"messages":[{"role":"user","content":query}]},
        {"configurable":{"thread_id":"1"}}
    )

    result = response["messages"][-1].content[0]["text"]
    print("AI :", result)

    