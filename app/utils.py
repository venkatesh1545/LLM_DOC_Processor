import re, requests, html, magic, tempfile
from pathlib import Path
from typing import List
from pdfminer.high_level import extract_text as pdf_text
from docx import Document
from app.config import TMP_DIR, DOC_CHUNK_SIZE, DOC_CHUNK_OVERLAP

def download(url: str) -> bytes:
    r = requests.get(url, timeout=90)
    r.raise_for_status()
    return r.content

def load_text(blob: bytes) -> str:
    mime = magic.from_buffer(blob, mime=True)

    with tempfile.NamedTemporaryFile(dir=TMP_DIR, delete=False) as tmp:
        tmp.write(blob)
        tmp_path = Path(tmp.name)

    if "pdf" in mime:
        return pdf_text(str(tmp_path))
    if ("word" in mime) or ("officedocument" in mime):
        doc = Document(str(tmp_path))
        return "\n".join(p.text for p in doc.paragraphs)
    if mime.startswith("text") or "html" in mime:
        text = blob.decode(errors="ignore")
        # strip simple HTML
        text = re.sub(r"<[^>]+>", " ", text)
        return html.unescape(text)
    # fallback
    return blob.decode(errors="ignore")

def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def chunk_text(text: str, size: int = DOC_CHUNK_SIZE, overlap: int = DOC_CHUNK_OVERLAP) -> List[str]:
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i:i+size]))
        i += size - overlap
    return chunks
