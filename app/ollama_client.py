import json
import logging
import requests
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL

logger = logging.getLogger(__name__)

HEADERS = {"Content-Type": "application/json"}

def _generate(prompt: str, system: str = "") -> str:
    """Low-level helper that calls Ollama /api/generate."""
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "temperature": 0.1,
    }
    r = requests.post(url, headers=HEADERS, data=json.dumps(payload), timeout=90)
    r.raise_for_status()
    return r.json()["response"]

def answer_question(question: str, context: str) -> str:
    """Call the LLM with retrieved context and a single question."""
    system_prompt = (
        "You are an insurance policy assistant. Use ONLY the provided context "
        "to answer the question. Quote exact sentences as evidence where helpful. "
        "If the context is insufficient, say 'I don't know' and nothing else."
    )
    prompt = (
        f"Context:\n\"\"\"\n{context}\n\"\"\"\n\n"
        f"Question: {question}\n\n"
        "Answer in 1-2 sentences, then list the clause(s) you used in square brackets."
    )
    logger.info("Sending prompt to Ollama (%.1f tokens)", len(prompt) / 4)
    return _generate(prompt, system_prompt)
