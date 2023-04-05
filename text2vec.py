import pinecone
import openai
import os
from tqdm.auto import tqdm
import json
import pandas as pd

# --------------------------------------------
# misc
idiom_file = "test_no_empties.json"

# --------------------------------------------
# OpenAI init
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
MODEL = "text-embedding-ada-002"

# --------------------------------------------
# pinecone init
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment="us-west1-gcp"
)
vec_dim = 1536 # the dim of ada-002
index_name = "test"

# --------------------------------------------

if index_name not in pinecone.list_indexes():
    print('creating index')
    pinecone.create_index(index_name, dimension=vec_dim)
# connect to index
index = pinecone.Index(index_name)


id = 0
# Open the file in streaming mode
with open(idiom_file) as f:
    description_block = []
    meta_block = []
    ids_block = []

    for line in f:
        j_content = json.loads(line)
        description = j_content["description"]
        meta = line
        description_block.append(description)
        meta_block.append(j_content)
        ids_block.append(str(id))
        id += 1

        if id % 32 == 0:
            res = openai.Embedding.create(input=description_block, engine=MODEL)
            embedded_description_block = [record['embedding'] for record in res['data']]
            to_upsert = zip(ids_block, embedded_description_block, meta_block)
            index.upsert(to_upsert)
            description_block = []
            meta_block = []
            ids_block = []

        # upload the remaining ones
        if len(description_block) > 0:
            res = openai.Embedding.create(input=description_block, engine=MODEL)
            embedded_description_block = [record['embedding'] for record in res['data']]
            to_upsert = zip(ids_block, embedded_description_block, meta_block)
            index.upsert(to_upsert)
            description_block = []
            meta_block = []
            ids_block = []
        

# query the index
query = "Give me an idiom to use to describe my homosexual friend"
xq = openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']
res = index.query([xq], top_k=1, include_metadata=True)

print(res['matches'][0]['metadata']['idiom'] + '\n')
print(res['matches'][0]['metadata']['description'])



# %%
