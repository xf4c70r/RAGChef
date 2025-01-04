import os
from openai import OpenAI
from utils import query_recipes, build_context, query_deepseekv3

# Initialize the client
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def recipe_assistant(user_input):
    results = query_recipes(user_input)    
    if not results:
        return "Sorry, I couldn't find any relevant recipes."
    context = build_context(results)
    try:
        response = query_deepseekv3(client, user_input, context)
        return response
    except Exception as e:
        return f"Error: {e}"