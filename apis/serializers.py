from rest_framework import serializers
from inventario.models import Genre, Author, Book


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("type",)


def create(self, validated_data):
    return Genre.objects.create(**validated_data)


class AuthorSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        read_only=False,
        queryset=Genre.objects.all(),
        slug_field='type'
    )

    class Meta:
        model = Author
        fields = ("name", "genre")

    def create(self, validated_data):
        return Author.objects.create(**validated_data)


class BookSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        read_only=False,
        queryset=Genre.objects.all(),
        slug_field='type'
    )

    author = serializers.SlugRelatedField(
        read_only=False,
        queryset=Author.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Book
        fields = ("title", "author", "genre", "publish_date", "isbn")

    def create(self, validated_data):
        return Book.objects.create(**validated_data)


