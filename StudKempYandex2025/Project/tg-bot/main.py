import logging
import os
import httpx
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ORCHESTRATOR_URL = "http://orchestrator:8000/process"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramBotHandler:
    def __init__(self, token: str, orchestrator_url: str):
        self.token = token
        self.orchestrator_url = orchestrator_url
        self.app = Application.builder().token(self.token).build()

        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._on_message)
        )

    async def _on_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_message = update.message.text
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(
                    self.orchestrator_url,
                    json={"prompt": user_message},
                )
            if resp.status_code == 200:
                reply = resp.json().get("answer", "❌ Оркестратор вернул пустой ответ")
            else:
                reply = f"⚠️ Ошибка оркестратора ({resp.status_code})"
        except Exception as e:
            logger.exception("Ошибка связи с оркестратором")
            reply = "❌ Не удалось связаться с оркестратором"

        await update.message.reply_text(reply)

    def run(self):
        logger.info("🚀 Telegram бот запущен")
        self.app.run_polling()


if __name__ == "__main__":
    bot = TelegramBotHandler(TELEGRAM_TOKEN, ORCHESTRATOR_URL)
    bot.run()