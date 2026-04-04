import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.planner_service import generate_plan_service

st.set_page_config(page_title="校园活动策划AI助手", layout="wide")

st.title("校园活动策划AI助手")

theme = st.text_input("活动主题")
type_ = st.text_input("活动类型")
budget = st.number_input("预算")

prompt_type = st.selectbox(
    "生成策略",
    ["role", "step", "fewshot", "rag"]
)

if "result" not in st.session_state:
    st.session_state["result"] = ""

if st.button("生成策划案"):

    if theme == "":
        st.warning("请输入主题")
    else:
        with st.spinner("生成中..."):
            result = generate_plan_service(theme, type_, budget, prompt_type)

        st.session_state["result"] = result

if st.session_state["result"]:
    st.markdown("## 策划案")
    st.write(result)