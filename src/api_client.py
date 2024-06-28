import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def call_openai_api(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant that helps generate code patches."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message['content'].strip()

