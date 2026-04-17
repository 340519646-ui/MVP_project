from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "model"
DATA_DIR = BASE_DIR / "data"

_model = None
_docs = None
_doc_texts = None
_index = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            str(MODEL_DIR),
            local_files_only=True,
        )
    return _model


def load_docs():
    global _docs, _doc_texts

    if _docs is not None:
        return _docs, _doc_texts

    docs = []
    doc_texts = []

    for file_path in sorted(DATA_DIR.iterdir()):
        if not file_path.is_file() or file_path.suffix != ".txt":
            continue

        text = file_path.read_text(encoding="utf-8")
        docs.append(file_path.name)
        doc_texts.append(text)

    _docs = docs
    _doc_texts = doc_texts
    return docs, doc_texts


def build_index():
    global _index

    if _index is not None:
        return _index

    docs, doc_texts = load_docs()
    if not docs:
        raise ValueError("No text documents found in data directory")

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

    if not docs:
        return []

    limit = min(k, len(doc_texts))
    q_emb = model.encode([query])
    _, indices = index.search(q_emb, limit)
    return [doc_texts[i] for i in indices[0]]
