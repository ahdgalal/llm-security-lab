
FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev

COPY main.py ./

CMD ["uv", "run", "--no-sync", "main.py"]