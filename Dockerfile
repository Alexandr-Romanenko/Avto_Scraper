FROM python:3.12.2-slim

# Отключаем создание .pyc и буферизацию stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем системные зависимости для сборки C-пакетов
RUN apt-get update && apt-get install -y \
    build-essential \
    postgresql-client-15 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Создаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# По умолчанию запускаем Uvicorn
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]