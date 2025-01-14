import streamlit as st
from model import recipe_assistant

# Set page configuration
st.set_page_config(
    page_title="Recipe Assistant",
    page_icon="🍳",
    layout="wide"
)

# Add title and description
st.title("🍳 Recipe Assistant")
st.markdown("""
Ask me about recipes! You can:
- Search for recipes with specific ingredients
- Ask for quick meal ideas
- Get cooking suggestions for leftover ingredients
- Learn about different cuisines
""")

# Create the input text area
user_query = st.text_area("What would you like to cook today?", height=100)

# Add a search button
if st.button("Search Recipes"):
    if user_query:
        # Show a spinner while processing
        with st.spinner("Searching for recipes..."):
            response = recipe_assistant(user_query)
            st.markdown("### Here's what I found:")
            st.markdown(response)
    else:
        st.warning("Please enter a query first!")

# Add footer
st.markdown("---")
st.markdown("Powered by AI 🤖 • Built with Streamlit") 