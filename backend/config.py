 
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    CHAT_MODEL: str = os.getenv("CHAT_MODEL", "llama3")
    EMBED_MODEL: str = os.getenv("EMBED_MODEL", "nomic-embed-text")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 220))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 40))
    TOP_K: int = int(os.getenv("TOP_K", 4))
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "./chroma_db")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MAX_MEMORY_TURNS: int = int(os.getenv("MAX_MEMORY_TURNS", 6))


settings = Settings()