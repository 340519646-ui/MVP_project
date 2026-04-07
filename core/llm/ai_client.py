from openai import OpenAI
import os
import time
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com"
)

def ask_ai(prompt, history=None,use_tools=False,retry=3):
    full_prompt = ""

    if history:
        for h in history:
            full_prompt += f"用户:{h['user']}\nAI:{h['ai']}\n"

    full_prompt += prompt
    for i in range(retry):

        try:

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "user", "content": prompt}
                ],
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
            
