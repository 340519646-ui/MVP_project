from core.llm.ai_client import ask_ai
from core.rag.rag_engine import search
from services.prompt_loader import render_prompt
from services.prompt_loader import compress_docs
import os

import random
import time


def generate_plan(theme, type_, budget, prompt_type,person):

    query = f"{theme} {type_} 校园活动"
    
    # ===== analysis =====
    analysis_prompt = f"""
分析这个活动的关键策划要点：

主题：{theme}
类型：{type_}
预算：{budget}
人数: {person}

列出5条关键点
"""
    analysis = ask_ai(analysis_prompt)

    example = None
    if prompt_type in ["role" , "step"]:
        final_prompt=render_prompt("{role}.txt",{
            "theme":theme,
            "budget":budget,
            "type": type_,
            "person":person
        })
    elif prompt_type == "fewshot":
        files = os.listdir("data")
        example_file = random.choice(files)

        with open(f"data/{example_file}", "r", encoding="utf-8") as f:
            example = f.read()
        final_prompt=render_prompt("{fewshot}.txt",{
            "example":example,
            "theme":theme,
            "budget":budget,
            "type": type_,
            "person":person
        })

    elif prompt_type == "rag":
        context_docs = search(query)
        context_docs = [doc[:500] for doc in context_docs]
        summary = compress_docs(context_docs)
        final_prompt=render_prompt("{rag}.txt",{
            "theme": theme,
            "type" : type_,
            "budget":budget,
            "person":person,
            "analysis": analysis,
            "summary" : summary
            })


    result = ask_ai(final_prompt)

    os.makedirs("output", exist_ok=True)
    filename = f"output/{prompt_type}_{int(time.time())}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)

    return result