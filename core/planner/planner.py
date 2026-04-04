from core.llm.ai_client import ask_ai
from core.rag.rag_engine import search
import os
import random
import time


def generate_plan(theme, type_, budget, prompt_type):

    query = f"{theme} {type_} 校园活动"
    
    # ===== RAG =====
    context_docs = search(query)
    context = "\n\n".join(context_docs)

    # ===== analysis =====
    analysis_prompt = f"""
分析这个活动的关键策划要点：

主题：{theme}
类型：{type_}
预算：{budget}

列出5条关键点
"""
    analysis = ask_ai(analysis_prompt)

    # ===== prompt =====
    path = f"prompts/{prompt_type}.txt"
    with open(path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    example = ""

    if prompt_type == "fewshot":
        files = os.listdir("data")
        example_file = random.choice(files)

        with open(f"data/{example_file}", "r", encoding="utf-8") as f:
            example = f.read()

    elif prompt_type == "rag":
        example = context

    final_prompt = f"""
请根据以下信息生成活动策划：

主题：{theme}
类型：{type_}
预算：{budget}
已有分析:{analysis}
请用【Markdown格式】输出，要求：

1. 必须有清晰结构
2. 使用标题（#、##）
3. 使用分点（- / 1.）
4. 内容要具体、可执行
5. 适合校园场景

输出格式示例：

# 🎉 活动名称

## 📌 活动简介
...

## 📅 活动流程
1. ...
2. ...

## 📦 物资清单
- ...
- ...

## 💰 预算分配
- ...
"""

    result = ask_ai(final_prompt)

    os.makedirs("output", exist_ok=True)
    filename = f"output/{prompt_type}_{int(time.time())}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)

    return result