from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import os

def main():
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
        ) # expires Apr 2, 2027

    prompt = "Explain what an SDK is in 3 sentences."
    temp = [0.2,1.0]

    for t in temp:
        response = client.responses.create(
            model="openrouter/free",
            temperature=t,
            instructions="You are a helpful assistant.",
            input=prompt,
        )

        print(f"=== Temperature {t} ===")
        print(response.output_text)
        print(f"\nTokens used: {response.usage.total_tokens}")

if __name__ == "__main__":
    main()