from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Book
from .serializers import BookSerializer
from users.permissions import IsColaboratorOrReadOnly, IsAuthenticated


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaboratorOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save().users.add(user)


class BookDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = BookSerializer
    lookup_url_kwarg = "book_id"

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")

        return Book.objects.filter(id=book_id)
