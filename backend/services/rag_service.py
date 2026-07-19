import uuid
from typing import Dict

from backend.services.document_service import DocumentService
from backend.services.embedding_service import EmbeddingService
from backend.services.vector_store_service import VectorStoreService
from backend.services.retriever import Retriever
from backend.services.prompt_manager import PromptManager
from backend.services.memory_manager import MemoryManager
from backend.services.llm_service import LLMService
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class RAGService:
    def __init__(self):
        self.document_service = DocumentService()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreService()
        self.retriever = Retriever(self.embedding_service, self.vector_store)
        self.prompt_manager = PromptManager()
        self.memory_manager = MemoryManager()
        self.llm_service = LLMService()

        self._chunks_cache: Dict[str, list] = {}

    def ingest_document(self, file_bytes: bytes, filename: str) -> dict:
        session_id = str(uuid.uuid4())[:8]

        pages = self.document_service.extract_pages(file_bytes)
        if not pages:
            raise ValueError("No extractable text found in this PDF (it may be scanned/image-based).")

        chunks = self.document_service.chunk_pages(
            pages, chunk_size=settings.CHUNK_SIZE, overlap=settings.CHUNK_OVERLAP
        )
        embeddings = self.embedding_service.embed_batch([c["text"] for c in chunks])
        self.vector_store.add_chunks(session_id, chunks, embeddings)
        self._chunks_cache[session_id] = chunks

        logger.info(f"Ingested '{filename}' as session '{session_id}' ({len(pages)} pages, {len(chunks)} chunks)")
        return {
            "session_id": session_id,
            "filename": filename,
            "num_pages": len(pages),
            "num_chunks": len(chunks),
        }

    def ask(self, session_id: str, question: str, top_k: int = None) -> dict:
        top_k = top_k or settings.TOP_K
        chunks = self.retriever.retrieve(session_id, question, top_k=top_k)
        history = self.memory_manager.get_history_text(session_id)
        prompt = self.prompt_manager.build_rag_prompt(question, chunks, history=history)
        answer = self.llm_service.generate(prompt)
        self.memory_manager.add_turn(session_id, question, answer)

        return {
            "answer": answer,
            "sources": [
                {"page": c["page"], "text": c["text"][:300], "score": c["score"]} for c in chunks
            ],
        }

    def summarize(self, session_id: str) -> str:
        chunks = self._chunks_cache.get(session_id)
        if not chunks:
            raise ValueError("Session not found. Re-upload the document.")

        n = len(chunks)
        group_size = max(1, n // 6)
        groups = [chunks[i:i + group_size] for i in range(0, n, group_size)]

        partial_summaries = []
        for group in groups:
            text = "\n".join(c["text"] for c in group)
            prompt = self.prompt_manager.build_section_summary_prompt(text)
            partial_summaries.append(self.llm_service.generate(prompt))

        combined = "\n".join(partial_summaries)
        final_prompt = self.prompt_manager.build_final_summary_prompt(combined)
        return self.llm_service.generate(final_prompt)

    def explain_concept(self, session_id: str, concept: str, top_k: int = None) -> dict:
        query = self.prompt_manager.build_concept_prompt(concept)
        return self.ask(session_id, query, top_k=top_k)


rag_service = RAGService()