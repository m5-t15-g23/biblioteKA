from rest_framework import serializers

from .models import Copy
from books.serializers import BookSerializer


class CopySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Copy
        fields = [
            "id",
            "status_for_loan",
            "book"
        ]
        read_only_fields = ["id", "book"]

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "book_id": instance.book.id,
            "book_title": instance.book.title,
            "status_for_loan": instance.status_for_loan
        }
