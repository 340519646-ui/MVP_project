from pathlib import Path

import yaml

from core.engine.Skill_Engine import SkillEngine


SKILL_PATH = Path(__file__).resolve().parents[1] / "skill" / "Skill_definition.yaml"
_planner_engine = None


def get_planner_engine():
    global _planner_engine
    if _planner_engine is None:
        with SKILL_PATH.open("r", encoding="utf-8") as file:
            skill_config = yaml.safe_load(file)
        _planner_engine = SkillEngine(skill_config, base_dir=SKILL_PATH.parent.parent)
    return _planner_engine


def run_planner_skill(input_data, history=None):
    return get_planner_engine().run(input_data, history=history)


def generate_plan_markdown(
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
    result = run_planner_skill(
        {
            "theme": theme,
            "type_": type_,
            "budget": budget,
            "prompt_type": prompt_type,
            "person": person,
            "duration": duration,
            "venue_type": venue_type,
            "target_audience": target_audience,
            "goal_priority": goal_priority,
            "llm_mode": mode,
        },
        history=history,
    )
    return result["plan_markdown"]
