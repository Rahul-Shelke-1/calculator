FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip \
  && pip install --no-cache-dir uv \
  && uv sync --frozen --no-dev

EXPOSE 8080

CMD ["uv", "run", "python", "app.py"]