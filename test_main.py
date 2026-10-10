from types import SimpleNamespace

import pytest

from main import LLMConfig, LLMResult, OpenAIProvider, OpenRouterProvider, get_provider


# fake OpenAI response
def fake_response():
    return SimpleNamespace(
        output_text="Hello from the fake model!",
        model="fake/model",
        usage=SimpleNamespace(
            input_tokens=10,
            output_tokens=5,
            output_tokens_details=SimpleNamespace(reasoning_tokens=2),
        ),
    )


class FakeResponses:
    def create(self, **kwargs):
        return fake_response()


class FakeClient:
    def __init__(self):
        self.responses = FakeResponses()


# Tests


def test_openai_provider_converts_response():
    provider = OpenAIProvider(client=FakeClient())

    result = provider.send(
        system_prompt="You are helpful.",
        user_message="Hello",
    )

    assert isinstance(result, LLMResult)
    assert result.text == "Hello from the fake model!"
    assert result.input_tokens == 10
    assert result.output_tokens == 5
    assert result.provider == "openai"
    assert result.model == "gpt-5-nano"
    assert result.latency >= 0


def test_openrouter_provider_converts_response():
    provider = OpenRouterProvider(client=FakeClient())

    result = provider.send(
        system_prompt="You are helpful.",
        user_message="Hello",
    )

    assert isinstance(result, LLMResult)
    assert result.text == "Hello from the fake model!"
    assert result.input_tokens == 10
    assert result.output_tokens == 5
    assert result.provider == "openrouter"
    assert result.model == "fake/model"
    assert result.latency >= 0


def test_missing_provider(monkeypatch):
    monkeypatch.delenv("PROVIDER", raising=False)

    with pytest.raises(ValueError, match="Unknown provider"):
        get_provider()


def test_unknown_provider(monkeypatch):
    monkeypatch.setenv("PROVIDER", "something_else")

    with pytest.raises(ValueError, match="Unknown provider"):
        get_provider()


# environment variable tests


def test_environment_selects_openai(monkeypatch):
    monkeypatch.setenv("PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    provider = get_provider()
    assert isinstance(provider, OpenAIProvider)


def test_environment_selects_openrouter(monkeypatch):
    monkeypatch.setenv("PROVIDER", "openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "fake-key")
    provider = get_provider()
    assert isinstance(provider, OpenRouterProvider)


# missing API key test


def test_missing_openai_api_key(monkeypatch):
    monkeypatch.setenv("PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="OPENAI_API_KEY is not set"):
        get_provider()


def test_missing_openrouter_api_key(monkeypatch):
    monkeypatch.setenv("PROVIDER", "openrouter")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    with pytest.raises(ValueError, match="OPENROUTER_API_KEY is not set"):
        get_provider()


# temperature tests


def test_temperature_valid():
    config = LLMConfig(temperature=0.5)
    assert config.temperature == 0.5


def test_temperature_too_low():
    with pytest.raises(ValueError):
        LLMConfig(temperature=-0.1)


def test_temperature_too_high():
    with pytest.raises(ValueError):
        LLMConfig(temperature=1.1)


def test_temperature_lower_boundary():
    config = LLMConfig(temperature=0)
    assert config.temperature == 0


def test_temperature_upper_boundary():
    config = LLMConfig(temperature=1)
    assert config.temperature == 1
