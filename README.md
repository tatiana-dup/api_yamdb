## Описание проекта:

Этот проект представляет собой API сервиса с различными произведениями, на которые авторизованные пользователи могут оставлять отзывы и выставлять рейтинг от 1 до 10, а также комментировать отзывы других пользователей, удалять свои отзывы и комментарии. Произведения могут относится к разным категориям и жанрам. Как авторизованные, так и неавторизованные пользователи могут просматривать информацию о произведениях, отзывы и комментырии к ним, а также жанры и категории. Авторизованные пользователи могут просматривать и изменять информацию о себе.
У всех пользователей есть роли, помимо обычного пользователя на сервисе есть модераторы и администраторы. Модераторы могут удалять любые отзывы и комментарии к ним. Администраторы могут добавлять новых пользователей, изменять их данные, просматривать информацию о всех пользователях сервиса. Администраторы могут добавлять новые произведения, категории и жанры, изменять и удалять их.
Для регистрации пользователю необходимо указать емейл и придумать юзернейм, в ответ ему на почту придет код подтверждения, используя который он сможет получить токен для аутентификации.

В проекте использованы: Python3.9, Django, Django REST Framework, SQLite3. Генерация кодов подтверждения настроена при помощи PyJWT, аутентификация пользователей настроена по JWT-токену.


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

### GET запрос для списка  категория
http://127.0.0.1:8000/api/v1/categories/
В результате получим список всех категорий с пагинацией

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ]
}
```

### POST запрос для добавления новой категории
http://127.0.0.1:8000/api/v1/categories/

Формат запроса/ответа
```
{
  "name": "string",
  "slug": "^-$"
}
```

### DELETE запрос для удаления категории
http://127.0.0.1:8000/api/v1/categories/{slug}/
При удачном удалении вернет статус 204

### GET запрос для списка  жанров
http://127.0.0.1:8000/api/v1/genres/
В результате получим список всех жанров с пагинацией

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ]
}
```

### POST запрос для добавления нового жанра
http://127.0.0.1:8000/api/v1/genres/

Формат запроса/ответа
```
{
  "name": "string",
  "slug": "^-$"
}
```

### DELETE запрос для удаления жанра
http://127.0.0.1:8000/api/v1/genres/{slug}/
При удачном удалении вернет статус 204

### GET запрос для списка произведений
http://127.0.0.1:8000/api/v1/titles/
В результате получим список всех произведений с пагинацией

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

### POST запрос для добавления нового произведения
http://127.0.0.1:8000/api/v1/titles/

Формат запроса/ответа
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

### GET запрос для получения произведения по идентификатору
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
Ответ
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ],
  "category": {
    "name": "string",
    "slug": "^-$"
  }
}
```

### PATCH запрос для частичного обновления произведения
http://127.0.0.1:8000/api/v1/titles/{titles_id}/

```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

### DELETE запрос для удаления произведения
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
При удачном удалении вернет статус 204

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

### GET запрос для списка комментариев
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

### Регистрация нового пользователя и/или получение кода подтверждения:
```
POST /api/v1/auth/signup/
Content-Type: application/json
{
"email": "user@example.com",
"username": "^w\\Z"
}
```

### Получение токена:
```
POST /api/v1/auth/token/
Content-Type: application/json
{
"username": "^w\\Z",
"confirmation_code": "string"
}
```

### Получение токена:
```
POST /api/v1/auth/token/
Content-Type: application/json
{
"username": "^w\\Z",
"confirmation_code": "string"
}
```

### Получение списка всех пользователей администратором:
```
GET /api/v1/users/
```

### Добавление пользователя администратором:
```
POST /api/v1/users/
Content-Type: application/json
{
"username": "^w\\Z",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```

### Получение пользователя:
```
GET /api/v1/users/{username}/
```

---
Авторы проекта:
[Бахтияр Каюпов](https://github.com/Prospero6666)
[Михаил Игнатенко](https://github.com/Mig239116)
[Татьяна Дуплинская](https://github.com/tatiana-dup)
