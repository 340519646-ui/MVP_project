import streamlit as st
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.planner_service import generate_plan_service

st.set_page_config(page_title="校园活动策划AI助手", layout="wide")

st.title("校园活动策划AI助手")

theme = st.text_input("活动主题")
type_ = st.text_input("活动类型")
budget = st.number_input("预算",step=1)
person = st.number_input("人数",step=1)
prompt_type = st.selectbox(
    "生成策略",
    ["role", "step", "fewshot", "rag"]
)
mode = st.selectbox(
    "使用模式",
    ["生成策划案","优化策划案"]
)

if "result" not in st.session_state:
    st.session_state["result"] = None

if "history" not in st.session_state:
    st.session_state["history"] = []
    
if mode =="生成策划案":
    if st.button("生成"):

        if theme == "":
            st.warning("请输入主题")
        else:
            with st.spinner("生成中..."):
                result = generate_plan_service(
                    theme, 
                    type_, 
                    budget, 
                    prompt_type,
                    person,
                    )

            st.session_state["result"] = result
            
            #初始化对话历史
            st.session_state["history"]=[
                {
                    "user": f"生成策划案：主题={theme}, 类型={type_}, 预算={budget}, 人数={person}",
                    "ai": result
                }
            ]
elif mode == "优化策划案":
    if not st.session_state["history"]:
        st.info("请先生成一版策划案，再进行优化。")
        st.stop()
    user_input = st.chat_input("请输入修改需求，例如：互动细节/预算细节")
    
    for h in st.session_state["history"]:
        with st.chat_message("user"):
            st.write(h["user"])
        with st.chat_message("assistant"):
            st.write(h["ai"])

    if user_input:

        st.session_state["history"].append({
            "user": user_input,
            "ai": ""
        })

        result = generate_plan_service(
            theme="策划优化",
            type_=type_,
            budget=budget,
            prompt_type="rag",   
            person=person,
            history=st.session_state["history"]
        )

        st.session_state["history"][-1]["ai"] = result

        st.rerun()

if mode=="生成策划案" and st.session_state["result"]:
    st.markdown("## 策划案")
    st.markdown(st.session_state["result"])