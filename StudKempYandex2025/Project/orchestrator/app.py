import asyncio
from fastapi import FastAPI, Request
import httpx

PROMPT_VALIDATOR_URL = "http://prompt-validator:8000/validate_prompt"
RAG_URL = "http://rag:8000/search"
ANSWER_MODEL_URL = "http://answer-model:8000/generate"
UNIFIED_VALIDATOR_URL = "http://output_validator:8000/validate_output"

app = FastAPI()

@app.post("/process")
async def process(request: Request):
    data = await request.json()
    user_message = data.get("prompt", "")

    async with httpx.AsyncClient(timeout=30) as client:
        # 1. Prompt validation
        val_resp = await client.post(PROMPT_VALIDATOR_URL, json={"prompt": user_message})
        validation = val_resp.json()
        if validation.get("action") == "deny":
            return {"answer": f"⚠️ Ввод отклонён. Причина: {validation.get('reason', 'подозрительный ввод')}"}

        cleaned = validation.get("cleaned", user_message)

        # 2. RAG поиск
        rag_res = await client.post(RAG_URL, json={"query": cleaned})
        context = rag_res.json().get("context", "")

        # 3. Генерация ответа LLM
        ans_resp = await client.post(ANSWER_MODEL_URL, json={"prompt": cleaned, "context": context})
        raw_answer = ans_resp.json().get("answer", "")

        # 4. Unified validation ответа
        val_resp = await client.post(UNIFIED_VALIDATOR_URL, json={"answer": raw_answer})
        answer_val = val_resp.json()

        if answer_val.get("action") == "deny":
            return {"answer": f"⚠️ Ответ модели отклонён. Причина: {answer_val.get('reason')}"}

    return {"answer": raw_answer}

async def process_message(user_message: str) -> str:
    async with httpx.AsyncClient() as client:
        # 1. Prompt validation
        val_resp = await client.post(PROMPT_VALIDATOR_URL, json={"prompt": user_message})
        validation = val_resp.json()
        if validation.get("action") == "deny":
            return f"Ввод отклонён. Причина: {validation.get('reason', 'подозрительный ввод')}"

        cleaned = validation.get("cleaned", user_message)

        # 2. RAG поиск
        rag_res = await client.post(RAG_URL, json={"query": cleaned})
        context = rag_res.json().get("context", "")

        # 3. Генерация ответа LLM
        ans_resp = await client.post(ANSWER_MODEL_URL, json={"prompt": cleaned, "context": context})
        raw_answer = ans_resp.json().get("answer", "")

        # 4. Unified validation ответа
        val_resp = await client.post(UNIFIED_VALIDATOR_URL, json={"answer": raw_answer})
        answer_val = val_resp.json()

        if answer_val.get("action") == "deny":
            return f"Ответ модели отклонён. Причина: {answer_val.get('reason')}"

        return raw_answer


@app.post("/message")
async def message_handler(req: Request):
    data = await req.json()
    user_message = data.get("message", "")
    reply = await process_message(user_message)
    return {"reply": reply}