from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.models.schemas import (
    AskRequest, AskResponse, SummaryResponse, ConceptRequest, UploadResponse, Source,
)
from backend.services.rag_service import rag_service
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")
    try:
        file_bytes = await file.read()
        result = rag_service.ingest_document(file_bytes, file.filename)
        return UploadResponse(**result)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        logger.exception("Upload failed")
        raise HTTPException(500, f"Upload failed: {e}")


@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    try:
        result = rag_service.ask(req.session_id, req.question, top_k=req.top_k)
        return AskResponse(answer=result["answer"], sources=[Source(**s) for s in result["sources"]])
    except Exception as e:
        logger.exception("Ask failed")
        raise HTTPException(500, str(e))


@router.post("/summarize/{session_id}", response_model=SummaryResponse)
def summarize(session_id: str):
    try:
        summary = rag_service.summarize(session_id)
        return SummaryResponse(summary=summary)
    except ValueError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        logger.exception("Summarize failed")
        raise HTTPException(500, str(e))


@router.post("/explain", response_model=AskResponse)
def explain(req: ConceptRequest):
    try:
        result = rag_service.explain_concept(req.session_id, req.concept)
        return AskResponse(answer=result["answer"], sources=[Source(**s) for s in result["sources"]])
    except Exception as e:
        logger.exception("Explain failed")
        raise HTTPException(500, str(e))