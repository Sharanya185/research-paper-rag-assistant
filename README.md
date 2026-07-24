# 📚 AI Research Paper Assistant

### 🤖 Retrieval-Augmented Generation (RAG) | LLM | FastAPI | ChromaDB

<p align="center">
<img src="https://img.shields.io/badge/AI-RAG%20Assistant-blue?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Backend-FastAPI-green?style=for-the-badge"/>
<img src="https://img.shields.io/badge/LLM-Ollama-orange?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Vector%20DB-ChromaDB-purple?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge"/>
</p>

---

# 🌟 Overview

**AI Research Paper Assistant** is an intelligent document-based question-answering system that allows users to interact with research papers using natural language.

Upload a research paper PDF and the assistant can:

📄 Summarize the complete paper
🔍 Answer questions from the document
💡 Explain complex concepts
🧠 Maintain conversation context

Unlike traditional chatbots, this system uses **Retrieval-Augmented Generation (RAG)** to provide answers grounded only in the uploaded document content.

---

# ✨ Key Features

| Feature                  | Description                                     |
| ------------------------ | ----------------------------------------------- |
| 📤 PDF Upload            | Upload research papers directly                 |
| 🔎 Smart Q&A             | Ask questions in natural language               |
| 📑 Context-Based Answers | Responses generated from document content       |
| 📝 Paper Summarization   | Full-document summary using map-reduce approach |
| 💡 Concept Explanation   | Simplifies complex research ideas               |
| 🧠 Memory Support        | Maintains previous conversation context         |
| 📍 Page References       | Provides document-based citations               |

---

# 🧠 System Architecture

```
                User
                 |
                 ↓
        🖥️ Streamlit Frontend
                 |
                 ↓
          ⚡ FastAPI Backend
                 |
                 ↓
            🔥 RAG Service
                 |
        ┌────────┼────────┐
        ↓        ↓        ↓
 Document   Embedding   Retriever
 Service    Service     Service
        |        |        |
        ↓        ↓        ↓
     PDF → Chunks → Vectors
                 |
                 ↓
             ChromaDB
                 |
                 ↓
          Prompt Manager
                 |
                 ↓
          Ollama LLM
        (Llama3 Model)
                 |
                 ↓
          Final Response
```

---

# 🏗️ Architecture Design

Originally developed as a single-file Streamlit application, the project was redesigned into a scalable layered architecture:

```
Frontend
   ↓
FastAPI API Layer
   ↓
Service Layer
   ↓
RAG Pipeline
   ↓
Vector Database
   ↓
LLM Response Generation
```

This improves:

✅ Maintainability
✅ Scalability
✅ Code organization
✅ Future deployment readiness

---

# 🛠️ Tech Stack

## Backend

🐍 Python
⚡ FastAPI
📦 Pydantic

## AI / ML

🦙 Ollama
🤖 Llama3
🔢 Nomic Embed Text

## Retrieval System

📚 Retrieval-Augmented Generation (RAG)
🗄️ ChromaDB Vector Database
🔎 Semantic Search

## Frontend

🎨 Streamlit

## Document Processing

📄 PyPDF

---

# 📂 Project Structure

```
research-paper-rag-assistant/

│
├── backend/
│   │
│   ├── main.py                 🚀 FastAPI entry point
│   ├── config.py               ⚙️ Configuration
│   │
│   ├── api/
│   │   └── routes.py            🌐 API endpoints
│   │
│   ├── services/
│   │   ├── rag_service.py       🧠 RAG pipeline
│   │   ├── document_service.py  📄 PDF processing
│   │   ├── embedding_service.py 🔢 Embeddings
│   │   ├── vector_store_service.py
│   │   ├── retriever.py         🔍 Search engine
│   │   ├── prompt_manager.py
│   │   ├── memory_manager.py
│   │   └── llm_service.py       🤖 LLM interaction
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   └── utils/
│       └── logger.py
│
├── frontend/
│   └── app.py                   🎨 Streamlit UI
│
└── README.md
```

---

# ⚙️ How It Works

### 1️⃣ Document Processing

📄 User uploads a PDF
⬇️
Text is extracted and divided into meaningful chunks

### 2️⃣ Embedding Generation

Chunks are converted into numerical vectors using:

🔢 Nomic Embeddings

### 3️⃣ Vector Storage

Vectors are stored in:

🗄️ ChromaDB

### 4️⃣ Retrieval

User query is matched with relevant document sections.

### 5️⃣ Response Generation

Retrieved context is passed to:

🦙 Llama3 LLM

to generate accurate answers.

---

# 🚀 Setup Instructions

### Clone Repository

```bash
git clone <repository-url>
cd research-paper-rag-assistant
```

### Install Dependencies

```bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### Download Ollama Models

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

### Run Backend

```bash
uvicorn backend.main:app --reload
```

### Run Frontend

Open another terminal:

```bash
streamlit run frontend/app.py
```

---

# 📊 Project Highlights

🚀 Built a complete end-to-end RAG pipeline
🧠 Integrated local LLM inference using Ollama
🔍 Implemented semantic document retrieval
📚 Created PDF-based knowledge assistant
🏗️ Designed modular backend architecture
💬 Added conversational memory management

---

# 🔮 Future Enhancements

🌐 Deploy using Docker & Cloud Services
🎤 Add voice-based interaction
📑 Support multiple research papers simultaneously
🔗 Add citation graph generation
📊 Add paper comparison feature
⚡ Improve retrieval using advanced reranking models

---

# 👩‍💻 Author

## Sharanya Rai K

🎓 Artificial Intelligence & Machine Learning Engineering Student

💡 Interested in:

* Artificial Intelligence
* Large Language Models
* Deep Learning
* Generative AI
* Computer Vision

---

⭐ If you find this project interesting, consider starring the repository!
