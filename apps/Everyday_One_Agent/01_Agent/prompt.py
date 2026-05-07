def build_prompt(goal):
    prompt = f"""
    You are an intelligent AI agent.

    Your task is to achieve the user's goal.

    Goal : {goal}

    You must think step by step and respond in the following format:

    Thought:
    Explain how you understand the goal.

    Plan:
    Explain your strategy.

    Steps:
    1.
    2.
    3.

    Final Answer:
    Provide the final response to the user.
    """
    return prompt