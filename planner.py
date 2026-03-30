from ai_client import ask_ai
from rag_engine import load_docs,build_index,search
import random
import os
import time

load_docs()
index, _ =build_index()

def generate_plan(theme, type_, budget, prompt_type):

    path = f"prompts/{prompt_type}.txt"

    # 读取prompt模板
    with open(path, "r", encoding="utf-8") as f:
        template = f.read()

    example = ""

    # 只有 fewshot 才读取案例
    if prompt_type == "fewshot":
        files = os.listdir("data")
        
        related_files = [f for f in files if type_ in f]
        #向量化搜索
        if related_files:
            example_file = random.choice(related_files)
        else:
            example_file = random.choice(files)

        with open(f"data/{example_file}", "r", encoding="utf-8") as f:
            example = f.read()

    # 填充prompt
    prompt = template.format(
        theme=theme,
        type=type_,
        budget=budget,
        example=example
    )

    # 调用AI
    result = ask_ai(prompt)

    # 保存结果
    filename = f"output/{prompt_type}_{int(time.time())}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)

    return result