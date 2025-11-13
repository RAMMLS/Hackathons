from fastapi import FastAPI, Request
from common.Old_RagAgent import RagAgent

rag_agent = RagAgent("https://2d29e8b05d4e.ngrok-free.app/search")

app = FastAPI()

@app.post("/search")
async def search(req: Request):
    data = await req.json()
    query = data.get("query", "")
    rag_responce = rag_agent.request(query)
    context = f"Контекст для запроса: {rag_responce}"
    return {"context": context}