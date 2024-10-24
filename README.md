# Платформа для онлайн-обучения

## Сущности

- пользователь
- курс    
- занятие
- платеж

## Модели:
  - Пользователь:
      - все поля от обычного пользователя, но авторизацию заменить на email;
      - телефон;
      - город;
      - аватарка.

  - Курс:
      - название,
      - превью (картинка),
      - описание.
  - Урок:
      - название,
      - описание,
      - превью (картинка),
      - ссылка на видео.
  - Подписка:
    - FK на модель пользователя)
    - FK на модель курса
    
## Оснновные функции:
- реализовны CRUD для моделей курса и урока
- реализованы CRUD для пользователей, в том числе регистрацию пользователей, настроено использование JWT-авторизации. 
  Каждый эндпоинт, кроме авторизации и регистрации, закрыт для неавторизованных пользователей.
- для группы модераторов описаны права работы с любыми уроками и курсами, но без возможности их удалять и создавать новые. 
- права доступа для объектов описаны таким образом, чтобы пользователи, которые не входят в группу модераторов, могли видеть, редактировать и удалять только свои курсы и уроки
- для сохранения уроков и курсов реализована дополнительная проверку на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com
- реализован эндпоинт для установки подписки пользователя и на удаление подписки у пользователя.
- реализована пагинация для вывода всех уроков и курсов.
- настроен вывод документации для проекта. 
- реализована асинхронная рассылка писем пользователям об обновлении материалов курса. ( когда курс обновлен — тем, кто подписан на обновления именно этого курса, отправляется письмо на почту. )
- С помощью celery-beat реализована фоновая задача, которая проверяет пользователей по дате последнего входа по полю last_login и, если пользователь не заходил более месяца, блокирует его с помощью флага is_active

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

