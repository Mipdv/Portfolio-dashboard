import os
from dotenv import load_dotenv
load_dotenv("tt.env")

from openai import OpenAI

client = OpenAI(api_key=os.environ["API_KEY"])

system_prompt = "You are a lawyer that is really interested in AI and Tech. You are also a rpg gamer."

user_prompt = input("So, tell me what do you thin about me, hehe\n")

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    model="gpt-4.1"
)

response_text = chat_completion.choices[0].message.content

print(response_text)

teste teste novo
sadsadasd aafasdgfasgsg