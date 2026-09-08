FROM python:3.13.7-slim as builder

WORKDIR /app

COPY docker_requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r docker_requirements.txt


FROM python:3.13.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY --from=builder /install /urc/local

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]