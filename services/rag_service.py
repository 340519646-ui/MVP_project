from core.rag.rag_engine import search
from core.llm.ai_client import ask_ai

def answer(question: str):
    docs = search(question)
    
    context = "\n".join(d["content"] for d in docs)
    
    prompt = f"""
基于以下内容回答问题：

{context}

问题：{question}
"""
    
    return ask_ai(prompt)