# LLM Security Lab

A small Python project for working with multiple LLM providers through one shared interface. It uses the OpenAI SDK, Pydantic, and pytest.

## What it does

* Supports OpenAI and a second provider.
* Uses one shared `LLMProvider` interface.
* Sends a system prompt and user message.
* Returns a common `LLMResult`.
* Tracks input and output tokens.
* Allows switching providers using `.env`.
* Tests provider behavior using fake SDK clients.

## Setup

Create a `.env` file:

```env
PROVIDER=openai

OPENAI_API_KEY=your_openai_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Add `.env` to `.gitignore`:

```text
.env
```

### Requirements

* Python 3.12+
* `uv`
* API key for the provider you want to use

## Providers

### OpenAI

Uses the OpenAI SDK with the Responses API.

Default model:

```text
gpt-5-nano
```

### OpenRouter

OpenRouter is used as the second provider because it provides access to multiple models and has a free option for experimentation.

OpenRouter is **not required by the project design**. It can be replaced with another provider as long as the new provider implements the same `LLMProvider` interface.

## Switching Providers

Change `PROVIDER` in `.env`:

```env
PROVIDER=openai
```

or:

```env
PROVIDER=openrouter
```

The rest of the application does not need to change.

## Shared Interface

Both providers use:

```python
class LLMProvider(ABC):

    @abstractmethod
    def send(self, system_prompt: str, user_message: str) -> LLMResult:
        pass
```

Provider responses are converted into:

```python
class LLMResult(BaseModel):
    text: str
    input_tokens: int
    output_tokens: int
    provider: str
    model: str
```

## Temperature

Temperature was validated with Pydantic using the range:

```text
0 <= temperature <= 1
```

Invalid values are rejected before an API call.

During testing, OpenAI returned an error because the model does not support the temperature parameter. I removed it from the OpenAI API call and the related API tests.

This showed that different providers/models can support different API parameters.

## Testing

The project uses pytest.

Run the tests:

```bash
uv run pytest
```

Tests cover:

* Provider response conversion
* Provider selection
* Missing API keys
* Temperature validation
* Temperature boundaries

Fake SDK clients are used so provider tests do not make real API calls.

## Provider Comparison

The same prompt was sent to each provider three times.

**Prompt:**

```text
You are a helpful assistant.

Explain embeddings in one simple paragraph.
```

| Provider   | Run | Reply                                                                        | Input Tokens | Output Tokens |
| ---------- | --: | ---------------------------------------------------------------------------- | -----------: | ------------: |
| OpenAI     |   1 | An embedding is a way to represent objects as fixed-length vectors...        |           23 |           817 |
| OpenAI     |   2 | An embedding is a way to turn items into a compact set of numbers...         |           23 |           578 |
| OpenAI     |   3 | Embeddings are a way to turn objects into fixed-length vectors...            |           23 |           926 |
| OpenRouter |   1 | An embedding is a way of turning data into a fixed-length list of numbers... |           31 |           105 |
| OpenRouter |   2 | Embeddings are numerical vector representations of objects...                |           31 |           138 |
| OpenRouter |   3 | `User Safety: safe`                                                          |          469 |            86 |

*Replies are shortened for readability.*

The providers gave different responses and used different numbers of tokens. OpenRouter also returned `User Safety: safe` on the third run instead of answering the question.

## Running

Set the provider in `.env`, then run:

```bash
uv run main.py
```

## Future Work

* Add more LLM providers.
* Explore LLM security risks.
* **v2.0:** Work on **LLM01:2025 Prompt Injection** from the OWASP Top 10 for LLM Applications.
