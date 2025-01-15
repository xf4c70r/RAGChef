
# RAG Chef

An intelligent recipe assistant powered by DeepSeek AI and Pinecone vector database. This application helps users find recipes based on ingredients, cuisine preferences, or general cooking queries.

Dataset used: https://www.kaggle.com/datasets/sooryaprakash12/cleaned-indian-recipes-dataset?resource=download

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PINECONE_API_KEY`

`DEEPSEEK_API_KEY`

`HF_TOKEN`

##  Steps For Adding 'api_key' To Your Environment Variables

Windows: 

1. Open the Start Menu.

2. Search for “Environment Variables” and click on “Edit the system environment variables.”

3. Click the “Environment Variables” button.

4. Under “User variables,” click “New” and enter the variable name and value.

macOS:

1. Open your Terminal app. You can find it in Applications › Utilities › Terminal

2. Type nano ~/.shre if you're using Zsh (default on newer macOS), or nano ~/. bash profile for Bash.

3. In the file that opens, add export 'API_KEY_NAME'='api_key' at the end.

4. Save changes by pressing Ctrl + 0, then Enter. Exit by pressing ctrl + X

5. Type source ~/.zshre Or source ~/. bash profile to reload the profile.

6.  Verify the setup by typing echo $API_KEY_NAME in the terminal. It should display your API key.
## Run Locally

Clone the repo

```
git clone https://github.com/xf4c70r/RAGChef.git
```

Install dependencies 
```
cd RAGChef
```
```
cd directory
```

Install dependencies 
```
pip install -r requirements.txt
```

Setup the VectorDB (Just need to do it once)
```
python vectorDB.py
```

Run the app
```
streamlit run app.py
```