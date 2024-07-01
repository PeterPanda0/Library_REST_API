# Проект Library

## Описание проекта
Проект "Library" представляет собой RESTful API для управления книгами, авторами и жанрами. Он включает в себя базовый CRUD функционал для книг, авторов и жанров, а также дополнительный функционал для работы с поставками книг и статистикой.

## Установка и запуск
### Для установки и запуска проекта выполните следующие шаги:
1. Клонируйте репозиторий с проектом.(ссылка)

2. Разверните и активируйте виртуальное окружение, установите зависимости.

3. Создайте файлы .env и env.docker в корневой папке проекта и добавьте свои переменные для работы с PostgreSQL и с Docker. Смотрите env и env.docker для получения дополнительной информации. 

4. Установите Docker (если не установлен).

5. В корневой директории проекта выполните команду:
```
docker-compose up --build
```

6. После успешного запуска, проект будет доступен по адресу:

```
http://0.0.0.0:8000/
```

7. Для доступа к Swagger UI перейдите по ссылке:
bash
```
http://0.0.0.0:8000/swagger/
```


## API Endpoints
Проект предоставляет следующие API endpoint'ы:

### Книги
| HTTP | Endpoints | Action |
| --- | --- | --- |
| GET | /api/books/ | получение списка всех книг с пагинацией.
| GET | /api/books/{book_id}/ | получение информации о конкретной книге.
| POST | /api/books/ | создание новой книги.
| PUT | /api/books/{book_id}/ | изменение информации о книге.
| DELETE | /api/books/{book_id}/ | удаление книги.

### Авторы
| HTTP | Endpoints | Action |
| --- | --- | --- |
| GET | /api/authors/ | получение списка всех авторов с пагинацией.
| GET | /api/authors/{author_id}/ | получение информации об авторе и его книгах.
| POST | /api/authors/ | создание нового автора.
| PUT | /api/authors/{author_id}/ | изменение информации об авторе.
| DELETE | /api/authors/{author_id}/ | удаление автора.

### Жанры
| HTTP | Endpoints | Action |
| --- | --- | --- |
| GET | /api/genres/ | получение списка всех жанров с пагинацией.
| GET | /api/genres/{genre_id}/ | получение информации о конкретном жанре и о книгах этого жанра.
| POST | /api/genres/ | создание нового жанра.
| PUT | /api/genres/{genre_id}/ | изменение информации о жанре.
| DELETE | /api/genres/{genre_id}/ | удаление жанра.

### Дополнительный функционал
| HTTP | Endpoints | Action |
| --- | --- | --- |
| GET | /api/books/copies?top=N/ | получение топ N книг по количеству экземпляров.
| GET | /api/authors/{author_id}/stat/ | получение количества книг у конкретного автора.
| GET | /api/authors/stat?page=N&page_count=M/ | получение количества книг по каждому автору.
| POST | /api/books/delivery/ | добавление новых книг в базу данных из файла JSON.


## Технологии
Проект использует следующие технологии и библиотеки:

- Django: фреймворк для веб-приложений на Python.
- Django REST Framework (DRF): мощный инструмент для создания веб-API.
- Swagger (drf-yasg): автоматическая генерация документации для API.
- Docker: контейнеризация приложения.


## Дополнительные аспекты
Проект реализует:

- Покрытие всех endpoint'ов тестами с использованием pytest.
- Упаковку приложения в Docker контейнер для удобства развертывания и управления окружением.
- Автоматическую генерацию документации API с помощью Swagger.


## Документация API
Документация API автоматически генерируется и доступна по ссылке Swagger UI после запуска проекта. Swagger предоставляет подробную информацию о доступных endpoint'ах, параметрах запросов и форматах данных.


## Автор 
[PeterPanda0](https://github.com/PeterPanda0)


## Лицензия
Этот проект доступен для использования по лицензии MIT.