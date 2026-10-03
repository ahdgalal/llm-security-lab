from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = "Explain what an SDK is in 3 sentences."

response_low  = client.responses.create(
    model="gpt-4.1",
    temperature=0.2,
    instructions="You are a helpful assistant.",
    input=prompt,
)

response_high  = client.responses.create(
    model="gpt-4.1",
    temperature=1.0,
    instructions="You are a helpful assistant.",
    input=prompt,
)

print("=== Temperature 0.2 ===")
print(response_low.output_text)
print(f"\nTokens used: {response_low.usage.total_tokens}")

print("\n=== Temperature 1.0 ===")
print(response_high.output_text)
print(f"\nTokens used: {response_high.usage.total_tokens}")
