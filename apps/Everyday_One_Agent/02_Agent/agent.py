from tools import tools 
from llm import ask_llm
from prompt import system_prompt

class ReActAgent:
    def run(self,goal):

        messages = [
            {"role":"system","content":system_prompt},
            {"role":"user","content":goal}
        ]

        for step in range(5):
            response = ask_llm(messages)

            print("\n LLM Response:\n", response)

            messages.append({"role":"assistant","content":response})

            # check final answer
            if "Final Answer" in response:
                break

            # extract action

            if "Action:" in response:
                action : response.split("Action:")[1].split("\n")[0].strip()
                action_input : response.split("Action Input:")[1].split("\n")[0].strip()

                if action in tools:
                    result = tools[action](action_input)
                else:
                    result = "Unknown tool"
                
                observation = f"Observation: {result}"

                messages.append({"role" : "user", "content":observation})
        return response