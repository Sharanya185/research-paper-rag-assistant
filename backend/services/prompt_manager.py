class PromptManager:
    def build_rag_prompt(self, query: str, context_chunks: list, history: str = "") -> str:
        context = "\n\n".join(f"[Page {c['page']}] {c['text']}" for c in context_chunks)
        history_block = f"\nConversation so far:\n{history}\n" if history else ""
        return f"""You are a research assistant. Answer the question using ONLY the context below.
If the answer is not contained in the context, say "I couldn't find that in the paper."
Cite page numbers in your answer where relevant.
{history_block}
Context:
{context}

Question: {query}

Answer:"""

    def build_section_summary_prompt(self, text: str) -> str:
        return f"Summarize the key points of this excerpt from a research paper in 2-3 sentences:\n\n{text}"

    def build_final_summary_prompt(self, combined_summaries: str) -> str:
        return f"""Combine these section summaries into one coherent, simple summary of the research paper.
Include: the main problem, method/approach, key findings, and significance.

Section summaries:
{combined_summaries}

Final summary:"""

    def build_concept_prompt(self, concept: str) -> str:
        return f"Explain the concept of '{concept}' as it is used in this paper, in simple terms."