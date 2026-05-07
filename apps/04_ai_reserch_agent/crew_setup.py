from crewai import Crew
from agents import research_agent, writer_agent
from task import research_task, writer_task

crew = Crew(
    agents = [research_agent, writer_agent],
    tasks = [research_task, writer_task],
    verbose = True
)
