import streamlit as st
from pypdf import PdfReader
import ollama

# -------------------------------
# UI Setup
# -------------------------------
st.set_page_config(page_title="AI Assistant")

st.title("📄 AI Research Paper Assistant")


# -------------------------------
# Extract text
# -------------------------------
def extract_text(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        st.error(f"Error: {e}")
        return ""

# -------------------------------
# Summarization
# -------------------------------
def summarize(text):
    prompt = f"""
Summarize this research paper in simple terms:
{text[:3000]}
"""
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# -------------------------------
# Question Answering
# -------------------------------
def answer_question(text, question):
    prompt = f"""
Based on the following research paper, answer the question.

Paper:
{text[:3000]}

Question:
{question}
"""
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# -------------------------------
# Explain Concept
# -------------------------------
def explain(concept):
    prompt = f"""
Explain this concept in simple terms:
{concept}
"""
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]


pdf = st.file_uploader("Upload PDF", type="pdf")

if pdf:
    st.success("PDF uploaded successfully!")
    

    text = extract_text(pdf)

    if text:
        #  Summarize
        if st.button(" Summarize"):
            st.write(summarize(text))

        #  Q&A
        st.subheader(" Ask Question")
        question = st.text_input("Enter question")

        if st.button("Get Answer"):
            if question:
                st.write(answer_question(text, question))
            else:
                st.warning("Enter a question")

        #  Explain
        st.subheader(" Explain Concept")
        concept = st.text_input("Enter concept")

        if st.button("Explain"):
            if concept:
                st.write(explain(concept))
            else:
                st.warning("Enter a concept")

    else:
        st.warning("No text found")

else:
    st.info("Upload a PDF to start")