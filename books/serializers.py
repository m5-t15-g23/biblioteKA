from rest_framework import serializers
from .models import Book
from copies.models import Copy
from users.serializers import UserSerializer


class BookSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True, read_only=True)

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
            "user"
        ]
        read_only_fields = ["user", "id"]
        depth = 1
        extra_kwargs = {"copies_number": {"write_only": True}}

    def create(self, validated_data: dict) -> Book:
        copies_number = validated_data.get("copies_number")
        book = Book.objects.create(**validated_data)

        for i in range(copies_number):
            Copy.objects.create(book=book)

        return book
