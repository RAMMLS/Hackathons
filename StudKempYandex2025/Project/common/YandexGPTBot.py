import jwt
import requests
import time
import os
from dotenv import load_dotenv
from common.Logger import logger

load_dotenv()

"""SERVICE_ACCOUNT_ID = os.environ.get("SERVICE_ACCOUNT_ID")
KEY_ID = os.environ.get("KEY_ID")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
if PRIVATE_KEY:
    PRIVATE_KEY = PRIVATE_KEY.replace("\\n", "\n")
FOLDER_ID = os.environ.get("FOLDER_ID")
SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT")"""

SERVICE_ACCOUNT_ID = "aje747jp3bso084emfnb"
KEY_ID = "ajevvq2dlpt956bn2mff"
TELEGRAM_TOKEN = "8264950965:AAHXy1D6cBcr89n6Kg780l_u-b6iGjiHC0g"
PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDPge7CHpiNjN2D\nGi3QgE5QvJuzfO5nvu/MPaM45WD4/a94TFxWmJe6iR0FItRH3z0qu2vbJ1sIQJv/\n78lRR0wNEcGiAalq+VanqMQ5p2vaaWyMvYHLMEHyXupEB4HRJhR0P0SdWDGSqJch\nTiSLOMvo4mNsWWm6c3lUkBTmkFPCC3IlnBY4fDg/UeYFIWEjdB2fAWtU1J3gJ1dU\nqMnq1lJtoerJpk8I5XmFBC939imGApmfWWvOSFyHx4gHq85ArVUw5HXWncBN6PO7\n4fGHqa6waUnIcD7k+1QTWiUwiUnQ60Ql99NqfyR9M+Cbq/weT6cLCG6hfTyh/cUw\nGnoagh9LAgMBAAECggEAB2I8OLQWAZNtnmikELNAFidf8vcTFKX6qm3XDQM8fB+q\nysEM2Bf97ilK2w/uNdB/wLGCmP3Bg32pD2Zc54N99UkYdsdQW/obV0PuF48Zi2AM\n+MUVhUFmV1WBSIJr4CFWwPwvWNn2iZ1uI0VAj6OpvdOwbf6QgI3zV0r5M2sXT+Q/\n6omr0Hof5z3rjndN6IMX/SZWL7MyF76ThgrQl7COdW7nfAW8WU4DCxZ4J3USDEtc\n9MWmZ8TzINF0e0vyzKhdvmWlhTBkaIcWDZVDEbSZdnQYJocWGmWM/cRbE531X+pm\n/7zalQKzXnSfCkv63HZCApDf76lOjyReIkC2Rtc7wQKBgQD6CH/MtG2x/wqlvaCb\n+/Xvcv3WhQwdju88ZcOQHJsYw2qOjvMuuDwBD9f5/GUBcpj9KFQO2BABdZhv7KQq\nSH+DuE/gWw9kHNVwyElTvsbGp68xQNFA+dd/zrcdT9MY7f0C95tKvI7Bmbm13Wad\nyc+v3em/C14P+je5t4m/XLwiCQKBgQDUdaLVy2sibG2V3Oy/57ZUyWYDrrLJw8C/\nh+MuHSUItJrv4y7p+JTLVBLS6TWoJULVGFOdWtjAT5hWYFyY7NqQLf+8QIFzXQri\nmohMOVWa2uOGdUMmJ1X0Zdx2GM3LPyr4fkuX1/PbhDEcXxeS+XtNlxE865yD/RQQ\n5EYF4Lx7swKBgQDpiF61uCBtDCXJwF/u0VtYFzN31jUGtqZE51fNlqpWas9v75y7\nmmCRLVcwqsk8nOjAK5a3dp8cfdWvVHvQ8n4HbXNNvj+V5kiFWs0CZ0IJ8jzz5/KK\nmdDqEw19Vz14H3EeAF8PYyaDNS3765sY7ZIKVV8pjViB29eIoyEJl3gw4QKBgCHZ\nD/UxsELOtXK/vLQiLUk6wNbrWS6N0kJxWr85A3Jsm5aGQi4iXUo7fbg+UT8VmJ0s\nf/28wHV6+NEiDv6KFZQM0AZk3HrNovNRHU/PfpTqNH9yZR1J/Qavx7zE3Nx5ltX6\nAP8S95XMbKqRd8cBmiRVYfirrMbWZgD+7Sz4je7DAoGADW1VH4QPxGtj9eQeYN+N\nvpGg8bqOIESEpAb7eKmi8CSex6l++Va0ldKqDhy5eOI1EKDUf3Vg3Bph1170VIsO\nhqRkbwwTQS0HLEPEROBqmUHa51Q+4T28BdXO46J0+yTUiuiMYg4sZv32APeg8DOY\nbvXEGn6sW56MDR/0ekcNcTU=\n-----END PRIVATE KEY-----\n"
FOLDER_ID = "b1gk4jc9l8kjk8lb9bj9"
SYSTEM_PROMPT = "Ты помощник, который отвечает кратко и понятно."

class YandexGPTBot:
    def __init__(self, system_prompt: str = None):
        self.iam_token = None
        self.token_expires = 0
        self.system_prompt = system_prompt

    def get_iam_token(self):
        """Получение IAM-токена (с кэшированием на 1 час)"""
        if self.iam_token and time.time() < self.token_expires:
            return self.iam_token
        try:
            now = int(time.time())
            payload = {
                'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
                'iss': SERVICE_ACCOUNT_ID,
                'iat': now,
                'exp': now + 3600
            }

            # Проверяем и приводим KEY_ID к строке
            kid = str(KEY_ID) if KEY_ID is not None else None
            if not kid:
                raise ValueError("KEY_ID (private_key_id) не задан или пустой")

            encoded_token = jwt.encode(
                payload,
                PRIVATE_KEY,
                algorithm='PS256',
                headers={'kid': kid}  # теперь kid гарантированно строка
            )

            response = requests.post(
                'https://iam.api.cloud.yandex.net/iam/v1/tokens',
                json={'jwt': encoded_token},
                timeout=10
            )
            if response.status_code != 200:
                raise Exception(f"Ошибка генерации токена: {response.text}")

            token_data = response.json()
            self.iam_token = token_data['iamToken']
            self.token_expires = now + 3500
            logger.info("IAM token generated successfully")
            return self.iam_token

        except Exception as e:
            logger.error(f"Error generating IAM token: {str(e)}")
            raise

    def ask_gpt(self, messages: list[dict]):
        """Запрос к Yandex GPT API"""
        try:
            iam_token = self.get_iam_token()

            # если есть системный промпт, добавляем его в начало
            if self.system_prompt:
                messages = [{"role": "system", "text": self.system_prompt}] + messages

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {iam_token}',
                'x-folder-id': FOLDER_ID
            }
            data = {
                "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.6,
                    "maxTokens": 2000
                },
                "messages": messages
            }

            response = requests.post(
                'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code != 200:
                logger.error(f"Yandex GPT API error: {response.text}")
                raise Exception(f"Ошибка API: {response.status_code}")

            return response.json()['result']['alternatives'][0]['message']['text']

        except Exception as e:
            logger.error(f"Error in ask_gpt: {str(e)}")
            raise
