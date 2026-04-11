from core.llm.ai_client import ask_ai
from services.prompts_choice import prompts_choice

import os


def generate_plan(theme, type_, budget, prompt_type,person,history=None):
    
    
    final_prompt = prompts_choice(theme, type_, budget, prompt_type,person)
 

    return ask_ai(prompt=final_prompt,history=history,mode="generate")