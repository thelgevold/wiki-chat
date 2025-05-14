from fastapi import FastAPI
from app.model import predict, init_llm, query_vector_db_by_question
from app.chat_context import ChatContext

from app.helpers.index_db_helper import IndexDBHelper

app = FastAPI()

index_helper = IndexDBHelper()

init_llm()

index = index_helper.build_index_db()

@app.post('/api/chat')
async def chat(ctx: ChatContext):
    print(ctx)
    
    return predict(ctx)

@app.get('/api/query-vector')
def query_vector(query: str):
    
    resp = query_vector_db_by_question(query)
   
    data = {'response':resp}

    return data
 