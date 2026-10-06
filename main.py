from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import os
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod

# same result format for every provider
class LLMResult(BaseModel):
    text: str
    input_tokens: int
    output_tokens: int
    provider: str
    model: str

class LLMConfig(BaseModel):
    temperature: float = Field(ge=0, le=1)

# shared interface 
class LLMProvider(ABC): 
    @abstractmethod 
    def send(self, system_prompt: str, user_message: str) -> LLMResult: 
        pass

class OpenAIProvider(LLMProvider):

    def __init__(self, client=None, model:str="gpt-5-nano", temperature=0.7): # can change model

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")
        
        if client is None:
            client = OpenAI(api_key=api_key)

        self.client = client
        # self.config = LLMConfig(temperature=temperature)
        self.model=model

    def send(self, system_prompt: str, user_message: str) -> LLMResult:
            response = self.client.responses.create( 
                model=self.model, 
                #temperature=self.config.temperature,
                instructions=system_prompt, 
                input=user_message, 
            )

            return LLMResult( 
                text=response.output_text, 
                input_tokens=response.usage.input_tokens, 
                output_tokens=response.usage.output_tokens, 
                provider="openai", 
                model=self.model, 
            )

class Provider(LLMProvider):

    def __init__(self, client=None, model:str="openrouter/free", temperature=0.7): # can change model
        
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is not set")
        
        if client is None:
            client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key
                    ) # expires Apr 2, 2027

        self.client = client
        self.config = LLMConfig(temperature=temperature)
        self.model=model

    def send(self, system_prompt: str, user_message: str) -> LLMResult:
            response = self.client.responses.create( 
                model=self.model, 
                temperature=self.config.temperature,
                instructions=system_prompt, 
                input=user_message, 
            )

            return LLMResult( 
                text=response.output_text, 
                input_tokens=response.usage.input_tokens, 
                output_tokens=response.usage.output_tokens, 
                provider="openrouter", 
                model=self.model, 
            )

def get_provider() -> LLMProvider:

    provider = os.getenv("PROVIDER")

    if provider == "openrouter":
        return Provider()

    elif provider == "openai":
        return OpenAIProvider()

    raise ValueError(f"Unknown provider: {provider}")

def main():

    provider = get_provider()

    result = provider.send( 
        system_prompt="You are a helpful assistant.", 
        user_message="Explain embeddings in one simple paragraph.", 
    )

    print("Reply") 
    print("--------------") 
    print(result.text) 
    
    print("\nMetadata:") 
    print("- Input tokens:", result.input_tokens) 
    print("- Output tokens:", result.output_tokens) 
    print("- Provider:", result.provider) 
    print("- Model:", result.model)

if __name__ == "__main__":
    main()