from rest_framework import serializers
from datetime import datetime as dt

from .models import Book
from users.serializers import UserSerializer
from copies.models import Copy


class BookSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    def create(self, validated_data: dict) -> Book:
        copies_number = validated_data.get("copies_number")
        book_title = validated_data.get("title")
        book = Book.objects.filter(title=book_title).first()

        if book is None:
            book = Book.objects.create(**validated_data)

        for _ in range(copies_number):
            Copy.objects.create(book=book)

        return book

    def to_representation(self, instance):
        date_format = "%Y-%m-%d"
        return {
            "id": instance.id,
            "title": instance.title,
            "author": instance.author,
            "description": instance.description,
            "publication_year": instance.publication_year.strftime(
                date_format
            ),
            "page_numbers": instance.page_numbers,
            "language": instance.language,
            "genre": instance.genre,
            "disponibility": instance.disponibility,
        }

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "description",
            "publication_year",
            "page_numbers",
            "language",
            "genre",
            "disponibility",
            "copies_number",
            "users"
        ]
        read_only_fields = ["users"]
        depth = 1
        extra_kwargs = {"copies_number": {"write_only": True}}
