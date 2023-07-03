from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from loans.models import Loan
from loans.serializers import LoanSerializer
from copies.models import Copy
from users.models import User
from users.permissions import IsAuthenticated, IsColaborator


# class LoanView(generics.ListAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     queryset = Loan.objects.all()

#     def get_queryset(self):
#         user = self.request.user
#         is_colaborator = user.is_colaborator

#         if is_colaborator is False:
#             user_id = user.id
#             return Loan.objects.filter(user_id=user_id)

#         return Loan.objects.all()

#     serializer_class = LoanSerializer


class LoanCopyDetailView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = LoanSerializer
    lookup_url_kwarg = "copy_id"

    def get_queryset(self):
        req_method = self.request.method
        copy_id = self.kwargs.get("copy_id", None)
        user = self.request.user
        is_colaborator = user.is_colaborator

        if req_method == "GET" and is_colaborator is True and copy_id is not None:
            return Loan.objects.filter(copy_id=copy_id)
        elif req_method == "GET" and is_colaborator is False and copy_id is None:
            return Loan.objects.filter(user_id=user.id)
        elif req_method == "GET" and is_colaborator is False:
            return Loan.objects.filter(copy_id=copy_id, user_id=user.id)

        return Loan.objects.all()

    def perform_create(self, serializer):
        copy_id = self.kwargs.get("copy_id")
        copy = get_object_or_404(Copy, pk=copy_id)

        user = self.request.user

        serializer.save(
            user=user,
            copy=copy
        )


class LoanColaboratorDetailView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = LoanSerializer
    permission_classes = [IsColaborator]

    lookup_url_kwarg = "student_id"

    def get_queryset(self):
        student_id = self.kwargs.get("student_id")
        student = get_object_or_404(User, pk=student_id)

        return Loan.objects.filter(user=student)
