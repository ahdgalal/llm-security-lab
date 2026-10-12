import os
import sys
import time
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


# same result format for every provider
class LLMResult(BaseModel):
    text: str
    input_tokens: int
    output_tokens: int
    provider: str
    model: str
    latency: float
    reasoning_tokens: int


class LLMConfig(BaseModel):
    temperature: float = Field(ge=0, le=1)


# shared interface
class LLMProvider(ABC):
    @abstractmethod
    def send(self, system_prompt: str, user_message: str) -> LLMResult:
        pass


class OpenAIProvider(LLMProvider):
    def __init__(self, client=None, model: str = "gpt-5-nano"):

        if client is None:
            api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                raise ValueError("OPENAI_API_KEY is not set")

            client = OpenAI(api_key=api_key)

        self.client = client
        self.model = model

    def send(self, system_prompt: str, user_message: str) -> LLMResult:

        start = time.perf_counter()

        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=user_message,
        )

        latency = time.perf_counter() - start

        return LLMResult(
            text=response.output_text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            provider="openai",
            model=self.model,
            latency=latency,
            reasoning_tokens=response.usage.output_tokens_details.reasoning_tokens,
        )


class OpenRouterProvider(LLMProvider):
    def __init__(self, client=None, model: str = "openrouter/free", temperature=0.7):

        if client is None:
            api_key = os.getenv("OPENROUTER_API_KEY")

            if not api_key:
                raise ValueError("OPENROUTER_API_KEY is not set")

            client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

        self.client = client
        self.config = LLMConfig(temperature=temperature)
        self.model = model

    def send(self, system_prompt: str, user_message: str) -> LLMResult:

        start = time.perf_counter()

        response = self.client.responses.create(
            model=self.model,
            temperature=self.config.temperature,
            instructions=system_prompt,
            input=user_message,
        )

        latency = time.perf_counter() - start

        return LLMResult(
            text=response.output_text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            provider="openrouter",
            model=response.model,
            latency=latency,
            reasoning_tokens=response.usage.output_tokens_details.reasoning_tokens,
        )


def get_provider() -> LLMProvider:

    provider = os.getenv("PROVIDER")

    if provider == "openrouter":
        return OpenRouterProvider()

    elif provider == "openai":
        return OpenAIProvider()

    raise ValueError(f"Unknown provider: {provider}")


def main():
    load_dotenv()

    try:
        provider = get_provider()

    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        sys.exit(1)

    result = provider.send(
        system_prompt="You are a helpful assistant.",
        user_message="Explain embeddings in one simple paragraph.",
    )

    print("Reply")
    print("--------------")
    print(result.text)

    print("\nMetadata:")
    print("- Provider:", result.provider)
    print("- Model:", result.model)
    print("- Latency:", result.latency, "seconds")

    print("- Input tokens:", result.input_tokens)
    print("- Output tokens:", result.output_tokens)
    print("- Reasoning tokens:", result.reasoning_tokens)


if __name__ == "__main__":
    main()
