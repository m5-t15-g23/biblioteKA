from rest_framework import serializers

from .models import Copie
from books.serializers import BookSerializer


class CopieSerializer(serializers.ModelField):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Copie
        fields = [
            "id",
            "status_for_loan",
            "book"
        ]
        read_only_fields = ["id", "book"]
