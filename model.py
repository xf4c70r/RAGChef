import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig
import torch
from utils import query_recipes
from huggingface_hub import login

HF_TOKEN = os.getenv('HF_TOKEN')

# Login with your Hugging Face token
login(HF_TOKEN)

# Configure quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

# Load the model with auto device map and quantization
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B", token="HF_TOKEN")
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B",
    quantization_config=bnb_config,
    torch_dtype=torch.float16,
    device_map="cuda:0",
    low_cpu_mem_usage=True
)

def recipe_assistant(user_query):
    retrieved_recipes = query_recipes(user_query)
    context = "Relevant Recipes:\n"
    for recipe in retrieved_recipes:
        context += (
            f"Recipe Name: {recipe['recipe_name']}\n"
            f"Time: {recipe['prep_time']}\n"
            f"Ingredients: {recipe['ingredients']}\n"
            f"Measurements: {recipe['measurements']}\n"
            f"Instructions: {recipe['instructions']}\n\n"
        )
    prompt = context + f"User Query: {user_query}"

    # Move inputs to the same device as the model
    device = next(model.parameters()).device
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    max_input_length = tokenizer.model_max_length - 200
    if len(inputs['input_ids'][0]) > max_input_length:
        truncated_prompt = tokenizer.decode(inputs['input_ids'][0][:max_input_length], skip_special_tokens=True)
        inputs = tokenizer(truncated_prompt, return_tensors="pt").to(device)

    # Generate output
    outputs = model.generate(**inputs, max_new_tokens=300)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response