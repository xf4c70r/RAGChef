import os
import pandas as pd
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

df = pd.read_csv("Indian_Food_Dataset.csv")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "recipe-index"
if index_name not in pc.list_indexes():
    pc.create_index(index_name, dimension=384, spec=ServerlessSpec(
        cloud='aws',
        region='us-east-1'
    ))
index = pc.Index(index_name)

model = SentenceTransformer('all-MiniLM-L6-v2')
for i, row in df.iterrows():
    combined_text = f"Ingredients: {row['Cleaned-Ingredients']}\nInstructions: {row['TranslatedInstructions']}"
    embedding = model.encode(combined_text)
    metadata = {
        "recipe_name": row['TranslatedRecipeName'],
        "ingredients": row['Cleaned-Ingredients'],
        "measurements": row['TranslatedIngredients'],
        "prep_time": row['TotalTimeInMins'],
        "instructions": row['TranslatedInstructions'],
        "cuisine": row['Cuisine'],
        "url": row['URL'],
        "final_look": row['image-url']
    }
    index.upsert([(str(i), embedding, metadata)])
