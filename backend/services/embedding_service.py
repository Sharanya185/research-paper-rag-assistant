from typing import List

import ollama

from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    def __init__(self, model: str = None):
        self.model = model or settings.EMBED_MODEL

    def embed(self, text: str) -> List[float]:
        resp = ollama.embeddings(model=self.model, prompt=text)
        return resp["embedding"]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        logger.info(f"Embedding {len(texts)} texts with '{self.model}'")
        return [self.embed(t) for t in texts]