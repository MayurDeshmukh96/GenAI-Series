from llm import ask_llm
from prompt import build_prompt

class GaolAgent:
    def run(self,goal):
        prompt = build_prompt(goal)

        response = ask_llm(prompt)

        return response