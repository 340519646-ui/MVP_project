from openai import OpenAI
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com"
)

def ask_ai(prompt, history=None,max_history=5,retry=3):
    """
    :param prompt:当前用户输入问题
    :param history:[{"user":"...","ai":"..."}]
    :param retry:重复次数
    :param max_history:可保留最大历史
    """
    
    messages=[]
    
    messages.append({
        "role":"system",
        "content":"你是校园活动策划专家，负责优化已有方案"#保留接口，可以改变ai回答模式
        })
    

    if history:
        history = history[-max_history:]
        
        for h in history:
            messages.append({
                "role": "user",
                "content": h["user"]
            })
            if h["ai"]:
                messages.append({
                    "role": "assistant",
                    "content": h["ai"]
                })
    messages.append({
    "role": "user",
    "content": f"""
请优化当前校园活动策划方案：

要求{prompt}

用户最新修改要求已在对话历史中，请基于历史进行优化。
"""
})

    for i in range(retry):

        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                timeout=120
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"AI请求失败: {e}")

            if i < retry - 1:
                print("正在重试...\n")
                time.sleep(3)
            else:
                return "AI请求失败，请稍后再试"
            
