# Инструкции по запуску микросервиса

Каждая инструкция выполняется из директории репозитория mle-sprint3-completed
Если необходимо перейти в поддиректорию, напишите соотвесвтующую команду

## 1. FastAPI микросервис в виртуальном окружение
```python
# команды создания виртуального окружения
# и установки необходимых библиотек в него

# обновление локального индекса пакетов
sudo apt-get update
# установка расширения для виртуального пространства
sudo apt-get install python3.10-venv
# создание виртуального пространства
python3.10 -m venv .venv_sprint3 

source .venv_sprint3/bin/activate

pip install -r requirements.txt

# команда перехода в директорию
cd services

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

# команда для запуска микросервиса в режиме docker compose
```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:...' \
```

## 3. Docker compose для микросервиса и системы моониторинга

```bash
# команда перехода в нужную директорию

# команда для запуска микросервиса в режиме docker compose

```

### Пример curl-запроса к микросервису

```bash
curl -X 'POST' \
  'http://localhost:
```

## 4. Скрипт симуляции нагрузки
Скрипт генерирует <...> запросов в течение <...> секунд ...

```
# команды необходимые для запуска скрипта
...
```

Адреса сервисов:
- микросервис: http://localhost:<port>
- Prometheus: ...
- Grafana: ...