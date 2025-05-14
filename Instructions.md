# Инструкции по запуску микросервиса

Каждая инструкция выполняется из директории репозитория deploy_price_predict_model

## 1. FastAPI микросервис в виртуальном окружение
```python
# команды создания виртуального окружения
# и установки необходимых библиотек в него

# команда перехода в директорию
cd services

# обновление локального индекса пакетов
sudo apt-get update
# установка расширения для виртуального пространства
sudo apt-get install python3.10-venv
# создание виртуального пространства
python3.10 -m venv .venv_sprint3 

source .venv_sprint3/bin/activate

pip install -r requirements.txt

# команда запуска сервиса с помощью uvicorn
uvicorn --app-dir=ml_service price_app:price_app --reload --port 8081 --host 0.0.0.0
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:8081/api/price/?flat_id=123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1, 
  "flat_id": 0, 
  "building_id": 6220, 
  "floor": 9, 
  "kitchen_area": 9.90, 
  "living_area": 19.900000, 
  "rooms": 1, 
  "is_apartment": false, 
  "studio": false, 
  "total_area": 35.099998, 
  "build_year": 1965, 
  "building_type_int": 6, 
  "latitude": 55.717113, 
  "longitude": 37.781120, 
  "ceiling_height": 2.64, 
  "flats_count": 84, 
  "floors_total": 12, 
  "has_elevator": true
}'
```

## 2. FastAPI микросервис в Docker-контейнере

```bash
# команда перехода в нужную директорию
cd services

# команда для создания образа
docker image build . -f Dockerfile_ml_service --tag price_prediction:v1

# команда для запуска контейнера
docker container run --publish 4601:8081 --env-file .env --volume=./models:/price_app/models price_prediction:v1
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:4601/api/price/?flat_id=123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1, 
  "flat_id": 0, 
  "building_id": 6220, 
  "floor": 9, 
  "kitchen_area": 9.90, 
  "living_area": 19.900000, 
  "rooms": 1, 
  "is_apartment": false, 
  "studio": false, 
  "total_area": 35.099998, 
  "build_year": 1965, 
  "building_type_int": 6, 
  "latitude": 55.717113, 
  "longitude": 37.781120, 
  "ceiling_height": 2.64, 
  "flats_count": 84, 
  "floors_total": 12, 
  "has_elevator": true
}'
```

## 3. Docker compose для микросервиса и системы моониторинга

```bash
# команда перехода в нужную директорию
cd services

# команда для запуска микросервиса в режиме docker compose
docker compose up --build
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:4601/api/price/?flat_id=123' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 1, 
  "flat_id": 0, 
  "building_id": 6220, 
  "floor": 9, 
  "kitchen_area": 9.90, 
  "living_area": 19.900000, 
  "rooms": 1, 
  "is_apartment": false, 
  "studio": false, 
  "total_area": 35.099998, 
  "build_year": 1965, 
  "building_type_int": 6, 
  "latitude": 55.717113, 
  "longitude": 37.781120, 
  "ceiling_height": 2.64, 
  "flats_count": 84, 
  "floors_total": 12, 
  "has_elevator": true
}'
```

## 4. Скрипт симуляции нагрузки
Скрипт генерирует 6 запросов в течение 130 секунд 

```
# команды необходимые для запуска скрипта
cd services

python3 test_requests.py
```

Адреса сервисов:
- микросервис: http://localhost:4601
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
