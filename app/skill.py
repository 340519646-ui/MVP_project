import os
import sys

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.skill_service import run_planner_skill


st.title("校园活动策划 Skill System")

theme = st.text_input("活动主题")
type_ = st.selectbox("活动类型", ["文艺", "体育", "学术", "公益"])
budget = st.number_input("预算", 0, 10000, 1000)
person = st.number_input("人数", 10, 1000, 100)
duration = st.number_input("活动时长(小时)", 1, 24, 3)
venue_type = st.selectbox("场地类型", ["室内", "室外", "线上"])
target_audience = st.text_input("目标人群", "本科生")
goal_priority = st.text_input("核心目标", "参与度")
prompt_type = st.selectbox("策略", ["role", "step", "fewshot", "rag"], index=3)

input_data = {
    "theme": theme,
    "type_": type_,
    "budget": budget,
    "person": person,
    "duration": duration,
    "venue_type": venue_type,
    "target_audience": target_audience,
    "goal_priority": goal_priority,
    "prompt_type": prompt_type,
}

if st.button("生成策划案"):
    with st.spinner("Skill运行中..."):
        result = run_planner_skill(input_data)

    st.success("生成完成")
    st.subheader("结构化结果")
    st.json(result)
    st.subheader("策划案预览")
    st.markdown(result["plan_markdown"])
