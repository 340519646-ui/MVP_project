from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

class CaseVectorDB:
    def __init__(self, data_path):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.index = None
        self.embeddings = None
        self.build()

    def build(self):
        texts = [c["theme"] + c["content"] for c in self.data]

        self.embeddings = self.model.encode(texts)

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings))

    def search(self, query, top_k=5):
        q_emb = self.model.encode([query])
        D, I = self.index.search(np.array(q_emb), top_k)

        return [self.data[i] for i in I[0]]