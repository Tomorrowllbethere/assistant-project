# Змінні (для зручності)
MANAGE = poetry run python core/manage.py

# Команда за замовчуванням (просто написати make)
all: up install migrate run

# Підняти базу в докері (в фоновому режимі)
db:
	docker-compose up -d db

# Встановити залежності через poetry
install:
	poetry install

# Застосувати міграції
migrate:
	$(MANAGE) migrate

# Запустити сервер розробки
run:
	$(MANAGE) runserver

# Зупинити все
stop:
	docker-compose stop

# Повна "реанімація" проєкту однією командою
up:
	docker-compose up -d
	poetry install
	$(MANAGE) migrate
	@echo "Вуаля! Все готово. Запускаю сервер..."
	$(MANAGE) runserver

# Створити нову міграцію (якщо змінила models.py)
mm:
	$(MANAGE) makemigrations

# Увійти в оболонку Django (Shell) - часто питають на співбесідах
shell:
	$(MANAGE) shell