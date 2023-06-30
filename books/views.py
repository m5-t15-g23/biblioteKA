from rest_framework import generics

from .models import Book
from .serializers import BookSerializer


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
