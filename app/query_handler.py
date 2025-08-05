from typing import List, Dict
from app.vector_store import store
from app.config import TOP_K
from app.ollama_client import answer_question

def run_query(question: str) -> Dict[str, str]:
    """Retrieve context → LLM → structured answer dict."""
    hits = store.search(question, TOP_K)
    if not hits:
        return {"answer": "I don't know - no relevant information found.", "clauses": []}

    # Build context string with actual chunk text
    context_parts = []
    clause_refs = []
    for score, src, cid, chunk_text in hits:
        context_parts.append(chunk_text)
        clause_refs.append(f"[{src} - chunk {cid} - score {score:.2f}]")
    
    context = "\n\n".join(context_parts)
    answer_text = answer_question(question, context)
    
    return {"answer": answer_text, "clauses": clause_refs}
