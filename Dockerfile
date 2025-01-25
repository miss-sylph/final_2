# Базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы
COPY app/requirements.txt requirements.txt
COPY app/app.py app.py

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запуск приложения
CMD ["python", "app.py"]

