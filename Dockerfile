# 1. Беремо офіційний легкий образ Python
FROM python:3.12-slim

# 2. Встановлюємо системні залежності для PostgreSQL та Make
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    make \
    && rm -rf /var/lib/apt/lists/*

# 3. Встановлюємо Poetry
RUN pip install poetry

# 4. Встановлюємо робочу директорію
WORKDIR /app

# 5. Копіюємо файли залежностей (це важливо для кешування)
COPY . . 

# 6. Вимикаємо створення віртуальних середовищ всередині контейнера
# (контейнер сам по собі вже є ізольованим середовищем)
# 6. Налаштування Poetry та інсталяція в один рядок
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# 7. Копіюємо решту коду
COPY . .

# 8. Відкриваємо порт
EXPOSE 8000

# 9. Команда для запуску (може бути перезаписана в docker-compose)
CMD ["python", "core/manage.py", "runserver", "0.0.0.0:8000"]