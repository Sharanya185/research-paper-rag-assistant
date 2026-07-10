import streamlit as st
from pypdf import PdfReader
import ollama
import numpy as np
import re

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(page_title="RAG Assistant", page_icon="📄", layout="wide")
CHAT_MODEL = "llama3"
EMBED_MODEL = "nomic-embed-text"   # run: ollama pull nomic-embed-text

st.title("📄 AI Research Paper Assistant (RAG)")

# =========================================================
# HELPERS: Ollama connectivity check
# =========================================================
@st.cache_data(show_spinner=False)
def check_ollama():
    try:
        models = ollama.list()
        names = [m.get("model", m.get("name", "")) for m in models.get("models", [])]
        return True, names
    except Exception as e:
        return False, str(e)

# =========================================================
# EXTRACT TEXT (per-page, so we can keep page numbers)
# =========================================================
@st.cache_data(show_spinner=False)
def extract_pages(file_bytes):
    reader = PdfReader(file_bytes)
    pages = []
    for i, page in enumerate(reader.pages):
        content = page.extract_text() or ""
        content = re.sub(r"\s+", " ", content).strip()
        if content:
            pages.append((i + 1, content))
    return pages

# =========================================================
# CHUNKING: word-based with overlap, keeps page reference
# =========================================================
def chunk_pages(pages, chunk_size=220, overlap=40):
    chunks = []
    for page_num, text in pages:
        words = text.split()
        i = 0
        while i < len(words):
            piece = words[i:i + chunk_size]
            if piece:
                chunks.append({
                    "text": " ".join(piece),
                    "page": page_num
                })
            i += max(chunk_size - overlap, 1)
    return chunks

# =========================================================
# EMBEDDINGS + retrieval (cosine similarity)
# =========================================================
@st.cache_data(show_spinner=False)
def embed_texts(texts, _cache_key):
    vectors = []
    for t in texts:
        resp = ollama.embeddings(model=EMBED_MODEL, prompt=t)
        vectors.append(resp["embedding"])
    return np.array(vectors, dtype=np.float32)

def embed_query(query):
    resp = ollama.embeddings(model=EMBED_MODEL, prompt=query)
    return np.array(resp["embedding"], dtype=np.float32)

def cosine_sim(matrix, vector):
    matrix_norm = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-8)
    vec_norm = vector / (np.linalg.norm(vector) + 1e-8)
    return matrix_norm @ vec_norm

def retrieve(query, chunks, embeddings, k=4):
    q_vec = embed_query(query)
    sims = cosine_sim(embeddings, q_vec)
    top_idx = np.argsort(sims)[::-1][:k]
    return [(chunks[i], float(sims[i])) for i in top_idx]

# =========================================================
# GENERATION
# =========================================================
def call_llm(prompt, temperature=0.2):
    response = ollama.chat(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": temperature},
    )
    return response["message"]["content"]

def rag_answer(query, chunks, embeddings, k=4):
    results = retrieve(query, chunks, embeddings, k=k)
    context = "\n\n".join(
        f"[Page {c['page']}] {c['text']}" for c, _ in results
    )
    prompt = f"""You are a research assistant. Answer the question using ONLY the context below.
If the answer is not contained in the context, say "I couldn't find that in the paper."
Cite page numbers in your answer where relevant.

Context:
{context}

Question: {query}

Answer:"""
    answer = call_llm(prompt)
    return answer, results

