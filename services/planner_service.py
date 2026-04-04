from core.planner.planner import generate_plan


def generate_plan_service(theme, type_, budget, prompt_type):
    return generate_plan(theme, type_, budget, prompt_type)