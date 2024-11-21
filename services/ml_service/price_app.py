"""FastAPI-приложение для предсказания цены квартиры."""

from fastapi import FastAPI, Body
from fast_api_handler import FastApiHandler

"""
Пример запуска из директории mle-project-sprint-3-v001/services/ml_service:
uvicorn --app-dir=ml_service price_app:price_app --reload --port 8081 --host 0.0.0.0

Для просмотра документации API и совершения тестовых запросов зайти на  http://127.0.0.1:8081/docs

Если используется другой порт, то заменить 8081 на этот порт
"""

# создаём приложение FastAPI
price_app = FastAPI()

# создаём обработчик запросов для API
price_app.handler = FastApiHandler()

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
    return price_app.handler.handle(all_params)