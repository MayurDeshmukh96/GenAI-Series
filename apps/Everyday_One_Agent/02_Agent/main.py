from agent import ReActAgent

agent = ReActAgent()

goal = input("Enter your goal :")

result = agent.run(goal)

print("\n Final Output\n", result)