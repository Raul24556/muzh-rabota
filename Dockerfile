# Используем официальное минимальное изображение Python 3.12
FROM python:3.12.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (для сборки psycopg2, Pillow и других пакетов)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей и устанавливаем пакеты
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Настройки среды
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=voenkom.settings
ENV PORT=8000

# Собираем статику (если collectstatic не нужен на этапе сборки, можно закомментировать)
RUN python manage.py collectstatic --noinput || echo "collectstatic skipped"

# Открываем порт
EXPOSE 8000

# Команда запуска Gunicorn
CMD ["gunicorn", "voenkom.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "90"]
