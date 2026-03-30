from sentence_transformers import SentenceTransformer
import faiss
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

docs = []
doc_texts = []

def load_docs():
    global docs, doc_texts

    for file in os.listdir("data"):
        with open(f"data/{file}", "r", encoding="utf-8") as f:
            text = f.read()
            docs.append(file)
            doc_texts.append(text)

def build_index():
    embeddings = model.encode(doc_texts)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    return index, embeddings

def search(query, index, k=2):
    q_emb = model.encode([query])
    D, I = index.search(q_emb, k)

    return [doc_texts[i] for i in I[0]]