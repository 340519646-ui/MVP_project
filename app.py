import streamlit as st
from planner import generate_plan

st.set_page_config(page_title="校园活动策划AI助手", layout="wide")

st.title("校园活动策划AI助手")

st.info("输入活动信息，AI将自动生成完整策划方案")

theme = st.text_input("活动主题")

type_=st.text_input("活动类型")

budget = st.number_input("预算")

prompt_type = st.selectbox(
    "生成策略",
    ["basic", "role", "step", "fewshot"]
)

if st.button("生成策划案"):
    if theme =="":
        st.warning("⚠请输入活动主题")
    else:
        with st.spinner("AI正在生成策划案，请稍后..."):
            result = generate_plan(theme,type_,budget,prompt_type)
        st.success("策划案生成成功！")
    result = generate_plan(theme, type_, budget, prompt_type)

    st.markdown("## AI生成策划案")

    st.write(result)
    
    st.download_button(
        label="下载策划案",
        data=result,
        file_name="activity_plan.md",
        mime="test/markdown"
    )