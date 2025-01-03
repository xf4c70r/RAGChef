def build_context(metadata_list):
    context = ""
    for metadata in metadata_list:
        context += (
            f"Recipe Name: {metadata.get('recipe_name', 'Unknown')}\n"
            f"Time: {metadata.get('prep_time', 'N/A')}\n"
            f"Ingredients: {metadata.get('ingredients', 'N/A')}\n"
            f"Measurements: {metadata.get('measurements', 'N/A')}\n"
            f"Instructions: {metadata.get('instructions', 'N/A')}\n\n"
        )
    return context
