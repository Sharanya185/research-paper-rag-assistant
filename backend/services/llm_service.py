import ollama

from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class LLMService:
    def __init__(self, model: str = None):
        self.model = model or settings.CHAT_MODEL

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        logger.info(f"Calling LLM '{self.model}' (prompt length={len(prompt)} chars)")
        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": temperature},
        )
        return response["message"]["content"]