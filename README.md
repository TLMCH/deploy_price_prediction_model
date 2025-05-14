# Вывод модели предсказания цен на недвижимость в продакшен.

Цели проекта:
1. Разработать FastAPI-микросервис.
2. Контейнеризовать его с помощью Docker.
3. Развернуть систему мониторинга, используя Prometheus и Grafana.
4. Разработать дашборд для мониторинга в Grafana.

Документация по проекту:
- Instructions.md - файл с инструкциями по запуску.
- Monitoring.md - файл с описанием метрик в Grafana.
- dashboard.png - изображение с готовым дашбордом в Grafana.

Вся логика проекта находится в директории services.

Структура проекта:
- ml_service/ - Основной код микросервиса
- - fast_api_handler.py - Обработчик запросов FastAPI
- - price_app.py - FastAPI-микросервис
- models/ - Папка с обученными моделями
- prometheus/ - Конфигурации мониторинга Prometheus
- - prometheus.yml - Конфигурационный файл Prometheus
- .env - Файл с переменными окружения. Оставлен намеренно (в нем хранятся порты для Docker).
- Dockerfile_ml_service- Dockerfile, в котором указаны инструкции для сборки образа FastAPI-микросервиса с ML-моделью.
- docker-compose.yaml- Docker Compose для запуска всех сервисов (ML-сервис, Prometheus и Grafana)
- requirements.txt - Список зависимостей Python
- test_requests.py - Скрипт для тестирования API-запросов
