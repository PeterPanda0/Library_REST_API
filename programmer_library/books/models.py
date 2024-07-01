from django.db import models

# Количество книг по умолчанию
COPY = 1


class Author(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=128)
    authors = models.ManyToManyField(Author, through='AuthorBook')
    genres = models.ManyToManyField(Genre, through='GenreBook')
    count = models.PositiveSmallIntegerField(default=COPY)

    def __str__(self):
        return self.title


class AuthorBook(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'"{self.book}" {self.author}'


class GenreBook(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f'"{self.book}" {self.genre}'
