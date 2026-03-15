from ai_client import ask_ai

print("====== AI活动策划生成器 ======")

theme = input("活动主题：")
people = input("参与人数：")
budget = input("预算：")

# 读取prompt模板
with open("prompts/planner.txt", "r") as f:
    template = f.read()

prompt = template.format(
    theme=theme,
    people=people,
    budget=budget
)

print("\nAI生成中...\n")

result = ask_ai(prompt)

print(result)

# 保存文件
with open("output/plan.md", "w") as f:
    f.write(result)

print("\n策划已保存到 output/plan.md")