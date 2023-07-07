from rest_framework import generics
from rest_framework.views import APIView, Request, Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from .models import Follower
from .serializers import FollowerSerializer
from .exceptions import FollowExceptions
from books.models import Book
from users.permissions import IsStudent, IsColaborator


class FollowerView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]

    serializer_class = FollowerSerializer
    lookup_url_kwarg = "book_id"

    def get_queryset(self):
        method = self.request.method
        student = self.request.user

        if method == "GET":
            return Follower.objects.filter(student=student)

        return Follower.objects.all()

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs.get("book_id"))
        user = self.request.user

        user_following = Follower.objects.filter(
            student_id=user.id,
            book_followed=book
        ).first()

        if user_following is not None:
            message = "You already follow this book"
            raise FollowExceptions(message)

        serializer.save(student=user, book_followed=book)


class FollowerListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaborator]

    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer


class FollowerDestroyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]

    def delete(self, request: Request, book_id) -> Response:
        book_followed = get_object_or_404(Book, pk=book_id)
        student = request.user

        following_student_book = Follower.objects.filter(
            student=student,
            book_followed=book_followed
        ).first()

        if following_student_book is None:
            message = "Student doesn't follow this book"
            raise FollowExceptions(message)

        following_student_book.delete()

        return Response(status=204)
