# drf-lms

## Платформа для онлайн-обучения

## Сущности

- пользователь
- курс    
- занятие
- платеж

## Запуск через docker-compose
1. Заполнить файл `.env` с переменными окружения
2. Выполнить 
```commandline
    docker compose up --build
```
3. Сервис будет доступен по адресу: http://0.0.0.0:8000/

## Установка и использование (локально)

Для работы программы необходимо:

1. установить зависимости, указанные в файле  pyproject.toml:
- для первичной установки:

  ```poetry install```
- для обновления:

  ```poetry update```


2. создать файл `.env` с параметрами доступа к базе данных PostgresSQL и запуска сервера django.
Пример содержимого файла:

```
POSTGRES_HOST=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432
POSTGRES_DB=postgres

DJANGO_DEBUG=True
DJANGO_SECRET_KEY=your_secret_key

STRIPE_API_KEY=your_stripe_api_key
```
3. выполнить миграции командой
```commandline
python3 ./manage.py migrate
```

4. запустить сервер:
```commandline
python3 ./manage.py runserver
```

## Создание суперпользователя:
```commandline
        python manage.py createadmin --email admin@example.com --password admin
```

## Наполнение БД:
```commandline
        python manage.py loaddata --exclude auth.permission --exclude contenttypes ./fixtures/data.json
```

## Проверка степени покрытия тестами (linux):
```commandline
        coverage run --source='.' manage.py test 
        coverage report  --omit='migrations'
```

