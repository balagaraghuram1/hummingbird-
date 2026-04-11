from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from src.config.settings import settings


class VectorService:
    def __init__(self) -> None:
        self._embeddings = OpenAIEmbeddings(api_key=settings.openai_api_key)
        self._store = Chroma(
            embedding_function=self._embeddings,
            persist_directory=settings.chroma_persist_directory,
        )

    def search(self, query: str, k: int = 4) -> list[str]:
        docs = self._store.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]


vector_service = VectorService()

