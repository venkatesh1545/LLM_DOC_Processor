import logging
import sys
import os

# Add the current directory to Python path to ensure proper imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO)

# Import after setting up the path
from app.doc_ingest import ingest
from app.vector_store import store
from app.query_handler import run_query

# Test document ingestion
url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"

print("Testing document ingestion...")
print(f"Store ID before ingestion: {id(store)}")
ingest([url])

print(f"Store ID after ingestion: {id(store)}")
print(f"Vector store has {store.index.ntotal} total vectors")
print(f"Number of chunks: {len(store.chunks)}")
print(f"Number of metadata entries: {len(store.meta)}")

# Test search
question = "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?"
print(f"\nSearching for: {question}")
results = store.search(question, k=5)

print(f"Found {len(results)} results:")
for i, (score, src, cid, chunk_text) in enumerate(results):
    print(f"\nResult {i+1}:")
    print(f"Score: {score:.3f}")
    print(f"Source: {src}")
    print(f"Chunk ID: {cid}")
    print(f"Text: {chunk_text[:200]}...")

# Test the full query handler
print(f"\nTesting full query handler...")
result = run_query(question)
print(f"Query result: {result}") 