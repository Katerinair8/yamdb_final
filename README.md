# api_yamdb

api для проекта 
# YAMDB "Свободное слово"
 
Проект YaMDb собирает отзывы пользователей
на различные произведения.

# IP боевого сервера:
51.250.106.169

# Бэйдж, который показывает статус workflow:

![example workflow](https://github.com/katerinair8/yamdb_final/actions/workflows/yamdb_workflow/badge.svg?branch=master?event=push)

# Шаблон наполнения .env-файла:

Расположен в файле example.env в директории infra

# Как запустить приложения в контейнерах:

Развернуть проект через docker-compose:

```
docker-compose up -d
```

Выполнить миграции:

```
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

Собрать статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

### Использованные технологии:

Python 3.7
Django REST Framework 3.12
DRF Simple JWT 4.7

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Valllium/api_yamdb.git
```

```
cd  api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```
В зависимости от операционной системы
```
source venv/Scripts/activate или source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

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
### Эндпойнты:

AUTH


```
/api/v1/auth/signup/
Регистрация нового пользователя
Получение кода подтверждения на переданный email.

{
  "email": "string",
  "username": "string"
}

/api/v1/auth/token/
Получение JWT-токена в обмен на username и confirmation code.
{
  "username": "string",
  "confirmation_code": "string"
}

```
CATEGORIES
```
/api/v1/categories/
Получение списка всех категорий

Добавление новой категории.
Права доступа: Администратор.
{
  "name": "string",
  "slug": "string"
}

/api/v1/categories/{slug}/
Удаление категории по ее слагу.
Права доступа: Администратор.

```
GENRES
```
/api/v1/genres/
Получение списка всех жанров.

Добавление списка.
Права доступа: Администратор.
{
  "name": "string",
  "slug": "string"
}

/api/v1/genres/{slug}/
Удаление жанра по его слагу.
Права доступа: Администратор.
```
TITLES
``````
/api/v1/titles/
Получение списка всех произведений.

Добавление нового произведения.
Права доступа: Администратор.
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
  "string"
],
  "category": "string"
}

/api/v1/titles/{titles_id}/
Информация о произведении.

Частичное обновление информации о произведении.
Удаление произведения.
Права доступа: Администратор.

``````
REVIEWS

```
/api/v1/titles/{title_id}/reviews/
Получение списка всех отзывов.

Добавление нового отзыва.
Пользователь может оставить только один отзыв на произведение.
Права доступа: Аутентифицированные пользователи.
{
  "text": "string",
  "score": 1
}

/api/v1/titles/{title_id}/reviews/{review_id}/
Получение отзыва по id для указанного произведения.

Частичное обновление отзыва по id.
Удаление отзыва по id
Права доступа: Автор отзыва, модератор или администратор.
```
COMMENTS

```
/api/v1/titles/{title_id}/reviews/{review_id}/comments/
Получение списка всех комментариев к отзыву по id.

Добавление комментария к отзыву.
Права доступа: Аутентифицированные пользователи.
{
  "text": "string"
}

/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Получение комментария к отзыву по id.

Частичное обновление комментария к отзыву по id комментария.
Удаление комментария к отзыву по id комментария.
Права доступа: Автор комментария, модератор или администратор.
``````

USERS
```
/api/v1/users/
Получение списка всех пользователей
Права доступа: Администратор

Добавление пользователя
Права доступа: Администратор
Поля email и username должны быть уникальными.
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
} 
/api/v1/users/{username}/
Получение пользователя по username
Изменение данных пользователя по username
Удаление пользователя по username
Права доступа: Администратор

/api/v1/users/me/
Получить данные своей учетной записи
Изменить данные своей учетной записи
Права доступа: Любой авторизованный пользователь
``````
```
```

### Алгоритм регистрации пользователей:
```
1. Пользователь отправляет POST-запрос на добавление нового пользователя 
с параметрами email и username на эндпоинт /api/v1/auth/signup/.
2. YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
3. Пользователь отправляет POST-запрос с параметрами username и
confirmation_code на эндпоинт /api/v1/auth/token/,
 в ответе на запрос ему приходит token (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и
 заполняет поля в своём профайле (описание полей — в документации).
 Размещение, получение, редактирование постов
```


### Мы за яркие произведения и интересные мнения!