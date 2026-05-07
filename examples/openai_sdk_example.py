from openai import OpenAI

client = OpenAI(api_key="mock-key", base_url="http://localhost:8000/v1")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "hello"}],
)

print(response.choices[0].message.content)
