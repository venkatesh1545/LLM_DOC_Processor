from pathlib import Path
from typing import Final

# === Embeddings & Vector store =========================================
EMBED_MODEL: Final = "all-MiniLM-L6-v2"
VECTOR_DIMENSIONS: Final = 384            # dim of all-MiniLM-L6-v2
TOP_K: Final = 2                       # retrieved chunks per question
DOC_CHUNK_SIZE: Final = 512
DOC_CHUNK_OVERLAP: Final = 50

# === Ollama =============================================================
OLLAMA_MODEL: Final = "llama3.2"
OLLAMA_BASE_URL: Final = "http://localhost:11434"

# === Paths ============================================================== 
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
TMP_DIR = BASE_DIR / "tmp"
TMP_DIR.mkdir(parents=True, exist_ok=True)

