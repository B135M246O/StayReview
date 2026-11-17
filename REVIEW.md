# StayReview — подготовлено к просмотру

Автор адаптации и доработок — Рябуха Олег.

## Исходники и объём работ

Изучены README, структура Django-приложений, DRF views/serializers/permissions,
модели пользователей, каталога, отзывов и комментариев, миграции, fixture,
OpenAPI, инфраструктурные тесты, Docker/nginx, обе копии workflow и MIT LICENSE.
Лицензия MIT и обязательное уведомление сохранены в LICENSE; сведения о лицензии — в NOTICE.md.

Домен каталога: типы размещения, особенности отдыха и объекты с годом открытия.
Внутренние `Title`, `Genre`, `titcatgen` и пути `titles`/`genres` сохранены, а их смысл описан в README/OpenAPI.
Пользовательские подписи, администрирование, примеры и fixture согласованы с этой предметной областью.
В demo fixture — три типа, три особенности и три вымышленных объекта; учётных записей,
хешей паролей, сессий и журнала администрирования в ней нет.

Сохранены регистрация/email-код/JWT, роли, оценки 1–10, один отзыв на автора и объект,
комментарии, фильтры и пагинация. Дополнительно исправлены обнаруженные дефекты:

- код подтверждения генерируется случайно для каждого пользователя вместо общего `XXXX`;
- права суперпользователя Django учитываются как административные;
- комментарии нельзя получить или создать через ID чужого объекта в URL;
- модельный валидатор действительно отклоняет оценки за пределами 1–10.

Три новые миграции обновляют доменные подписи и default кода подтверждения.
Исторические миграции не изменены. Идентификаторы пользователей сохранены AutoField,
согласованным с исходной миграцией.

Python 3.11 и совместимые зависимости установлены в отдельной `.venv`.
Старые серверные пути, пароль БД, wildcard hosts, DockerHub-образ, CI push/deploy/Telegram
удалены. Backend Docker собирается локально; CI выполняет проверки.
PostgreSQL остаётся основной конфигурацией, SQLite добавлена для изолированного локального запуска и тестов.
`.env.example` содержит только заглушки, README описывает настройку.

## Проверено 17 ноября 2026

Из корня StayReview:

| Команда / сценарий | Результат |
| --- | --- |
| `.\.venv\Scripts\python.exe -m pytest -q --tb=short` | **14 passed**, включая 9 API/fixture проверок и 5 инфраструктурных |
| `.\.venv\Scripts\python.exe api_yamdb\manage.py check --settings=api_yamdb.settings_test` | 0 issues |
| `.\.venv\Scripts\python.exe api_yamdb\manage.py makemigrations --check --dry-run --settings=api_yamdb.settings_test` | No changes detected |
| `.\.venv\Scripts\python.exe -m pip check` | No broken requirements found |
| `.\.venv\Scripts\python.exe -m compileall -q api_yamdb` | Успешно |
| `docker compose --env-file .env.example -f infra/docker-compose.yaml config --no-env-resolution --quiet` | Конфигурация корректна; daemon не нужен |
| `git diff --check` | Успешно |

API-тесты проверяют signup → письмо → JWT → профиль, защиту роли пользователя,
уникальные коды, фильтрацию каталога, создание объекта администратором и запрет будущего года,
отзывы/рейтинг/повторный отзыв, авторские и модераторские права, комментарии,
отрицательные и слишком большие оценки, согласованность вложенного URL и загрузку fixture.
Прежние тесты привязки к старому DockerHub, SSH-деплою и чужому бейджу заменены
проверками локальной сборки и отсутствия деплоя; бизнес-проверки не ослаблялись.

Отдельно на локальном SQLite выполнены реальные `migrate --noinput`, `loaddata fixtures.json`
(9 записей), `check` и запуск `runserver 127.0.0.1:8002 --noreload`.
HTTP 200 получены от `/api/v1/titles/` (3 объекта), `/redoc/`, `/static/redoc.yaml`.
Это настоящий HTTP-процесс, без имитации сети; после проверки сервер остановлен.
Локальная demo SQLite оставлена в игнорируемом `api_yamdb/db.sqlite3`.

## Запуск

Полная инструкция — README.md. После подготовки `.env`:

```powershell
.\.venv\Scripts\python.exe api_yamdb\manage.py migrate
.\.venv\Scripts\python.exe api_yamdb\manage.py loaddata fixtures.json
.\.venv\Scripts\python.exe api_yamdb\manage.py runserver 127.0.0.1:8002
```

Для SQLite задайте `DB_ENGINE=django.db.backends.sqlite3` и уберите `DB_NAME` из `.env`.
Для PostgreSQL подготовьте свою базу и заполните её параметры.

## Ограничения

PostgreSQL и контейнеры не запускались: в среде нет работающего Docker daemon.
Применение миграций и поведение ORM подтверждены на SQLite; PostgreSQL-специфические
особенности и Docker/nginx runtime требуют отдельной проверки.
Внешний SMTP не настроен: код использует штатный filebased backend, письма сохраняются локально.
ReDoc загружает JS с jsDelivr; сама YAML-спецификация доступна локально.
При `DEBUG=false` локальный runserver не раздаёт оформление админки; используйте Docker/nginx
или включите DEBUG для разработки.

Django 4.2.30 выбран как совместимая ступень для Python 3.11. Ветка 4.2 уже завершила
период поддержки; для публичного размещения потребуется отдельное обновление до поддерживаемой LTS.
В исторической миграции остаётся предупреждение о `django.utils.timezone.utc`,
важное для такого обновления; старая миграция сохранена.

 Вариант будущего сообщения:
`Adapt StayReview accommodation catalog, API examples and local setup`.
