from random import choice

import pytest
from django.urls import reverse
from rest_framework import status

from books.models import Author, Book, Genre
from .constants import (DEFAULT_TOP_COPIES_BOOKS, OBJECT,
                        PAGE, PAGE_SIZE, QUERY_OBJECTS)


@pytest.mark.django_db
def test_get_books(api_client, books):
    """GET /api/books/"""
    response = api_client.get(reverse('book-list'))
    data = response.data['results']
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == PAGE_SIZE


@pytest.mark.django_db
def test_get_book_detail(api_client, book):
    """GET /api/books/{book_id}"""
    response = api_client.get(reverse('book-detail', args=(book.id,)))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == book.title


@pytest.mark.django_db
def test_get_top_books(api_client, books):
    """GET /api/books/copies?top=N"""
    response = api_client.get(reverse('book-copies'), {'top': QUERY_OBJECTS})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == QUERY_OBJECTS
    response = api_client.get(reverse('book-copies'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == DEFAULT_TOP_COPIES_BOOKS


@pytest.mark.django_db
def test_get_author_stat(api_client, authors, books):
    """GET /api/authors/{author_id}/stat"""
    author = choice(authors)
    response = api_client.get(reverse('author-stat', args=(author.id,)))
    count = Book.objects.filter(authors__id=author.id).count()
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == author.name
    assert response.data['book_count'] == count


@pytest.mark.django_db
def test_get_authors_stat_all(api_client, authors, books):
    """GET /api/authors/stat?page=N&page_count=M"""
    response = api_client.get(
        reverse('author-stat-all'),
        {'page': PAGE, 'page_count': QUERY_OBJECTS}
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == QUERY_OBJECTS
    response = api_client.get(reverse('author-stat-all'))
    assert len(response.data['results']) == PAGE_SIZE


@pytest.mark.django_db
def test_post_books_delivery(api_client, delivery_data):
    """POST /api/books/delivery"""
    response = api_client.post(
        reverse('book-delivery'), delivery_data, format='json')
    data = delivery_data['books']
    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.filter(title=data[0]['title']).exists()
    assert Book.objects.filter(title=data[1]['title']).exists()
    assert Book.objects.filter(title=data[2]['title']).exists()


@pytest.mark.django_db
def test_post_create_book(api_client, book_data):
    """POST /api/books/"""
    response = api_client.post(reverse('book-list'), book_data, format='json')
    book = Book.objects.get()
    assert response.status_code == status.HTTP_201_CREATED
    assert book.title == book_data['title']
    assert book.count == book_data['count']
    for author_data in book_data['authors']:
        assert book.authors.filter(name=author_data['name']).exists()
    for genre_data in book_data['genres']:
        assert book.genres.filter(title=genre_data['title']).exists()
    response = api_client.post(reverse('book-list'), book_data, format='json')
    new_count = Book.objects.get().count
    assert new_count == book.count + book.count


@pytest.mark.django_db
def test_delete_book(api_client, book):
    """DELETE /api/books/{book_id}"""
    response = api_client.delete(reverse('book-detail', args=(book.id,)))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_put_update_book(api_client, book, book_data):
    """PUT /api/books/{book_id}"""
    response = api_client.put(
        reverse('book-detail', args=(book.id,)), book_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == book_data['title']
    assert book.count == book_data['count']
    for author_data in book_data['authors']:
        assert book.authors.filter(name=author_data['name']).exists()
    for genre_data in book_data['genres']:
        assert book.genres.filter(title=genre_data['title']).exists()


@pytest.mark.django_db
def test_get_authors(api_client, authors):
    """GET /api/authors"""
    response = api_client.get(reverse('author-list'))
    data = response.data['results']
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == PAGE_SIZE


@pytest.mark.django_db
def test_get_author_detail(api_client, authors, books):
    """GET /api/authors/{author_id}"""
    author = choice(authors)
    response = api_client.get(reverse('author-detail', args=(author.id,)))
    author_books = Book.objects.filter(authors__id=author.id)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == author.name
    assert len(response.data['books']) == len(author_books)


@pytest.mark.django_db
def test_post_create_author(api_client):
    """POST /api/authors"""
    author_data = {'name': 'New Author'}
    response = api_client.post(reverse('author-list'), author_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    response = api_client.post(reverse('author-list'), author_data, format='json')
    assert Author.objects.all().count() == OBJECT


@pytest.mark.django_db
def test_delete_author(api_client, author):
    """DELETE /api/authors/{author_id}"""
    response = api_client.delete(reverse('author-detail', args=(author.id,)))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_put_update_author(api_client, author):
    """PUT /api/authors/{author_id}"""
    author_data = {'name': 'Updated Author'}
    response = api_client.put(
        reverse('author-detail', args=(author.id,)),
        author_data, format='json'
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == author_data['name']


@pytest.mark.django_db
def test_get_genres(api_client, genres):
    """GET /api/genres"""
    response = api_client.get(reverse('genre-list'))
    data = response.data['results']
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == PAGE_SIZE


@pytest.mark.django_db
def test_get_genre_detail(api_client, genre):
    """GET /api/genres/{genre_id}"""
    response = api_client.get(reverse('genre-detail', args=(genre.id,)))
    genre_books = Book.objects.filter(genres__id=genre.id)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == genre.title
    assert len(response.data['books']) == len(genre_books)


@pytest.mark.django_db
def test_post_create_genre(api_client):
    """POST /api/genres"""
    genre_data = {'title': 'New Genre'}
    response = api_client.post(reverse('genre-list'), genre_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    response = api_client.get(reverse('genre-list'), genre_data, format='json')
    assert Genre.objects.all().count() == OBJECT


@pytest.mark.django_db
def test_delete_genre(api_client, genre):
    """DELETE /api/genres/{genre_id}"""
    response = api_client.delete(reverse('genre-detail', args=(genre.id,)))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_put_update_genre(api_client, genre):
    """PUT /api/genres/{genre_id}"""
    genre_data = {'title': 'Updated Genre'}
    response = api_client.put(
        reverse('genre-detail', args=(genre.id,)), genre_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == genre_data['title']
