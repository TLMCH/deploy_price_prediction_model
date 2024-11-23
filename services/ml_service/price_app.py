"""FastAPI-приложение для предсказания цены квартиры."""

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, Counter
import numpy as np
from fast_api_handler import FastApiHandler

"""
Пример запуска из директории mle-project-sprint-3-v001/services/ml_service:
uvicorn --app-dir=ml_service price_app:price_app --reload --port 8081 --host 0.0.0.0

Для просмотра документации API и совершения тестовых запросов зайти на  http://127.0.0.1:8081/docs

Если используется другой порт, то заменить 8081 на этот порт
"""

# создаём приложение FastAPI
price_app = FastAPI()

# инициализируем и запускаем экпортёр метрик
instrumentator = Instrumentator()
instrumentator.instrument(price_app).expose(price_app)

# создаём обработчик запросов для API
price_app.handler = FastApiHandler()

price_app_predictions = Histogram(
    # имя метрики
    "price_app_predictions",
    # описание метрики
    "Histogram of predictions",
    # указываем корзины для гистограммы
    buckets=(6_000_000, 7_000_000, 8_000_000, 9_000_000, 10_000_000)
)

price_app_count = Counter(
    "price_app_count",
    "Count of predictions"
)

@price_app.post("/api/price/") 
def get_prediction_for_item(flat_id: str, model_params: dict):
    """Функция для получения предсказания цены квартиры.

    Args:
        flat_id (str): Идентификатор квартиры.
        model_params (dict): Параметры квартиры, которые нужно передать в модель.

    Returns:
        dict: Предсказание цены квартиры.
    """
    all_params = {
        "flat_id": flat_id,
        "model_params": model_params
    }
    response = price_app.handler.handle(all_params)
    price_app_predictions.observe(response["prediction"])
    price_app_count.inc()
    return response