import re
from io import BytesIO
from typing import List, Dict

from pypdf import PdfReader

from backend.utils.logger import get_logger

logger = get_logger(__name__)


class DocumentService:
    def extract_pages(self, file_bytes: bytes) -> List[Dict]:
        reader = PdfReader(BytesIO(file_bytes))
        pages = []
        for i, page in enumerate(reader.pages):
            content = page.extract_text() or ""
            content = re.sub(r"\s+", " ", content).strip()
            if content:
                pages.append({"page": i + 1, "text": content})
        logger.info(f"Extracted {len(pages)} pages with text")
        return pages

    def chunk_pages(self, pages: List[Dict], chunk_size: int = 220, overlap: int = 40) -> List[Dict]:
        chunks = []
        for p in pages:
            words = p["text"].split()
            i = 0
            while i < len(words):
                piece = words[i:i + chunk_size]
                if piece:
                    chunks.append({"text": " ".join(piece), "page": p["page"]})
                i += max(chunk_size - overlap, 1)
        logger.info(f"Created {len(chunks)} chunks (size={chunk_size}, overlap={overlap})")
        return chunks