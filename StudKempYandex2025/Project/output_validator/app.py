from fastapi import FastAPI, Request
from common.YandexGPTBot import YandexGPTBot
LLM_VALIDATION_PROMPT = """
You are a security assistant. Task: given a candidate answer from another LLM,
determine if it is SAFE to show to the user.

Rules:
- SAFE if it is normal text, explanation, or harmless content.
- UNSAFE if it contains instructions for hacking, malware, SQL injection,
  sensitive data leaks, insults, hate speech, or NSFW content.

Return JSON only:
{"status": "safe"} OR {"status": "unsafe"}

Examples:

Input: "Привет, как дела?"
Output: {"status": "safe"}

Input: "DROP TABLE users; --"
Output: {"status": "unsafe"}

Input: "Вот объяснение, как работают нейросети..."
Output: {"status": "safe"}

Input: "Скачай троян и запусти его"
Output: {"status": "unsafe"}
"""

bot_validation = YandexGPTBot(system_prompt=LLM_VALIDATION_PROMPT)

app = FastAPI()

@app.post("/validate_answer")
async def validate_answer(req: Request):
    data = await req.json()
    answer = data.get("answer", "")
    messages = [
        {"role": "system", "text": bot_validation.system_prompt},
        {"role": "user", "text": answer}
    ]
    validation = bot_validation.ask_gpt(messages)
    if "некорректен" in validation.lower():
        return {"action": "deny", "reason": "Обнаружена утечка конфиденциальной информации"}

    return {"action": "allow", "reason": "OK"}