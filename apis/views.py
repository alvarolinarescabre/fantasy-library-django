from rest_framework import generics, permissions
from inventario.models import Genre, Author, Book
from .serializers import GenreSerializer, AuthorSerializer, BookSerializer


class GenreList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_queryset(self):
        genres = Genre.objects.all()
        return genres


class GenreCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAdminUser, )
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_queryset(self):
        genres = Genre.objects.all()
        return genres

    def perform_create(self, serializer):
        serializer.save()


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser, )
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    http_method_names = ['get', 'post', 'put', 'delete']


class AuthorList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        authors = Author.objects.all()
        return authors


class AuthorCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        authors = Author.objects.all()
        return authors

    def perform_create(self, serializer):
        serializer.save()


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser, )
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    http_method_names = ['get', 'post', 'put', 'delete']


class BookList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        books = Book.objects.all()
        return books


class BookCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        books = Book.objects.all()
        return books

    def perform_create(self, serializer):
        serializer.save()


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser, )
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
