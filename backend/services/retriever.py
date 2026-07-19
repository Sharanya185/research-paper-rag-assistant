from typing import List, Dict

from backend.services.embedding_service import EmbeddingService
from backend.services.vector_store_service import VectorStoreService
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class Retriever:
    def __init__(self, embedding_service: EmbeddingService, vector_store: VectorStoreService):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(self, session_id: str, query: str, top_k: int = 4) -> List[Dict]:
        query_embedding = self.embedding_service.embed(query)
        results = self.vector_store.query(session_id, query_embedding, top_k=top_k)

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]

        chunks = []
        for doc, meta, dist in zip(docs, metas, dists):
            similarity = 1 - dist
            chunks.append({"text": doc, "page": meta.get("page"), "score": round(similarity, 4)})

        logger.info(f"Retrieved {len(chunks)} chunks for query: '{query[:60]}...'")
        return chunks