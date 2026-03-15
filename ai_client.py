from openai import OpenAI
import os

client = OpenAI(
    api_key="sk-46456a2253e94a788323389f0b48abf5",
    base_url="https://api.deepseek.com"
)

def ask_ai(prompt):

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ],
        timeout=120
    )

    return response.choices[0].message.content