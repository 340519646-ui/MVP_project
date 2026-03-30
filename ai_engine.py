def generate_plan(user_input, mode="basic"):

    if mode == "basic":
        prompt = f"请设计一个活动：{user_input}"

    elif mode == "role":
        prompt = f"你是一名校园活动专家，请设计：{user_input}"

    elif mode == "step":
        prompt = f"请一步一步设计活动方案：{user_input}"

    elif mode == "fewshot":
        with open("prompt_templates/fewshot_prompt.txt", "r", encoding="utf-8") as f:
            template = f.read()
        prompt = template.replace("{input}", user_input)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content