from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from datetime import datetime as dt

from .models import User
from .serializers import UserSerializer, StudentStatusSerializer
from .permissions import IsColaborator, IsAuthenticatedOrCreate
from .exceptions import StudentLoanException
from loans.models import Loan


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


class UserDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaborator]

    lookup_url_kwarg = "student_id"

    def get_queryset(self):
        student_id = self.kwargs.get("student_id")
        get_object_or_404(User, pk=student_id)

        return User.objects.filter(id=student_id)

    def get_serializer_class(self):
        request_method = self.request.method

        if request_method == "PATCH":
            return UserSerializer

        return StudentStatusSerializer

    def perform_update(self, serializer):
        student_id = self.kwargs.get("student_id")
        student = get_object_or_404(User, pk=student_id)

        first_loan = Loan.objects.filter(user=student).first()

        if first_loan is None:
            message = "User didn't have loans yet"
            raise StudentLoanException(message)

        first_loan_return_date = first_loan.loan_return
        now = dt.now().date()
        loan_date_subtraction = now - first_loan_return_date

        if loan_date_subtraction.days < 0:
            message = "User first loan is already in permited period"
            raise StudentLoanException(message)

        serializer.save()
