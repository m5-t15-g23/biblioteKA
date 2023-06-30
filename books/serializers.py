from rest_framework import serializers
from .models import Book
from copies.models import Copie
from users.serializers import UserSerializer


class BookSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

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
            "copies_number"
        ]
        read_only_fields = ["user", "id"]
        extra_kwargs = {"copies_number": {"write_only": True}}

    def create(self, validated_data: dict) -> Book:
        copies_number = validated_data.pop("copies_number")
        book = Book.objects.create(**validated_data)

        for _ in range(copies_number):
            Copie.objects.create(book=book)

        return book
