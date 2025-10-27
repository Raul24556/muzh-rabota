"""
extensions.py
Подключение и инициализация расширений проекта Django.
"""

import logging
from loguru import logger
from django.core.cache import cache
from django.conf import settings
from celery import Celery

# Настройка Loguru
logger.add(
    "logs/voenkom.log",
    rotation="5 MB",
    retention="10 days",
    level="INFO",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    enqueue=True
)

# Настройка стандартного логгера Django для совместимости
logging.basicConfig(level=logging.INFO)
django_logger = logging.getLogger("django")

# Настройка Celery
celery_app = Celery("voenkom")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()


def clear_cache():
    """Очищает весь кэш Django (например, при обновлении данных)."""
    try:
        cache.clear()
        logger.info("🧹 Кэш очищен успешно.")
    except Exception as e:
        logger.error(f"Ошибка очистки кэша: {e}")


def init_extensions():
    """Вызывается при старте приложения (например, в app_factory.py)."""
    logger.info("🚀 Инициализация расширений Django...")
    logger.info(f"DEBUG mode: {settings.DEBUG}")
    logger.info(
        f"Подключение к базе: {settings.DATABASES['default']['ENGINE']}"
    )
    logger.info(f"Кэш: {settings.CACHES['default']['BACKEND']}")
    logger.info("✅ Расширения успешно инициализированы.")
