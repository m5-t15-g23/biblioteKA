from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSerializer, StudentStatusSerializer
from .permissions import IsColaborator, IsAuthenticatedOrCreate


class UserView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrCreate]
    serializer_class = UserSerializer

    def get_queryset(self):
        req_method = self.request.method
        user = self.request.user
        is_colaborator = user.is_colaborator

        if req_method == "GET" and is_colaborator is False:
            return User.objects.filter(id=user.id)

        return User.objects.all()


class UserDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaborator]
    serializer_class = StudentStatusSerializer

    lookup_url_kwarg = "student_id"

    def get_queryset(self):
        student_id = self.kwargs.get("student_id")
        student = get_object_or_404(User, pk=student_id)

        return User.objects.filter(id=student_id)
