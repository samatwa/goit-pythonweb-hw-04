# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.12
FROM python:3.12-slim

# Встановимо змінну середовища
ENV APP_HOME /app

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

# Встановимо залежності всередині контейнера
COPY requirements.txt .
RUN pip install -r requirements.txt

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .

# Запустимо наш застосунок всередині контейнера
ENTRYPOINT ["python", "main.py"]