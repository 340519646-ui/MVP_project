from core.llm.ai_client import ask_ai
from services.prompts_choice import prompts_choice



def generate_plan(theme, type_, budget, prompt_type,person,duration,venue_type,target_audience,goal_priority,history=None):
    
    
    final_prompt = prompts_choice(theme, type_, budget, prompt_type,person,duration,venue_type,target_audience,goal_priority)
 

    return ask_ai(prompt=final_prompt,history=history,mode="generate")