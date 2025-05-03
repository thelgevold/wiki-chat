from fastapi import FastAPI

from app.model import predict, init_llm
from app.chat_context import ChatContext

app = FastAPI()

init_llm()

@app.post('/api/chat')
async def chat(ctx: ChatContext):
    print(ctx)
    question = ctx.question
    history = ctx.history

    result = predict(question)

    return result
 