import os
from openai import OpenAI
from modelling import query_recipes, build_context, query_deepseekv3

api_key = os.getenv("OPENAI_API_KEY")

# Initialize the client
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

def recipe_assistant(user_input):
    # Step 1: Retrieve metadata from Pinecone
    results = query_recipes(user_input)  # Implement your Pinecone query logic
    
    if not results:
        return "Sorry, I couldn't find any relevant recipes."

    # Step 2: Build the context string
    context = build_context(results)

    # Step 3: Query DeepSeekV3
    try:
        response = query_deepseekv3(client, user_input, context)
        return response
    except Exception as e:
        return f"Error: {e}"