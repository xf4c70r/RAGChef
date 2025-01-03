import os
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

def query_recipes(user_query, model=SentenceTransformer('all-MiniLM-L6-v2')):
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index("recipe-index")

    query_embedding = model.encode(user_query)
    results = index.query(
        vector=query_embedding.tolist(),
        top_k=3,
        include_metadata=True
    )
    metadata_list = [match["metadata"] for match in results.get("matches", [])]
    return metadata_list


def query_deepseekv3(client, user_input, context):
    messages = [
        {"role": "system", "content": "You are a helpful recipe assistant..."},
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": f"Here are the details I found:\n{context}"}
    ]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content


def build_context(metadata_list):
    """Build context string from recipe metadata"""
    context = ""
    for idx, recipe in enumerate(metadata_list, 1):
        context += f"\nRecipe {idx}:\n"
        context += f"Title: {recipe.get('title', 'N/A')}\n"
        context += f"Ingredients: {recipe.get('ingredients', 'N/A')}\n"
        context += f"Instructions: {recipe.get('instructions', 'N/A')}\n"
    return context
