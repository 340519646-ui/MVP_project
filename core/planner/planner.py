from core.llm.ai_client import ask_ai
from services.prompts_choice import prompts_choice

import os
import time


def generate_plan(theme, type_, budget, prompt_type,person,history=None):
    
    
    final_prompt = prompts_choice(theme, type_, budget, prompt_type,person)


    result = ask_ai(final_prompt)

    os.makedirs("output", exist_ok=True)
    filename = f"output/{prompt_type}_{int(time.time())}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(result)

    return result