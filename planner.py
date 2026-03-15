from ai_client import ask_ai
import random
import os
import time


def generate_plan(theme, type_, budget, prompt_type):

    path = f"prompts/{prompt_type}.txt"

    # 读取prompt模板
    with open(path, "r", encoding="utf-8") as f:
        template = f.read()

    example = ""

    # 只有 basic 才读取案例
    if prompt_type == "basic":
        files = os.listdir("data")
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