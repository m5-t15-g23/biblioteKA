from rest_framework import serializers

from .models import Copy
from books.serializers import BookSerializer


class CopySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Copy
        fields = [
            "id",
            "is_avaliable",
            "book"
        ]
        read_only_fields = ["id", "book"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "book_id": instance.book.id,
            "book_title": instance.book.title,
            "is_avaliable": instance.is_avaliable
        }
