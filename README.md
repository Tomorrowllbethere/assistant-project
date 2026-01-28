# assistyou
it is a personnal assistant for shedules
## 🛠 Стек технологій
* **Backend:** Python 3.10+, Django 4.x
* **Package Manager:** Poetry
* **Database:** PostgreSQL (Docker)
* **Automation:** Makefile

---

## ⚡ Швидкий запуск (Quick Start)

1. Вхід у проєкт
git checkout dev-branch  # Переходимо в робочу гілку
git pull origin main     # Забираємо оновлення з основної гілки (щоб не було конфліктів)
make up                  # Запуск Docker (БД) + Poetry (Install) + Server

2. Активна розробка
poetry add <назва>       # Додати пакет
make install             # Оновити оточення


            Якщо змінила models.py:

make mm                  # Створити файл міграції (makemigrations)
make migrate             # Прийняти зміни в базу (migrate)

3. Збереження та Пуш (Commit & Push)

git add .                # Додати всі зміни до черги
git commit -m "Опис"     # Зафіксувати зміни з коротким коментарем
git push                 # Відправити код на GitHub у гілку dev-branch

4. Злиття (На GitHub)
5. Вихід (Завершення дня)

make stop                # Зупинити базу (Docker) та звільнити оперативну пам'ять
