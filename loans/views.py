from rest_framework import generics, views
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from datetime import datetime as dt

from .models import Loan
from .serializers import LoanSerializer
from .exceptions import LoanIsNotStatusAvaliable
from copies.models import Copy
from books.models import Book
from users.models import User
from users.permissions import IsAuthenticated, IsColaborator


class LoanView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = LoanSerializer
    lookup_url_kwarg = "book_id"

    def perform_create(self, serializer):
        book_id = self.kwargs.get("book_id")
        book = get_object_or_404(Book, pk=book_id)

        user = self.request.user

        if user.status_for_loan is False:
            message = "This user alredy have a loan"
            raise LoanIsNotStatusAvaliable(message)

        if book.disponibility is False:
            message = ("This book is not available, follow to check"
                       "availability status.")
            raise LoanIsNotStatusAvaliable(message)

        copy = Copy.objects.filter(book_id=book_id, is_avaliable=True).first()
        copy.is_avaliable = False
        copy.save()

        user_loans_count = user.loans.count()
        if user_loans_count == 2:
            user.status_for_loan = False
            user.save()

        serializer.save(
            user=user,
            copy=copy
        )

        status_copy = Copy.objects.filter(
            book_id=book_id,
            is_avaliable=True
        ).first()

        if status_copy is None:
            book.disponibility = False
            book.save()


class LoanCopyDetailView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = LoanSerializer
    lookup_url_kwarg = "copy_id"

    def get_queryset(self):
        req_method = self.request.method
        copy_id = self.kwargs.get("copy_id", None)
        user = self.request.user
        is_colaborator = user.is_colaborator

        if (
            req_method == "GET"
            and is_colaborator is True
           and copy_id is not None
           ):
            return Loan.objects.filter(copy_id=copy_id)
        elif (
              req_method == "GET"
              and is_colaborator is False
              and copy_id is None
             ):
            return Loan.objects.filter(user_id=user.id)
        elif req_method == "GET" and is_colaborator is False:
            return Loan.objects.filter(copy_id=copy_id, user_id=user.id)

        return Loan.objects.all()


class LoanColaboratorDetailView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = LoanSerializer
    permission_classes = [IsColaborator]

    lookup_url_kwarg = "student_id"

    def get_queryset(self):
        student_id = self.kwargs.get("student_id")
        student = get_object_or_404(User, pk=student_id)

        return Loan.objects.filter(user=student)


class LoanCheckoutView(views.APIView):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsColaborator]

    def patch(self, request: views.Request, loan_id) -> views.Response:
        loan = get_object_or_404(Loan, id=loan_id)

        copy = loan.copy

        copy.is_avaliable = True
        copy.save()

        book = copy.book
        book_disp = book.disponibility

        if book_disp is False:
            book.disponibility = True
            book.save()

        user = loan.user

        if user.loans.count() > 1:
            others_loans = user.loans.all()
            for loan_obj in others_loans:
                if loan_obj.id != loan_id:
                    loan_return_date = loan_obj.loan_return
                    now = dt.now().date()
                    loan_date_subtraction = now - loan_return_date

                    if loan_date_subtraction.days > 0:
                        user.status_for_loan = False
                        user.save()
                        return

        loan.is_active = False
        loan.returned_at = dt.now().date()
        loan.save()

        loan_serialized = LoanSerializer(instance=loan).data

        return views.Response(loan_serialized)
