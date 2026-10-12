FROM python:3.12-slim

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /uvx /bin/

RUN useradd --create-home --uid 10001 appuser && mkdir /app && chown appuser:appuser /app

WORKDIR /app

COPY --chown=appuser:appuser pyproject.toml uv.lock ./

USER appuser

RUN uv sync --locked --no-dev

COPY --chown=appuser:appuser main.py ./

CMD ["uv", "run", "--no-sync", "main.py"]