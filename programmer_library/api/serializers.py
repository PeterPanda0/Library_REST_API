from rest_framework import serializers

from books.models import COPY, Author, AuthorBook, Book, Genre, GenreBook


class AuthorGenreMixin:
    def get_books(self, obj):
        books = obj.book_set.all()
        serializer = BookListSerializer(books, many=True)
        return serializer.data


class AuthorListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=64, required=False)

    class Meta:
        model = Author
        fields = ('id', 'name')


class AuthorStatSerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ('id', 'name', 'book_count')

    def get_book_count(self, obj):
        return obj.book_set.count()


class AuthorSerializer(AuthorGenreMixin, serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ('id', 'name', 'books')


class GenreListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=64, required=False)

    class Meta:
        model = Genre
        fields = ('id', 'title')


class GenreSerializer(AuthorGenreMixin, serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ('id', 'title', 'books')


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title')


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorListSerializer(many=True)
    genres = GenreListSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'count', 'authors', 'genres')

    def create(self, validated_data):
        authors_data = validated_data.pop('authors', [])
        genres_data = validated_data.pop('genres', [])
        count = validated_data.get('count', COPY)
        book, created = Book.objects.get_or_create(
            title=validated_data.get('title'), defaults={'count': count}
        )
        if not created:
            book.count += count
            book.save()
        else:
            for author_data in authors_data:
                author, _ = Author.objects.get_or_create(**author_data)
                AuthorBook.objects.get_or_create(author=author, book=book)
            for genre_data in genres_data:
                genre, _ = Genre.objects.get_or_create(**genre_data)
                GenreBook.objects.get_or_create(genre=genre, book=book)
        return book

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.count = validated_data.get('count', instance.count)
        instance.save()
        if 'authors' in validated_data:
            authors_data = validated_data.pop('authors')
            for author_data in authors_data:
                author, _ = Author.objects.get_or_create(**author_data)
                if author not in instance.authors.all():
                    AuthorBook.objects.create(author=author, book=instance)
        if 'genres' in validated_data:
            genres_data = validated_data.pop('genres')
            for genre_data in genres_data:
                genre, _ = Genre.objects.get_or_create(**genre_data)
                GenreBook.objects.get_or_create(genre=genre, book=instance)
        return instance
