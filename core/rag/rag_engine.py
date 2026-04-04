from sentence_transformers import SentenceTransformer
import faiss
import os

# ===== 全局单例（关键）=====
_model = None
_docs = None
_doc_texts = None
_index = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            "/home/user_01/mvp/model",
            local_files_only=True
        )
    return _model


def load_docs():
    global _docs, _doc_texts

    if _docs is not None:
        return _docs, _doc_texts

    docs = []
    doc_texts = []

    for file in os.listdir("data"):
        with open(f"data/{file}", "r", encoding="utf-8") as f:
            text = f.read()
            docs.append(file)
            doc_texts.append(text)

    _docs = docs
    _doc_texts = doc_texts
    return docs, doc_texts


def build_index():
    global _index

    if _index is not None:
        return _index

    docs, doc_texts = load_docs()
    model = get_model()

    embeddings = model.encode(doc_texts, batch_size=32)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    _index = index
    return index


def search(query, k=2):
    model = get_model()
    docs, doc_texts = load_docs()
    index = build_index()

    q_emb = model.encode([query])
    D, I = index.search(q_emb, k)

    return [doc_texts[i] for i in I[0]]