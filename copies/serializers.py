from rest_framework import serializers

from .models import Copy
from books.serializers import BookSerializer


class CopySerializer(serializers.ModelField):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Copy
        fields = [
            "id",
            "status_for_loan",
            "book"
        ]
        read_only_fields = ["id", "book"]
