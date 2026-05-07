def calculator(expression):
    return eval(expression)

tools = {
    "calculator": calculator
}

# Send it back to LLM again
# The LLM needs to:
# understand what happened
# use the result
# decide next step