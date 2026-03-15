from openai import OpenAI
import os
import time

client = OpenAI(
    api_key="sk-46456a2253e94a788323389f0b48abf5",
    base_url="https://api.deepseek.com"
)

def ask_ai(prompt, retry=3):

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