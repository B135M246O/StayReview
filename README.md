# StayReview

Каталог отелей, гостевых домов и хостелов с оценками проживания, отзывами и комментариями.
Объекты классифицируются по типу размещения и особенностям отдыха: например, «у моря» или «для семьи».

Пользователи регистрируются по имени и email, получают код подтверждения и JWT.
Каждый пользователь может оставить один отзыв об объекте с оценкой от 1 до 10.
Гости читают каталог; авторы управляют своими отзывами и комментариями; модераторы — всеми отзывами и комментариями;
администраторы дополнительно управляют каталогом, классификациями и пользователями.

Стек: Python 3.11, Django 4.2, Django REST Framework, PostgreSQL, JWT, nginx и Docker.
Для локальной проверки также доступна SQLite. API не требует отдельного фронтенда.

## Локальный запуск в PowerShell

Из каталога StayReview:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r api_yamdb\requirements.txt
Copy-Item .env.example .env
```

Укажите в `.env` случайный `SECRET_KEY` и параметры своей PostgreSQL. База `stayreview` должна существовать.
Секрет можно получить командой `.\.venv\Scripts\python.exe -c "from secrets import token_urlsafe; print(token_urlsafe(48))"`.
Для запуска без PostgreSQL задайте в `.env` `DB_ENGINE=django.db.backends.sqlite3` и удалите строку `DB_NAME`.
SQLite использует локальный файл `api_yamdb/db.sqlite3`. Проверка автоматическими тестами не требует `.env`.

```powershell
.\.venv\Scripts\python.exe api_yamdb\manage.py migrate
.\.venv\Scripts\python.exe api_yamdb\manage.py loaddata fixtures.json
.\.venv\Scripts\python.exe api_yamdb\manage.py createsuperuser
.\.venv\Scripts\python.exe api_yamdb\manage.py runserver 127.0.0.1:8002
```

API: http://127.0.0.1:8002/api/v1/; спецификация: http://127.0.0.1:8002/redoc/;
администрирование: http://127.0.0.1:8002/admin/.
При локальном `DEBUG=false` статика админки не обслуживается runserver; для её оформления используйте Docker/nginx или временно `DEBUG=true`.
Письма с кодами сохраняются в `api_yamdb/sent_emails/`; внешняя почта не нужна.
Без постоянного `SECRET_KEY` сессии и JWT инвалидируются при перезапуске.

## Docker с PostgreSQL

Подготовьте `.env`, как выше. Из корня проекта:

```powershell
docker compose --env-file .env -f infra/docker-compose.yaml up -d --build
docker compose --env-file .env -f infra/docker-compose.yaml exec web python manage.py migrate
docker compose --env-file .env -f infra/docker-compose.yaml exec web python manage.py loaddata fixtures.json
docker compose --env-file .env -f infra/docker-compose.yaml exec web python manage.py collectstatic --noinput
docker compose --env-file .env -f infra/docker-compose.yaml exec web python manage.py createsuperuser
```

nginx слушает порт 8002. Backend собирается из текущего дерева; БД и файлы хранятся в именованных томах.

## API

Поля и пути API стабильны: `titles` — объекты размещения; `categories` — типы объектов;
`genres` / `genre` — особенности отдыха; `year` — год открытия объекта.
Основные маршруты:

- `POST /api/v1/auth/signup/` — `{"username":"traveller","email":"traveller@example.org"}`.
- `POST /api/v1/auth/token/` — `{"username":"traveller","confirmation_code":"код из письма"}`.
- `GET /api/v1/titles/?category=hotel&genre=family` — каталог с фильтрами.
- `POST /api/v1/titles/` — для администратора: `{"name":"Маяк","year":2014,"category":"hotel","genre":["seaside","family"],"description":"Отель у набережной"}`.
- `POST /api/v1/titles/1/reviews/` — `{"score":8,"text":"Тихие номера и удобное расположение"}`.
- `POST /api/v1/titles/1/reviews/1/comments/` — `{"text":"Спасибо за подробности"}`.
- `GET/PATCH /api/v1/users/me/` — собственный профиль.

Для авторизованных запросов передавайте заголовок `Authorization: Bearer <token>`.
Точные форматы и разрешённые методы приведены в `/redoc/`.
Демонстрационные названия объектов вымышлены; fixture не создаёт пользователей, паролей или сессий.

## Проверки

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe api_yamdb\manage.py check --settings=api_yamdb.settings_test
.\.venv\Scripts\python.exe api_yamdb\manage.py makemigrations --check --dry-run --settings=api_yamdb.settings_test
```

GitHub Actions выполняет только тесты и проверку миграций. Автоматической публикации образов или деплоя нет.
Результаты локальных проверок и ограничения перечислены в `REVIEW.md`.

Автор адаптации и доработок — Рябуха Олег.
Сведения о лицензии — в `NOTICE.md`; лицензия MIT и обязательное уведомление — в `LICENSE`.
