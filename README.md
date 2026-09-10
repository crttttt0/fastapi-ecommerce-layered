# FastAPI Ecommerce

Учебный интернет-магазин на FastAPI: категории, товары, отзывы,
JWT-аутентификация и роли пользователей (buyer / seller / admin).

## Стек
- FastAPI + Pydantic v2
- SQLAlchemy 2 (async) + asyncpg, PostgreSQL
- Alembic (миграции)
- JWT (PyJWT), хеширование паролей (pwdlib / argon2)
- uv (зависимости), Docker + Docker Compose

## Архитектура
Проект написан по слоистой архитектуре (layered architecture).
Здесь ответственность разделена по слоям:

```
app/
├── api/
│   └── v1/
│       ├── endpoints/        # HTTP-слой: роутеры по ресурсам
│       │   ├── categories.py
│       │   ├── products.py
│       │   ├── reviews.py
│       │   └── users.py
│       └── router.py         # сборка роутеров
├── core/                     # конфиг, безопасность, зависимости, исключения
│   ├── config.py
│   ├── dependencies.py
│   ├── enums.py
│   ├── exceptions.py
│   └── security.py
├── database/                 # подключение к БД и миграции
│   ├── base.py
│   ├── connection.py
│   ├── session.py
│   └── migrations/           # Alembic
├── models/                   # ORM-модели (SQLAlchemy)
│   ├── category.py
│   ├── product.py
│   ├── review.py
│   └── user.py
├── repositories/             # доступ к данным
│   ├── base.py
│   ├── category.py
│   ├── product.py
│   ├── review.py
│   └── user.py
├── schemas/                  # Pydantic-схемы запросов/ответов
│   ├── categories.py
│   ├── pagination.py
│   ├── products.py
│   ├── reviews.py
│   ├── tokens.py
│   └── users.py
├── services/                 # бизнес-логика и проверки
│   ├── category.py
│   ├── product.py
│   ├── review.py
│   └── user.py
└── main.py                   # точка входа, маппинг исключений в HTTP-статусы
```

Поток запроса: `endpoint – service – repository – БД`.
Ошибки бизнес-логики – доменные исключения из `app/core/exceptions.py`,
которые `app/main.py` превращает в HTTP-статусы.

## Настройка окружения
Скопируй шаблон и при необходимости поправь значения:
```bash
cp .env.example .env          # Linux/macOS
Copy-Item .env.example .env   # Windows (PowerShell)
```
Секретный ключ JWT сгенерируй свой:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Файл `.env` не коммитится (он в `.gitignore`).

## Запуск через Docker Compose
```bash
cp .env.example .env
docker compose up --build
```
- поднимаются приложение и PostgreSQL;
- миграции применяются автоматически (`entrypoint.sh` – `alembic upgrade head`);
- API: http://127.0.0.1:8000, Swagger UI: http://127.0.0.1:8000/docs

## Локальный запуск (без Docker)
```bash
cp .env.example .env
uv sync
just migrations-up
just run
```

Полезные команды (`justfile`):
```bash
just run                   # запустить uvicorn с --reload
just format                # ruff format + сортировка импортов
just migrations-new "msg"  # создать миграцию (autogenerate)
just migrations-up         # применить миграции (alembic upgrade head)
just migrations-down       # откатить последнюю миграцию
just migrations-history    # история миграций
just migrations-current    # текущая ревизия БД
```

## Эндпойнты (префикс `/api/v1`)

| Метод  | Путь                               | Доступ                     |
|--------|------------------------------------|----------------------------|
| POST   | `/users/`                          | всем                       |
| POST   | `/users/login`                     | всем                       |
| POST   | `/users/refresh`                   | всем (по refresh-токену)   |
| POST   | `/users/access`                    | всем (по refresh-токену)   |
| GET    | `/categories/`                     | всем                       |
| POST   | `/categories/`                     | `admin`                    |
| PUT    | `/categories/{category_id}`        | `admin`                    |
| DELETE | `/categories/{category_id}`        | `admin`                    |
| GET    | `/products/`                       | всем                       |
| GET    | `/products/category/{category_id}` | всем                       |
| GET    | `/products/{product_id}`           | всем                       |
| POST   | `/products/`                       | `seller`                   |
| PUT    | `/products/{product_id}`           | `seller` (владелец товара) |
| DELETE | `/products/{product_id}`           | `seller` (владелец товара) |
| GET    | `/reviews/`                        | всем                       |
| GET    | `/products/{product_id}/reviews/`  | всем                       |
| POST   | `/reviews/`                        | `buyer`                    |
| DELETE | `/reviews/{review_id}`             | автор отзыва или `admin`   |
