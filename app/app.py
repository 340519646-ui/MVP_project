import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
import streamlit as st
from services.planner_service import generate_activity

st.set_page_config(page_title="校园活动策划AI助手", layout="wide")

st.title("校园活动策划AI助手")
st.info("输入活动信息，AI将自动生成完整策划方案")

# 初始化状态
if "result" not in st.session_state:
    st.session_state["result"] = ""

# 输入区域
theme = st.text_input("活动主题")
type_ = st.text_input("活动类型")
budget = st.number_input("预算")

prompt_type = st.selectbox(
    "生成策略",
    [ "role", "step", "fewshot","rag"]
)

# 按钮逻辑
if st.button("生成策划案"):

    if theme == "":
        st.warning("⚠ 请输入活动主题")
    else:
        with st.spinner("AI正在生成策划案，请稍后..."):
            result = generate_activity(theme,type_,budget,prompt_type)

        # 存入状态（关键！）
        st.session_state["result"] = result

        st.success("策划案生成成功！")

# 显示结果（放在按钮外！）
if st.session_state["result"]:

    st.markdown("## AI生成策划案")
    st.write(st.session_state["result"])

    st.download_button(
        label="下载策划案",
        data=st.session_state["result"],
        file_name="activity_plan.md",
        mime="text/markdown"
    )