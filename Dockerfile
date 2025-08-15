FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Системные зависимости для сборки и psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc \
 && rm -rf /var/lib/apt/lists/*

# Установка питон-зависимостей
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Копируем код
COPY . /app

EXPOSE 8000

# Команду запуска задаём в docker-compose
