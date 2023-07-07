from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsColaboratorOrReadOnly

from .models import Book
from .serializers import BookSerializer


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaboratorOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save().users.add(user)
