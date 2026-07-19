from typing import List, Dict

import chromadb

from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class VectorStoreService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)

    def _collection(self, session_id: str):
        return self.client.get_or_create_collection(
            name=f"session_{session_id}",
            metadata={"hnsw:space": "cosine"},
        
        )
    def add_chunks(self, session_id: str, chunks: List[Dict], embeddings: List[List[float]]):
        collection = self._collection(session_id)
        ids = [f"{session_id}_{i}" for i in range(len(chunks))]
        documents = [c["text"] for c in chunks]
        metadatas = [{"page": c["page"]} for c in chunks]
        collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
        logger.info(f"Stored {len(chunks)} chunks in collection 'session_{session_id}'")

    def query(self, session_id: str, query_embedding: List[float], top_k: int = 4) -> Dict:
        collection = self._collection(session_id)
        return collection.query(query_embeddings=[query_embedding], n_results=top_k)