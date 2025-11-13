import requests

class RagAgent:
    def __init__(self, url: str):
        self.url = url.rstrip("/")

    def request(self, text_request: str):
        params = {"query": text_request, "k": 3}
        try:
            rag_response = requests.post(f"{self.url}/search", json=params, timeout=30)
            rag_response.raise_for_status()
            data = rag_response.json()
            return data.get("context")
        except Exception as e:
            print(f"Ошибка запроса к RAG: {e}")
            return None
