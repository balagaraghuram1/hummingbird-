"""Vector database service for medical knowledge retrieval.

Provides semantic search capabilities over medical knowledge
using ChromaDB and OpenAI embeddings.
"""

from __future__ import annotations

import logging

from src.config.settings import settings

logger = logging.getLogger(__name__)


class VectorService:
    """Vector database service for medical knowledge retrieval.

    Uses ChromaDB with OpenAI embeddings for semantic search
    over medical documents and knowledge base.
    """

    def __init__(self) -> None:
        self._embeddings = None
        self._store = None
        self._available = False

    def _ensure_initialized(self) -> None:
        """Lazy-initialize the vector store."""
        if self._store is not None or self._embeddings is not None:
            return

        if not settings.openai_api_key:
            logger.warning("OpenAI API key not configured, vector service unavailable")
            return

        try:
            from langchain_openai import OpenAIEmbeddings
            from langchain_community.vectorstores import Chroma

            self._embeddings = OpenAIEmbeddings(api_key=settings.openai_api_key)
            self._store = Chroma(
                embedding_function=self._embeddings,
                persist_directory=settings.chroma_persist_directory,
            )
            self._available = True
            logger.info("Vector service initialized successfully")
        except ImportError as e:
            logger.warning("Vector dependencies not available: %s", e)
        except Exception as e:
            logger.error("Failed to initialize vector service: %s", e)

    def search(self, query: str, k: int = 4) -> list[str]:
        """Search for similar documents in the knowledge base.

        Args:
            query: Search query string.
            k: Number of results to return.

        Returns:
            List of document content strings.
        """
        self._ensure_initialized()
        if not self._available or self._store is None:
            return []

        try:
            docs = self._store.similarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            logger.error("Vector search failed: %s", e)
            return []

    def add_documents(self, texts: list[str], metadatas: list[dict] | None = None) -> int:
        """Add documents to the vector store.

        Args:
            texts: List of document texts to add.
            metadatas: Optional list of metadata dicts.

        Returns:
            Number of documents added.
        """
        self._ensure_initialized()
        if not self._available or self._store is None:
            return 0

        try:
            ids = self._store.add_texts(texts, metadatas=metadatas)
            return len(ids)
        except Exception as e:
            logger.error("Failed to add documents: %s", e)
            return 0

    @property
    def is_available(self) -> bool:
        """Check if the vector service is available."""
        self._ensure_initialized()
        return self._available


vector_service = VectorService()
