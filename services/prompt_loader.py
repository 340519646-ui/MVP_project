from core.llm.ai_client import ask_ai
from jinja2 import Template
import os
def render_prompt(filename,data) -> str:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    full_path = os.path.join(base_dir, "prompts", filename)
    with open(full_path, "r", encoding="utf-8") as f:
        template_str = f.read()

    template = Template(template_str)
    return template.render(**data)

def compress_docs(docs:list[str]) ->str :
    """将RAG检索结果压缩成结构化摘要"""
    content = "\n".join(docs)

    prompt = f"""
你是活动策划分析专家，请将以下案例提炼为结构化要点：

要求：
1. 不超过200字
2. 用简洁条目表达
3. 保留：活动形式 / 亮点 / 预算策略

案例：
{content}

输出示例：
- 活动形式：
- 核心亮点：
- 预算策略：
"""

    summary = ask_ai(prompt)
    return summary.strip()