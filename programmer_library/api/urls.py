from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import AuthorViewSet, BookViewSet, GenreViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
