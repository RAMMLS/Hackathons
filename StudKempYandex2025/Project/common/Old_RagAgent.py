import tempfile

import requests
from langchain_community.document_loaders import PyPDFLoader


def download_and_parse_pdf(url: str):
    response = requests.get(url)
    response.raise_for_status()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    return loader.load()

class RagAgent:
    def __init__(self, url):
        self.url = url

    def request(self, text_request):
        params = {"query": text_request, "k": 3}
        rag_response = requests.get(self.url, params=params)

        if rag_response.status_code != 200:
            return None

        context_text = rag_response.json()["context_text"]
        print(context_text)
        return context_text