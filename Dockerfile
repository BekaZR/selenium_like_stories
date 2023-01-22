FROM python:3.10-slim as builder
WORKDIR /app
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
ENV PATH=$PATH:/etc/poetry/bin
COPY ./pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.in-project true
RUN poetry install

FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH=$PYTHONPATH:/app/ PATH=/app/.venv/bin:$PATH
COPY --from=builder /app/.venv .venv
COPY . .
ENTRYPOINT ["python3", "main.py"]