def summarize_document(chunks, embeddings):
    """Map-reduce summary so the whole document is covered, not just the start."""
    n = len(chunks)
    group_size = max(1, n // 6)  # ~6 groups spanning the whole doc
    groups = [chunks[i:i + group_size] for i in range(0, n, group_size)]

    partial_summaries = []
    progress = st.progress(0.0, text="Summarizing sections...")
    for idx, group in enumerate(groups):
        text = "\n".join(c["text"] for c in group)
        prompt = f"Summarize the key points of this excerpt from a research paper in 2-3 sentences:\n\n{text}"
        partial_summaries.append(call_llm(prompt))
        progress.progress((idx + 1) / len(groups), text="Summarizing sections...")
    progress.empty()

    combined = "\n".join(partial_summaries)
    final_prompt = f"""Combine these section summaries into one coherent, simple summary of the research paper.
Include: the main problem, method/approach, key findings, and significance.

Section summaries:
{combined}

Final summary:"""
    return call_llm(final_prompt)

# =========================================================
# SIDEBAR SETTINGS
# =========================================================
with st.sidebar:
    st.header("⚙️ Settings")
    chunk_size = st.slider("Chunk size (words)", 100, 400, 220, 20)
    overlap = st.slider("Chunk overlap (words)", 0, 100, 40, 10)
    top_k = st.slider("Chunks retrieved per question", 1, 8, 4, 1)

    ok, info = check_ollama()
    if ok:
        st.success("Ollama connected")
        st.caption(f"Models available: {', '.join(info) if info else 'none found'}")
        if EMBED_MODEL not in " ".join(info):
            st.warning(f"'{EMBED_MODEL}' not found. Run: ollama pull {EMBED_MODEL}")
        if CHAT_MODEL not in " ".join(info):
            st.warning(f"'{CHAT_MODEL}' not found. Run: ollama pull {CHAT_MODEL}")
    else:
        st.error("Can't reach Ollama. Is it running? (`ollama serve`)")
        st.caption(str(info))

# =========================================================
# MAIN
# =========================================================
pdf = st.file_uploader("Upload PDF", type="pdf")

if pdf:
    with st.spinner("Reading PDF..."):
        pages = extract_pages(pdf)

    if not pages:
        st.warning("No extractable text found in this PDF (it may be scanned/image-based).")
        st.stop()

    st.success(f"PDF loaded — {len(pages)} pages with text.")

    chunks = chunk_pages(pages, chunk_size=chunk_size, overlap=overlap)
    cache_key = f"{pdf.file_id if hasattr(pdf, 'file_id') else pdf.name}-{chunk_size}-{overlap}"

    with st.spinner(f"Embedding {len(chunks)} chunks..."):
        try:
            embeddings = embed_texts([c["text"] for c in chunks], cache_key)
        except Exception as e:
            st.error(f"Embedding failed: {e}")
            st.stop()

    tab1, tab2, tab3 = st.tabs(["📌 Summary", "❓ Ask a Question", "🧠 Explain a Concept"])

    with tab1:
        if st.button("Generate Summary"):
            with st.spinner("Reading the whole paper..."):
                st.write(summarize_document(chunks, embeddings))

    with tab2:
        question = st.text_input("Enter your question", key="q_input")
        if st.button("Get Answer"):
            if question.strip():
                with st.spinner("Searching paper and generating answer..."):
                    answer, sources = rag_answer(question, chunks, embeddings, k=top_k)
                st.write(answer)
                with st.expander("Sources used"):
                    for c, score in sources:
                        st.markdown(f"**Page {c['page']}** (relevance {score:.2f})")
                        st.caption(c["text"][:300] + "...")
            else:
                st.warning("Enter a question")

    with tab3:
        concept = st.text_input("Enter concept", key="concept_input")
        if st.button("Explain"):
            if concept.strip():
                with st.spinner("Explaining..."):
                    answer, sources = rag_answer(
                        f"Explain the concept of '{concept}' as it is used in this paper, in simple terms.",
                        chunks, embeddings, k=top_k
                    )
                st.write(answer)
                with st.expander("Sources used"):
                    for c, score in sources:
                        st.markdown(f"**Page {c['page']}** (relevance {score:.2f})")
                        st.caption(c["text"][:300] + "...")
            else:
                st.warning("Enter a concept")

else:
    st.info("Upload a PDF to start")