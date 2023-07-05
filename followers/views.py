from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Follower
from .serializers import FollowerSerializer
from .exceptions import BookAlreadyFollowed
from books.models import Book
from users.permissions import IsStudent


class FollowerView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    lookup_url_kwarg = "book_id"

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs.get("book_id"))
        user = self.request.user
        
        user_following = Follower.objects.filter(student_id=user.id, book_followed=book).first()
        print(user_following)
        if user_following is not None:
            message = "You already follow this book"
            raise BookAlreadyFollowed(message)

        serializer.save(student=user, book_followed=book)

