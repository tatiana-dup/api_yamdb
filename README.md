## Описание проекта:

Этот проект представляет собой API сервиса с различными произведениями, на которые пользователи могут оставлять отзывы.

## Документация API:
При локальном запуске проекта статическая документация для API доступна по адресу: http://127.0.0.1:8000/redoc/

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:tatiana-dup/api_final_yatube.git
```

```
cd api_final_yatube/
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source venv/Scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Примеры запросов:
### GET запрос для списка отзывов
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
В результате получим список всех отзывов с пагинацией

```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{}
]
}
```
### POST запрос для добавления нового отзыва
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
Запрос
```
{
  "text": "string",
  "score": 1
}
```

Ответ
```
{
  "text": "string",
  "score": 1
}
```

### GET запрос для получения отзыва по идентификатору
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
Ответ
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
### PATCH запрос для частичного обновления отзыва
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/

```
{
  "text": "string",
  "score": 1
}
```
### DELETE запрос для удаления отзыва
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
При удачном удалении вернет статус 204

### GET запрос для списка комментарией
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
В результате получим список всех комментариев с пагинацией
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
### POST запрос для добавления нового комментария
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

```
{
  "text": "string"
}
```

### GET запрос для получения комментария по идентификатору
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
### PATCH запрос для частичного обновления комментария
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

```
{
  "text": "string"
}
```
### DELETE запрос для удаления комментария
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
При удачном удалении вернет статус 204
---
Авторы проекта: