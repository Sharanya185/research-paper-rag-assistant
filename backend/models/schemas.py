from typing import List, Optional
from pydantic import BaseModel


class UploadResponse(BaseModel):
    session_id: str
    filename: str
    num_pages: int
    num_chunks: int


class AskRequest(BaseModel):
    session_id: str
    question: str
    top_k: Optional[int] = None


class Source(BaseModel):
    page: int
    text: str
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: List[Source]


class SummaryResponse(BaseModel):
    summary: str


class ConceptRequest(BaseModel):
    session_id: str
    concept: str