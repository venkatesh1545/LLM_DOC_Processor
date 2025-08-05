from app.vector_store import store
import numpy as np

print("Testing global store instance...")
print(f"Initial state - index total: {store.index.ntotal}, chunks: {len(store.chunks)}")

# Add some test data
test_chunks = ["This is a test chunk", "Another test chunk"]
test_embeddings = np.random.rand(2, 384).astype(np.float32)

store.index.add(test_embeddings)
store.chunks.extend(test_chunks)
store.meta.extend([("test", i) for i in range(len(test_chunks))])

print(f"After adding test data - index total: {store.index.ntotal}, chunks: {len(store.chunks)}")

# Test search
results = store.search("test chunk")
print(f"Search results: {len(results)}")
for score, src, cid, text in results:
    print(f"Score: {score:.3f}, Text: {text}") 