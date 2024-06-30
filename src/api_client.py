import os
from openai import OpenAI

def call_openai_api(prompt):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o",
        max_tokens=1024,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
