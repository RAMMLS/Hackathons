from fastapi import FastAPI, Request
from common.YandexGPTBot import YandexGPTBot
SYSTEM_PROMPT = "Ты помощник, который отвечает на вопросы пользователей. Используй информацию из контекста, только если она содержит полезные данные, в противном случае игнорируй."

bot_answer = YandexGPTBot(system_prompt=SYSTEM_PROMPT)
app = FastAPI()

@app.post("/generate")
async def generate(req: Request):
    data = await req.json()
    prompt = data.get("prompt", "")
    context = data.get("context", "")

    messages = [
        {"role": "system", "text": bot_answer.system_prompt},
        {"role": "user", "text": f"Вопрос: {prompt}" + (f"\nКонтекст: {context}" if context is not None else "")}
    ]
    raw_answer = bot_answer.ask_gpt(messages)
    return {"answer": raw_answer}