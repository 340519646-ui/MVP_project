from openai import OpenAI
import os
import time
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)



def ask_ai(prompt, history=None,mode="generate",max_history=5,retry=3):
    """
    :param prompt:当前用户输入问题
    :param history:[{"user":"...","ai":"..."}]
    :param retry:重复次数
    :param max_history:可保留最大历史
    """
    
    messages=[]
    
    if mode == "optimize":
        messages.append({
            "role": "system",
            "content": "你是校园活动策划专家，负责基于已有方案进行优化。"
        })
    else:
        messages.append({
            "role": "system",
            "content": "你是校园活动策划专家，负责生成结构完整、可执行的校园活动策划案。"
        })
    

    if history:
        history = history[-max_history:]
        
        for h in history:
            messages.append({
                "role": "user",
                "content": h["user"]
            })
            if h.get("ai"):
                messages.append({
                    "role": "assistant",
                    "content": h["ai"]
                })
    messages.append({"role": "user", "content": prompt})

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
            
