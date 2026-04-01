#from sentence_transformers import SentenceTransformer
#import faiss
import os

#model = SentenceTransformer("all-MiniLM-L6-v2")
# core/rag/rag_engine.py

def load_docs():
    return [
        {"content": "这是测试文档A"},
        {"content": "这是测试文档B"},
        {"content": "这是测试文档C"}
    ]


def build_index():
    docs = load_docs()
    return docs, None


def search(query):
    docs, _ = build_index()
    return docs[:2]  # 返回前2条
#docs = []
#doc_texts = []

#def load_docs():
    #global docs, doc_texts

    #for file in os.listdir("data"):
        #with open(f"data/{file}", "r", encoding="utf-8") as f:
            #text = f.read()
            #docs.append(file)
            #doc_texts.append(text)

#def build_index():
    # embeddings = model.encode(doc_texts)
    # dim = embeddings.shape[1]

    # index = faiss.IndexFlatL2(dim)
    # index.add(embeddings)

    # return index, embeddings

#def search(query, index, k=2):
    # q_emb = model.encode([query])
    # D, I = index.search(q_emb, k)

    # return [doc_texts[i] for i in I[0]]