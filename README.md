AI Research Assistant

An AI-powered Research Paper Assistant built using Streamlit, Ollama, and Llama 3. The application allows users to upload research papers in PDF format, generate summaries, ask questions, and explain concepts using a simple Retrieval-Augmented Generation (RAG) pipeline.

---

Overview

This project implements a lightweight RAG-based application for research papers. After uploading a PDF, the application extracts the text, splits it into smaller chunks, retrieves the most relevant information based on the user's query, and generates responses using the Llama 3 model running locally with Ollama.

---

Features

- Upload research papers in PDF format
- Generate research paper summaries
- Ask questions about the uploaded document
- Explain concepts in simple language
- Keyword-based document retrieval
- Local inference using Ollama and Llama 3
- Interactive web interface with Streamlit

---

Tech Stack

- Python
- Streamlit
- Ollama
- Llama 3
- PyPDF
- Retrieval-Augmented Generation (RAG)

---

Project Structure

```
ai-research-assistant/
│── app.py
│── README.md
│── requirements.txt
│── .gitignore
```

---

Workflow

1. Upload a research paper in PDF format.
2. Extract text from the document.
3. Split the extracted text into smaller chunks.
4. Retrieve relevant chunks based on the user's query.
5. Generate summaries, answers, or explanations using Llama 3.

---

Skills Demonstrated

- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- PDF Text Processing
- Information Retrieval
- Streamlit Application Development
- Local AI Deployment

---

Future Improvements

- Integrate semantic search using embeddings
- Support multiple PDF documents
- Maintain conversation history
- Display source citations

---

Author

Sharanya Rai K

Artificial Intelligence & Machine Learning Engineering Student
