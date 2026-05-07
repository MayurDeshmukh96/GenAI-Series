from crewai import Agent
from tools import search_tool
        
research_agent = Agent(
    role = "{topic} Researcher",
    goal = "Find accurate information about {topic} topics.",
    backstory = "You are an expert {topic} resercher who gather reliable information",
    verbose = True,
    tools = [search_tool]
)


writer_agent = Agent(
    role = "{topic} Content writer",
    goal = "Write an content about {topic} topic which are engaging and informative",
    backstory = "You are an expert {topic} content writer who write engaging and informative content",
    verbose = True
)