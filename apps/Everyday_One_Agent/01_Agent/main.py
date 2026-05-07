from agent import GaolAgent

goal = input("Enter Your Goal :")

agent = GaolAgent()

result = agent.run(goal)

print(result)