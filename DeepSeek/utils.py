from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os

def query_recipes(user_query, model=SentenceTransformer('all-MiniLM-L6-v2')):
    api_key = os.getenv("PINECONE_API_KEY")
    pc = Pinecone(api_key=api_key)
    index = pc.Index("recipe-index")
    print(api_key)
    query_embedding = model.encode(user_query)
    results = index.query(
        vector=query_embedding.tolist(),
        top_k=3,
        include_metadata=True
    )
    metadata_list = [match["metadata"] for match in results.get("matches", [])]
    return metadata_list

def build_context(metadata_list):
    """Build context string from recipe metadata"""
    context = ""
    for idx, recipe in enumerate(metadata_list, 1):
        context += f"\nRecipe {idx}:\n"
        context += f"Title: {recipe.get('recipe_name', 'N/A')}\n"
        context += f"Cuisine: {recipe.get('cuisine', 'N/A')}\n"
        context += f"Prep Time: {recipe.get('prep_time', 'N/A')} minutes\n"
        context += f"Ingredients: {recipe.get('ingredients', 'N/A')}\n"
        context += f"Instructions: {recipe.get('instructions', 'N/A')}\n"
        if recipe.get('url'):
            context += f"Recipe URL: {recipe.get('url')}\n"
    return context