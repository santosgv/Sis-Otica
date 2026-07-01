FROM python:3.11-slim

WORKDIR /app/Backend

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Instala dependências de sistema para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instala psycopg2 primeiro (para isolar erros)
RUN pip install --no-cache-dir psycopg2-binary && \
    pip install --no-cache-dir -r requirements.txt


COPY . /app

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]