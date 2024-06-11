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

---
Авторы проекта: