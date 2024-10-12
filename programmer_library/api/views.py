from django.db.models import Count
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (AuthorListSerializer, AuthorSerializer,
                             AuthorStatSerializer, BookListSerializer,
                             BookSerializer, GenreListSerializer,
                             GenreSerializer)
from books.models import Author, Book, Genre
from programmer_library.constants import (DEFAULT_BOOKS_COUNT,
                                          DELIVERY_MESSAGE)


class AuthorViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления авторами."""

    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorListSerializer
        return AuthorSerializer

    @action(detail=True, methods=['get'], url_path='stat')
    def stat(self, request, pk=None):
        """Возвращает количество книг у конкретного автора."""
        author = Author.objects.get(pk=pk)
        serializer = AuthorStatSerializer(author)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='stat')
    def stat_all(self, request):
        """Возвращает количество книг для всех авторов."""
        authors = Author.objects.annotate(
            book_count=Count('book')).order_by('-book_count', 'name')
        page = self.paginate_queryset(authors)
        if page is not None:
            serializer = AuthorStatSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = AuthorStatSerializer(authors, many=True)
        return Response(serializer.data)


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления жанрами."""

    queryset = Genre.objects.all().order_by('title')
    serializer_class = GenreSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return GenreListSerializer
        return GenreSerializer


class BookViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления книгами."""

    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer

    @action(detail=False, methods=['get'], url_path='copies')
    def copies(self, request):
        """Возвращает топ N книг по количеству экземпляров."""
        top_n = int(request.query_params.get('top', DEFAULT_BOOKS_COUNT))
        books = Book.objects.order_by('-count', 'title')[:top_n]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='delivery')
    def delivery(self, request):
        """Добавляет партию новых книг в библиотеку."""
        books_data = request.data.get('books', [])
        for book_data in books_data:
            serializer = self.get_serializer(data=book_data)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'detail': DELIVERY_MESSAGE},
            status=status.HTTP_201_CREATED
        )
