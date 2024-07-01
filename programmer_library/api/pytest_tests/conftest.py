import pytest
from books.models import Author, Book, Genre
from rest_framework.test import APIClient

# Количество создаваемых объектов.
OBJECTS = 12


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def author():
    return Author.objects.create(name='Author 1')

@pytest.fixture
def genre():
    return Genre.objects.create(title='Genre 1')

@pytest.fixture
def book(author, genre):
    book = Book.objects.create(title='Book 1', count=5)
    book.authors.add(author)
    book.genres.add(genre)
    return book

@pytest.fixture
def authors():
    authors = [
        Author.objects.create(name=f'Author{i}') for i in range(OBJECTS)
    ]
    return authors

@pytest.fixture
def genres():
    genres = [
        Genre.objects.create(title=f'Genre{i}') for i in range(OBJECTS)
    ]
    return genres

@pytest.fixture
def books(authors, genres):
    books = []
    for i in range(OBJECTS):
        book = Book.objects.create(title=f'Book{i}', count=i)
        book.authors.set(authors[:i])
        book.genres.set(genres[:i])
        books.append(book)
    return books

@pytest.fixture
def delivery_data():
    return {
        'books': [
            {
                'title': 'New Book1',
                'count': 5,
                'authors': [{'name': 'New Author1'}],
                'genres': [{'title': 'New Genre1'}]
            },
            {
                'title': 'New Book2',
                'count': 5,
                'authors': [{'name': 'New Author2'}],
                'genres': [{'title': 'New Genre2'}]
            },
            {
                'title': 'New Book3',
                'count': 5,
                'authors': [{'name': 'New Author3'}],
                'genres': [{'title': 'New Genre3'}]
            }
        ]
    }

@pytest.fixture
def book_data():
    book_data = {
        'title': 'Single book',
        'count': 5,
        'authors': [{'name': 'Unknown Author'}],
        'genres': [{'title': 'Unknown Genre'}]
    }
    return book_data
