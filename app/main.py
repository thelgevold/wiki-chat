from fastapi import FastAPI
from llama_index.core import Settings
from app.model import predict, init_llm, query_vector_db
from app.chat_context import ChatContext

from app.helpers.index_db_helper import IndexDBHelper

app = FastAPI()

index_helper = IndexDBHelper()

init_llm()

index = index_helper.build_index_db()

#Settings.query_engine = init_query_engine(index)

@app.post('/api/chat')
async def chat(ctx: ChatContext):
    print(ctx)
    
    result = predict(ctx)

    print(f"HERE IS THE RESULT{result}")

    return result

@app.get('/api/query-vector')
def query_vector(query: str):
    
    resp = query_vector_db(query)
   
    data = {'response':resp}

    return data
 