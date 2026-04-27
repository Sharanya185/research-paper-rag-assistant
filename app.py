import streamlit as st
from pypdf import PdfReader
import ollama

# -------------------------------
# UI
# -------------------------------
st.set_page_config(page_title="RAG Assistant")
st.title("📄 AI Research Paper Assistant (Simple RAG)")

# -------------------------------
# Extract Text
# -------------------------------
def extract_text(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content
    return text

# -------------------------------
# Chunking
# -------------------------------
def chunk_text(text, chunk_size=500):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

# -------------------------------
# Simple Retrieval 
# -------------------------------
def retrieve_chunks(query, chunks, k=3):
    query_words = query.lower().split()
    scores = []

    for chunk in chunks:
        score = sum(chunk.lower().count(word) for word in query_words)
        scores.append((score, chunk))

    scores.sort(reverse=True, key=lambda x: x[0])
    return [chunk for score, chunk in scores[:k]]

# -------------------------------
# RAG Query
# -------------------------------
def rag_query(query, chunks):
    relevant_chunks = retrieve_chunks(query, chunks)
    context = "\n".join(relevant_chunks)

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

# -------------------------------
# Summarization
# -------------------------------
def summarize(chunks):
    context = "\n".join(chunks[:5])

    prompt = f"""
Summarize the research paper in simple terms:

{context}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]

# -------------------------------
# MAIN
# -------------------------------
pdf = st.file_uploader("Upload PDF", type="pdf")

if pdf:
    st.success("PDF uploaded successfully!")

    text = extract_text(pdf)

    if text:
        chunks = chunk_text(text)

        # 🔹 Summarize
        if st.button("📌 Summarize"):
            st.write(summarize(chunks))

        # 🔹 Q&A
        st.subheader("❓ Ask Question")
        question = st.text_input("Enter your question")

        if st.button("Get Answer"):
            if question:
                st.write(rag_query(question, chunks))
            else:
                st.warning("Enter a question")

        # 🔹 Explain
        st.subheader("🧠 Explain Concept")
        concept = st.text_input("Enter concept")

        if st.button("Explain"):
            if concept:
                st.write(rag_query(f"Explain {concept} in simple terms", chunks))
            else:
                st.warning("Enter a concept")

    else:
        st.warning("No text found")

else:
    st.info("Upload a PDF to start")