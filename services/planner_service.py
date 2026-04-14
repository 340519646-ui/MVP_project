from core.planner.planner import generate_plan


def generate_plan_service(theme, type_, budget, prompt_type,person,duration,venue_type,target_audience,goal_priority,history=None):
    return generate_plan(theme, type_, budget, prompt_type,person,history=history,duration=duration,venue_type=venue_type,target_audience=target_audience,goal_priority=goal_priority)

