📚 AI Research Paper Assistant

<p align="center">

<h3 align="center">

🤖 Retrieval-Augmented Generation (RAG) | FastAPI | Streamlit |Ollama | ChromaDB

</h3>

</p>

<p align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>{=html}<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>{=html}<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>{=html}<img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge"/>{=html}<img src="https://img.shields.io/badge/ChromaDB-6F42C1?style=for-the-badge"/>{=html}

</p>

Default Model: llama3.2:3b

🌟 Overview

AI Research Paper Assistant is a Retrieval-Augmented Generation (RAG)application that lets users upload research papers, generate summaries,ask questions, and understand complex concepts using a local LargeLanguage Model powered by Ollama.

✨ Features

📄 Upload research papers (PDF)

📝 AI-generated summaries

💬 Question answering from document context

💡 Explain difficult concepts

🧠 Conversation memory

🔍 Semantic retrieval with embeddings

💾 ChromaDB vector storage

⚡ Local inference using Ollama

🏗️ Architecture

User
 │
 ▼
Streamlit Frontend
 │
 ▼
FastAPI Backend
 │
 ▼
PDF Processing
 │
 ▼
Chunking
 │
 ▼
Embeddings (nomic-embed-text)
 │
 ▼
ChromaDB
 │
 ▼
Retriever
 │
 ▼
Prompt Builder
 │
 ▼
Ollama (llama3.2:3b)
 │
 ▼
AI Response

🛠️ Tech Stack

Category         Technology

Backend          FastAPI, PythonFrontend         StreamlitLLM              Ollama + llama3.2:3bEmbeddings       nomic-embed-textVector DB        ChromaDBPDF Processing   PyPDFRetrieval        RAG

📂 Project Structure

backend/
 ├── api/
 ├── services/
 ├── models/
 ├── utils/
 ├── config.py
 └── main.py
frontend/
 └── app.py
chroma_db/
README.md

⚙️ Workflow

Upload PDF.

Extract text.

Split into chunks.

Create embeddings.

Store vectors in ChromaDB.

Retrieve relevant chunks.

Send context + question to llama3.2:3b.

Generate grounded response.

🚀 Installation

git clone https://github.com/Sharanya185/research-paper-rag-assistant.git
cd research-paper-rag-assistant

python -m venv venv
venv\Scripts\activate

pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

ollama pull llama3.2:3b
ollama pull nomic-embed-text

python -m uvicorn backend.main:app --reload
streamlit run frontend/app.py

Note: The default model is llama3.2:3b because it providesfaster inference and lower memory usage on laptops.

🔮 Future Improvements

Multiple PDF support

Source highlighting

Citation support

Voice interaction

Docker deployment

Cloud deployment

👩‍💻 Author

Sharanya Rai K

GitHub: https://github.com/Sharanya185

⭐ If you like this project, consider starring the repository!