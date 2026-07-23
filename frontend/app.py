import streamlit as st
import requests

st.set_page_config(page_title="RAG Assistant", page_icon="📄", layout="wide")
API_URL = "http://localhost:8000/api"

st.title("📄 AI Research Paper Assistant")

if "session_id" not in st.session_state:
    st.session_state.session_id = None

pdf = st.file_uploader("Upload PDF", type="pdf")

if pdf and st.session_state.session_id is None:
    with st.spinner("Uploading and processing..."):
        files = {"file": (pdf.name, pdf.getvalue(), "application/pdf")}
        try:
            resp = requests.post(f"{API_URL}/upload", files=files, timeout=300)
        except requests.exceptions.ConnectionError:
            st.error("Can't reach the backend. Is `uvicorn backend.main:app --reload` running?")
            st.stop()

    if resp.status_code == 200:
        data = resp.json()
        st.session_state.session_id = data["session_id"]
        st.success(f"Loaded '{pdf.name}' — {data['num_pages']} pages, {data['num_chunks']} chunks")
    else:
        st.error(resp.json().get("detail", "Upload failed"))

if st.session_state.session_id:
    session_id = st.session_state.session_id
    tab1, tab2, tab3 = st.tabs(["📌 Summary", "❓ Ask a Question", "🧠 Explain a Concept"])

    with tab1:
        if st.button("Generate Summary"):
            with st.spinner("Reading the whole paper..."):
                resp = requests.post(f"{API_URL}/summarize/{session_id}", timeout=300)
            if resp.status_code == 200:
                st.write(resp.json()["summary"])
            else:
                st.error(resp.json().get("detail", "Summary failed"))

    with tab2:
        question = st.text_input("Enter your question", key="q_input")
        if st.button("Get Answer"):
            if question.strip():
                with st.spinner("Searching paper..."):
                    resp = requests.post(
                        f"{API_URL}/ask",
                        json={"session_id": session_id, "question": question},
                        timeout=180,
                    )
                if resp.status_code == 200:
                    data = resp.json()
                    st.write(data["answer"])
                    with st.expander("Sources used"):
                        for s in data["sources"]:
                            st.markdown(f"**Page {s['page']}** (relevance {s['score']:.2f})")
                            st.caption(s["text"] + "...")
                else:
                    st.error(resp.json().get("detail", "Failed"))
            else:
                st.warning("Enter a question")

    with tab3:
        concept = st.text_input("Enter concept", key="concept_input")
        if st.button("Explain"):
            if concept.strip():
                with st.spinner("Explaining..."):
                    resp = requests.post(
                        f"{API_URL}/explain",
                        json={"session_id": session_id, "concept": concept},
                        timeout=180,
                    )
                if resp.status_code == 200:
                    st.write(resp.json()["answer"])
                else:
                    st.error(resp.json().get("detail", "Failed"))
            else:
                st.warning("Enter a concept")

    if st.button("🔄 New Document"):
        st.session_state.session_id = None
        st.rerun()
else:
    st.info("Upload a PDF to start")
    