# smartics_test

Cервис для учёта личных расходов, в котором пользователь
может записывать траты и относить их к определенным категориям.

## Скриншоты с резульатами работы:
[Тык](https://github.com/leoscrowi/smartics_test/docs/images)

# Запуск проекта:
- Создайте .env файл, или:
```bash
cp .env.example .env
```
- Соберите и запустите контейнер:
```bash
docker-compose up -d --build 
```
- API находится на http://localhost:8000/api/

# API
## CRUD категорий - пользователь может взаимодействовать только со своими категориями:
- GET /api/categories - список категорий пользователя
- POST /api/categories - создать категорию
- GET /api/categories/{id} - получить категорию
- PUT /api/categories/{id} - обновить категорию
- DELETE /api/categories/{id} - удалить категорию

## CRUD расходов - пользователь может взаимодействовать только со своими расходами: 
- GET /api/expenses - список расходов пользователя
    - поддерживает фильтрацию по диапазону дат, сумме и категориям (для
        реализации необходимо воспользоваться библиотекой django-filter)
- POST /api/expenses - создать расход
- GET /api/expenses/{id} - получить расход
- PUT /api/expenses/{id} - обновить расход
- DELETE /api/expenses/{id} - удалить расход

# Технологии, зависимости:
```
Django==4.1.7
djangorestframework==3.14.0
django-filter==23.2
psycopg2-binary==2.9.5
djangorestframework-simplejwt
```
