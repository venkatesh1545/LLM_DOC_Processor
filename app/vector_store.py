import faiss, numpy as np
import logging
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
from app.config import EMBED_MODEL, VECTOR_DIMENSIONS

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self) -> None:
        self.model  = SentenceTransformer(EMBED_MODEL)
        # Use IndexFlatL2 instead of IndexFlatIP for better compatibility
        self.index  = faiss.IndexFlatL2(VECTOR_DIMENSIONS)
        self.meta:   List[Tuple[str,int]] = []   # (sourceURL, chunk_id)
        self.chunks: List[str]            = []   # actual text

    # ── add many chunks ───────────────────────────────────────────
    def add(self, chunks: List[str], source: str) -> None:
        logger.info(f"Adding {len(chunks)} chunks from {source}")
        logger.info(f"Before adding - index total: {self.index.ntotal}, chunks: {len(self.chunks)}")
        
        vecs = self.model.encode(chunks, normalize_embeddings=True)
        logger.info(f"Generated embeddings shape: {vecs.shape}")
        
        # Convert to float32 and ensure proper shape
        vecs_float32 = vecs.astype(np.float32)
        logger.info(f"Float32 embeddings shape: {vecs_float32.shape}")
        
        self.index.add(vecs_float32)
        self.meta.extend((source, i) for i in range(len(chunks)))
        self.chunks.extend(chunks)
        
        logger.info(f"After adding - index total: {self.index.ntotal}, chunks: {len(self.chunks)}")
        logger.info(f"Index is trained: {self.index.is_trained}")

    # ── similarity search ─────────────────────────────────────────
    def search(self, query: str, k: int = 8):
        logger.info(f"Searching for query: {query[:50]}...")
        logger.info(f"Index total: {self.index.ntotal}, chunks: {len(self.chunks)}")
        
        if self.index.ntotal == 0:
            logger.warning("Index is empty, returning no results")
            return []
        qv = self.model.encode([query], normalize_embeddings=True).astype(np.float32)
        scores, idxs = self.index.search(qv, k)
        out = []
        for s, ix in zip(scores[0], idxs[0]):
            if ix == -1:            # FAISS pad value
                continue
            src, cid = self.meta[ix]
            out.append((s, src, cid, self.chunks[ix]))
        logger.info(f"Found {len(out)} results")
        return out

# ── GLOBAL instance every module imports ──────────────────────────
store = VectorStore()
