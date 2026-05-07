# ============================================================
# Cell 1 - Imports
# ============================================================
from langchain_core.tools import tool
from dotenv import load_dotenv
import requests
import json
from langchain_core.messages import HumanMessage
load_dotenv()
import os
from langchain_groq import ChatGroq


# ============================================================
# Cell 2 - Tool Definitions
# FIX 1: Renamed 'base_currency' -> 'amount' in convert() to
#         avoid confusing the LLM (it was named like a currency
#         string but was actually a numeric amount).
# ============================================================
@tool
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
    """This fetches the currency conversion factor between base_currency and target_currency"""
    url = f"https://v6.exchangerate-api.com/v6/9df6e706193bf1f41ce9c91e/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    return response.json()


@tool
def convert(amount: float, conversion_factor: float) -> float:
    """Given a currency conversion rate this function calculates the target currency value from a given base amount."""
    return amount * conversion_factor


# ============================================================
# Cell 3 - Quick sanity checks (optional)
# ============================================================
print(get_conversion_factor.invoke({'base_currency': 'USD', 'target_currency': 'INR'}))
print(convert.invoke({'amount': 10, 'conversion_factor': 92.5746}))


# ============================================================
# Cell 4 - LLM Setup
# ============================================================
llm = ChatGroq(model='llama-3.3-70b-versatile')


# ============================================================
# Cell 5 - Bind tools
# ============================================================
llm_with_tools = llm.bind_tools([get_conversion_factor, convert])


# ============================================================
# Cell 6 - Initial message
# ============================================================
messages = [HumanMessage('What is the conversion factor between INR and USD, and based on that can you convert 10 inr to usd')]


# ============================================================
# Cell 7 - Agentic loop
# FIX 2: Instead of a single-pass loop (which missed the second
#         tool call in a separate turn), we now loop until the
#         LLM stops requesting tools, then print its final answer.
# ============================================================
tools_map = {
    'get_conversion_factor': get_conversion_factor,
    'convert': convert,
}

conversion_factor = None  # track across turns

while True:
    ai_message = llm_with_tools.invoke(messages)
    messages.append(ai_message)

    # If no tool calls remain, the LLM has produced a final text response
    if not ai_message.tool_calls:
        break

    for tool_call in ai_message.tool_calls:
        tool_name = tool_call['name']

        if tool_name == 'get_conversion_factor':
            result = get_conversion_factor.invoke(tool_call)
            conversion_factor = json.loads(result.content)['conversion_rate']
            messages.append(result)

        elif tool_name == 'convert':
            # Inject conversion_factor if the LLM didn't include it
            if conversion_factor is not None and 'conversion_factor' not in tool_call['args']:
                tool_call['args']['conversion_factor'] = conversion_factor
            result = convert.invoke(tool_call)
            messages.append(result)


# ============================================================
# Cell 8 - Final response
# ============================================================
print("\n=== Final LLM Response ===")
print(ai_message.content)
