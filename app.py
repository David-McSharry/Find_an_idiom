import pinecone
import openai
import os
from dotenv import load_dotenv
from tqdm.auto import tqdm
import json
import pandas as pd
from flask import Flask, request, render_template

load_dotenv()

# OpenAI init
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
MODEL = "text-embedding-ada-002"

# pinecone init
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment="us-west1-gcp"
)
vec_dim = 1536 # the dim of ada-002
index_name = "test"

index = pinecone.Index(index_name)

app = Flask(__name__)

@app.route('/')
def search_form():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    xq = openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']
    res = index.query([xq], top_k=1, include_metadata=True)['matches'][0]['metadata']
    return render_template('result.html', result=res['idiom'], description=res['description'])


