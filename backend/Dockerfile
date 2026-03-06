FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md ./
COPY aisubs ./aisubs
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -e .

EXPOSE 8099
CMD ["ai-subs", "serve", "--host", "0.0.0.0", "--port", "8099"]
