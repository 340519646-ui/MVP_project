from services.skill_service import generate_plan_markdown


def generate_plan(
    theme,
    type_,
    budget,
    prompt_type,
    person,
    duration,
    venue_type,
    target_audience,
    goal_priority,
    history=None,
    mode="generate",
):
    return generate_plan_markdown(
        theme=theme,
        type_=type_,
        budget=budget,
        prompt_type=prompt_type,
        person=person,
        duration=duration,
        venue_type=venue_type,
        target_audience=target_audience,
        goal_priority=goal_priority,
        history=history,
        mode=mode,
    )
