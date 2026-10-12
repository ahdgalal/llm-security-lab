# LLM Security Lab

[![CI](https://github.com/ahdgalal/llm-security-lab/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ahdgalal/llm-security-lab/actions/workflows/ci.yml)


A Python client for multiple LLM providers with a secure Docker setup and CI checks.


## Features

* Supports OpenAI and OpenRouter through one interface.
* Normalized results: reply text, model, token usage (including reasoning tokens), and latency.
* Provider chosen by an environment variable; results and settings are Pydantic models.
* Clear configuration errors with a non-zero exit code.


## Security

* Container runs as a non root user, with runtime dependencies only and no secrets
* CI scans the code (Bandit), dependencies (pip-audit), and the Dockerfile and image (Trivy)
* GitHub Actions pinned to commit SHAs, with a read only workflow token
* Dependabot opens weekly update PRs for actions and dependencies
* Scan results and triage decisions are documented in docs/security-scans.md


## Setup

Requirements:

* Python 3.12+
* `uv`
* API key for the provider you want to use

```bash
cp .env.example .env   # set PROVIDER and API key
uv run main.py
uv run pytest
```
Or with Docker:

```bash
docker build -t llm-security-lab .
docker run --rm --env-file .env llm-security-lab
```


## Testing

Tests use fake SDK clients, so they need no API keys or network. On every push and pull request, CI runs Ruff, pytest, the security scans, and checks on the built image.


## Findings

Detailed experiments and security research are kept separately so they are not lost when the README changes.

* [Temperature Experiment](docs/temperature-experiment.md)
* [Prompt Injection : OWASP LLM01:2026](docs/prompt-injection.md)
* [Provider comparison](docs/provider-comparison.md)
* [Security Scans](docs/security-scans.md)


## Project Structure

```text
.
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   └── dependabot.yml
├── docs/
│   ├── prompt-injection.md
│   ├── security-scans.md
│   └── temperature-experiment.md
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── main.py
├── test_main.py
├── pyproject.toml
├── uv.lock
└── README.md
```
