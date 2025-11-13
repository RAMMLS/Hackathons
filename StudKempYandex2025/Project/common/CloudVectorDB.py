import os, tempfile, csv, io
import faiss
import numpy as np
import boto3
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
from langchain_huggingface import HuggingFaceEmbeddings

class CloudVectorDB:
    def __init__(self, save_path="/app/vectorstore_faiss"):
        self.save_path = save_path
        self.embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")
        self.vectorstore = None
        self.s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("S3_ENDPOINT"),
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
            region_name="ru-central1",
        )
    def load_documents_from_s3(self):
        try:
            objects = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=self.prefix)
        except Exception as e:
            print(f"Ошибка подключения к S3: {e}")
            return []

        docs = []
        for obj in objects.get("Contents", []):
            key = obj["Key"]
            ext = os.path.splitext(key)[1].lower()

            try:
                response = self.s3.get_object(Bucket=self.bucket, Key=key)
                body = response["Body"].read()
            except Exception as e:
                print(f"Ошибка скачивания {key}: {e}")
                continue

            if ext == ".txt":
                text = body.decode("utf-8", errors="ignore")
                docs.append(Document(page_content=text, metadata={"source": key}))

            elif ext == ".pdf":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(body)
                    tmp_path = tmp.name
                loader = PyPDFLoader(tmp_path)
                docs.extend(loader.load())
                os.remove(tmp_path)

            elif ext == ".docx":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                    tmp.write(body)
                    tmp_path = tmp.name
                loader = UnstructuredWordDocumentLoader(tmp_path)
                docs.extend(loader.load())
                os.remove(tmp_path)

            elif ext == ".csv":
                try:
                    text_stream = io.StringIO(body.decode("utf-8", errors="ignore"))
                    reader = csv.reader(text_stream)
                    headers = next(reader, None)
                    for row in reader:
                        row_text = ", ".join(f"{h}: {v}" for h, v in zip(headers, row)) if headers else ", ".join(row)
                        docs.append(Document(page_content=row_text, metadata={"source": key}))
                except Exception as e:
                    print(f"Ошибка обработки CSV {key}: {e}")

            else:
                print(f"Формат не поддержан: {key}")

        return docs

    def validate_documents(self, docs):
        return [doc for doc in docs if doc.page_content and doc.page_content.strip()]

    def chunk_documents(self, docs, chunk_size=1000, chunk_overlap=200):
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return splitter.split_documents(docs)

    def build_vectorstore(self, chunks):
        vectors = self.embeddings.embed_documents([d.page_content for d in chunks])
        vectors = np.array(vectors, dtype="float32")
        faiss.normalize_L2(vectors)

        dim = vectors.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(vectors)

        index_to_docstore_id = {i: str(i) for i in range(len(chunks))}
        docstore = InMemoryDocstore({str(i): doc for i, doc in enumerate(chunks)})

        self.vectorstore = FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=docstore,
            index_to_docstore_id=index_to_docstore_id,
        )
        self.vectorstore.save_local(self.save_path)

    def load_vectorstore(self):
        self.vectorstore = FAISS.load_local(
            self.save_path, self.embeddings, allow_dangerous_deserialization=True
        )

    def search(self, query, k=5, distance_threshold=0.7):
        if self.vectorstore is None:
            self.load_vectorstore()
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        return [
            {"text": doc.page_content, "source": doc.metadata.get("source", ""), "score": score}
            for doc, score in results if score > distance_threshold
        ]

    def build_context(self, query, k=5, distance_threshold=0.8, max_chars=1000):
        results = self.search(query, k=k, distance_threshold=distance_threshold)
        return "\n\n".join(r["text"][:max_chars] for r in results if r["text"].strip())

