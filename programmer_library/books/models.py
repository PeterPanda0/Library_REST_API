from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from programmer_library.constants import (COPY, MAX_SCORE, MIN_SCORE,
                                          NAME_MAX_LEN, TITLE_MAX_LEN)


class Author(models.Model):
    """Модель автор с уникальным именем."""

    name = models.CharField(
        max_length=NAME_MAX_LEN, unique=True, verbose_name='Имя автора'
    )

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанр с уникальным названием."""

    title = models.CharField(
        max_length=TITLE_MAX_LEN, unique=True, verbose_name='Название'
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.title


class Book(models.Model):
    """Модель книга, связанная с авторами и жанрами."""

    title = models.CharField(
        max_length=TITLE_MAX_LEN, verbose_name='Название'
    )
    authors = models.ManyToManyField(
        Author, through='AuthorBook', verbose_name='Авторы'
    )
    genres = models.ManyToManyField(
        Genre, through='GenreBook', verbose_name='Жанры'
    )
    count = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE)
        ],
        default=COPY,
        verbose_name='Количество экземпляров'
    )

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title


class AuthorBook(models.Model):
    """Промежуточная модель для книг и их авторов."""

    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, verbose_name='Автор'
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name='Название книги'
    )

    def __str__(self):
        return f'"{self.book}" {self.author}'


class GenreBook(models.Model):
    """Промежуточная модель для книг и жанров."""

    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='Жанр'
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name='Название книги'
    )

    def __str__(self):
        return f'"{self.book}" {self.genre}'
