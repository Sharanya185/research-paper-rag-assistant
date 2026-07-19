from collections import defaultdict
from typing import List, Dict

from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class MemoryManager:
    def __init__(self):
        self._store: Dict[str, List[Dict]] = defaultdict(list)

    def add_turn(self, session_id: str, question: str, answer: str):
        self._store[session_id].append({"question": question, "answer": answer})
        self._store[session_id] = self._store[session_id][-settings.MAX_MEMORY_TURNS:]

    def get_history_text(self, session_id: str) -> str:
        turns = self._store.get(session_id, [])
        return "\n".join(f"Q: {t['question']}\nA: {t['answer']}" for t in turns)

    def clear(self, session_id: str):
        self._store.pop(session_id, None)
        logger.info(f"Cleared memory for session {session_id}")