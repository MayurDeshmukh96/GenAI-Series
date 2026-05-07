from crewai import task
from agents import research_agent, writer_agent

research_task = task(
    description = "Research about the topic {topic}",
    expected_output = "Detailed research on the {topic}",
    agent = research_agent
)

writer_task = task(
    description = "Write a blog post about the topic {topic}",
    expected_output = "Blog post on the {topic}",
    agent = writer_agent
)