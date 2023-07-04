from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Follower
from .serializers import FollowerSerializer
from books.models import Book


class FollowerListCreateView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs.get("pk"))
        user = self.request.user
        try:
            user_following = Follower.objects.get(pk=user.id)
            if (
                user_following.user_id == user.id
                and user_following.book_id == book.id
                 ):
                raise ValueError("Você já está seguindo este livro.")
        except Follower.DoesNotExist:
            pass
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs.get("pk"))
        user = self.request.user
        serializer.save(user=user, book=book)
