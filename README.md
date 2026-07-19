# AI Research Paper Assistant — Layered RAG Architecture

An AI-powered research paper assistant that lets you upload a PDF and ask questions about it, get a summary, or have concepts explained — all grounded in the actual document content using Retrieval-Augmented Generation (RAG).

Originally built as a single-file Streamlit app, refactored into a properly layered backend/frontend architecture:

Frontend (Streamlit) → FastAPI Backend → RAG Service → Document Service
→ Embedding Service → Vector Store Service (ChromaDB) → Retriever
→ Prompt Manager → Memory Manager → LLM Service → Logging → Configuration → Response

## Tech Stack
- **Backend:** FastAPI, Python
- **LLM & Embeddings:** Ollama (local), llama3, nomic-embed-text
- **Vector Store:** ChromaDB (persistent, disk-backed)
- **Frontend:** Streamlit
- **PDF Processing:** pypdf

## Project Structure
backend/
├── main.py                      # FastAPI app entrypoint
├── config.py                    # Centralized configuration
├── api/routes.py                # HTTP endpoints
├── services/
│   ├── rag_service.py           # Orchestrator
│   ├── document_service.py      # PDF → chunks
│   ├── embedding_service.py     # text → vectors
│   ├── vector_store_service.py  # ChromaDB
│   ├── retriever.py             # query → relevant chunks
│   ├── prompt_manager.py        # prompt templates
│   ├── memory_manager.py        # conversation history
│   └── llm_service.py           # Ollama chat
├── models/schemas.py            # Pydantic request/response models
└── utils/logger.py              # Centralized logging
frontend/
└── app.py                       # Streamlit UI

## Setup

1. Create a virtual environment and activate it
2. `pip install -r backend/requirements.txt`
3. `pip install -r frontend/requirements.txt`
4. Pull Ollama models: `ollama pull llama3` and `ollama pull nomic-embed-text`
5. Run the backend: `uvicorn backend.main:app --reload`
6. In a second terminal, run the frontend: `streamlit run frontend/app.py`

## Features
- Upload a PDF and ask natural-language questions about it, with page-cited answers
- Full-document summarization (map-reduce over all chunks, not just the start)
- Concept explanation grounded in the paper's actual content
- Session-based conversation memory for follow-up questions
- Interactive API docs at `/docs` via FastAPI's auto-generated OpenAPI UI