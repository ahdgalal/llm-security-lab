# LLM Security Lab

A small Python project that provides one interface for working with multiple LLM providers. It uses the OpenAI SDK, Pydantic, and pytest.


## What it does

* Supports OpenAI and OpenRouter through a shared `LLMProvider` interface.
* Converts provider responses into a common `LLMResult`.
* Tracks input tokens, output tokens, reasoning tokens, and latency.
* Selects the provider through `.env`.
* Uses fake SDK clients for tests, so tests do not make real API calls.
* Validates configuration and temperature values.

## Setup

Requirements:

* Python 3.12+
* `uv`
* API key for the provider you want to use

Copy `.env.example` to `.env` and add your API keys:

```env
PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Run the project:

```bash
uv run main.py
```

Run tests:

```bash
uv run pytest
```

## Providers

### OpenAI

Uses the OpenAI Responses API with `gpt-5-nano`.

### OpenRouter

Uses OpenRouter through the OpenAI SDK and can route requests to different models. For reproducible evaluations, a specific model should be pinned instead of using `openrouter/free`.

## Testing

Tests cover:

* Provider response conversion
* Provider selection
* Missing and unknown providers
* Missing API keys
* Temperature validation and boundaries
* Latency
* Provider response metadata

## Findings

Detailed experiments and security research are kept separately so they are not lost when the README changes.

* [Temperature Experiment](docs/temperature-experiment.md)
* [Prompt Injection — OWASP LLM01:2026](docs/prompt-injection.md)

## Project Structure

```text
.
├── main.py
├── tests/
├── docs/
│   ├── prompt-injection.md
│   └── temperature-experiment.md
├── .env.example
├── pyproject.toml
└── README.md
```
