import faiss
import numpy as np

class VectorStore:
    def __init__(self, docs, embeddings):
        self.docs = docs
        self.embeddings = np.array(embeddings).astype("float32")

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    def search(self, query_vec, top_k=3):
        query_vec = np.array(query_vec).astype("float32").reshape(1, -1)
        distances, indices = self.index.search(query_vec, top_k)
        return [self.docs[i] for i in indices[0]]
