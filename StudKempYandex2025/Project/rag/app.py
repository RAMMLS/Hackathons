from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from common.CloudVectorDB import CloudVectorDB

rag = CloudVectorDB(save_path="/app/vectorstore_faiss")

app = FastAPI()


@app.on_event("startup")
def startup_event():
    """При старте контейнера пробуем загрузить или построить векторное хранилище"""
    try:
        rag.load_vectorstore()
        print("✅ Локальная векторная БД загружена")
    except Exception:
        print("⚠️ Локальная БД не найдена, загружаем из S3")
        try:
            docs = rag.load_documents_from_s3()
            docs = rag.validate_documents(docs)
            chunks = rag.chunk_documents(docs)
            rag.build_vectorstore(chunks)
            print("✅ Векторная БД построена из S3")
        except Exception as e:
            print(f"❌ Ошибка при загрузке данных: {e}")


@app.get("/search")
def search(query: str = Query(..., description="Поисковый запрос"), k: int = 3):
    """Эндпоинт поиска по FAISS"""
    try:
        context_text = rag.build_context(query, k=k)
        return {"context_text": context_text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
