from core.planner.planner import generate_plan
from core.rag.rag_engine import search
from core.llm.ai_client import ask_ai

def generate_with_rag(theme, type_, budget, prompt_type):
    
    # 1. 用RAG找参考案例
    docs = search(theme)
    context = "\n".join(d["content"] for d in docs)
    
    # 2. 把 context 注入 planner
    enhanced_theme = f"{theme}\n参考案例：{context}"
    
    # 3. 调用原 planner
    return generate_plan(enhanced_theme, type_, budget, prompt_type)