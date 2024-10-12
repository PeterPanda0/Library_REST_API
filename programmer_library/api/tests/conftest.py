import pytest
from rest_framework.test import APIClient

from books.models import Author, Book, Genre
from .constants import (BOOK, BOOK_1, BOOK_2, COUNT, GENRE, GENRE_1,
                        GENRE_2, NAME, NAME_1, NAME_2, OBJECTS)


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def author():
    return Author.objects.create(name=NAME)

@pytest.fixture
def genre():
    return Genre.objects.create(title=GENRE)

@pytest.fixture
def book(author, genre):
    book = Book.objects.create(title=BOOK, count=COUNT)
    book.authors.add(author)
    book.genres.add(genre)
    return book

@pytest.fixture
def authors():
    authors = [
        Author.objects.create(name=f'Author {i}') for i in range(OBJECTS)
    ]
    return authors

@pytest.fixture
def genres():
    genres = [
        Genre.objects.create(title=f'Genre {i}') for i in range(OBJECTS)
    ]
    return genres

@pytest.fixture
def books(authors, genres):
    books = []
    for i in range(OBJECTS):
        book = Book.objects.create(title=f'Book {i}', count=i)
        book.authors.set(authors[:i])
        book.genres.set(genres[:i])
        books.append(book)
    return books

@pytest.fixture
def delivery_data():
    return {
        'books': [
            {
                'title': BOOK,
                'count': COUNT,
                'authors': [{'name': NAME}],
                'genres': [{'title': GENRE}]
            },
            {
                'title': BOOK_1,
                'count': COUNT,
                'authors': [{'name': NAME_1}],
                'genres': [{'title': GENRE_1}]
            },
            {
                'title': BOOK_2,
                'count': COUNT,
                'authors': [{'name': NAME_2}],
                'genres': [{'title': GENRE_2}]
            }
        ]
    }

@pytest.fixture
def book_data():
    book_data = {
        'title': BOOK,
        'count': COUNT,
        'authors': [{'name': NAME}],
        'genres': [{'title': GENRE}]
    }
    return book_data
