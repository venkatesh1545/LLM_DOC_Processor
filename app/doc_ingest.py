import logging, tempfile
from pathlib import Path
from typing import List
from app.utils import download, load_text, clean, chunk_text
from app.vector_store import store
from app.config import DOC_CHUNK_SIZE, DOC_CHUNK_OVERLAP

logger = logging.getLogger(__name__)

def ingest(urls: List[str]) -> None:
    """Download, parse and index each document URL."""
    for url in urls:
        try:
            logger.info("Downloading %s", url)
            blob = download(url)
            logger.info(f"Downloaded {len(blob)} bytes")
            
            text = load_text(blob)
            logger.info(f"Extracted text length: {len(text)} characters")
            
            text = clean(text)
            logger.info(f"Cleaned text length: {len(text)} characters")
            
            chunks = chunk_text(text, DOC_CHUNK_SIZE, DOC_CHUNK_OVERLAP)
            logger.info("Indexed %d chunks from %s", len(chunks), url)
            
            store.add(chunks, url)
            logger.info("Successfully added chunks to vector store")
            
        except Exception as e:
            logger.error(f"Error processing URL {url}: {str(e)}", exc_info=True)
            raise
