from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from loans.models import Loan
from loans.serializers import LoanSerializer
from copies.models import Copy


class LoanView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = Loan.objects.all()

    def get_queryset(self):
        user = self.request.user
        is_colaborator = user.is_colaborator

        if is_colaborator is False:
            user_id = user.id
            return Loan.objects.filter(user_id=user_id)

        return Loan.objects.all()

    serializer_class = LoanSerializer


class LoanCopyDetailView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = LoanSerializer
    lookup_url_kwarg = "copy_id"

    def get_queryset(self):
        req_method = self.request.method
        copy_id = self.kwargs.get("copy_id")

        if req_method == "GET":
            return Loan.objects.filter(copy_id=copy_id)

        return Loan.objects.all()

    def perform_create(self, serializer):
        copy_id = self.kwargs.get("copy_id")
        copy = get_object_or_404(Copy, pk=copy_id)

        user = self.request.user

        serializer.save(
            user=user,
            copy=copy
        )
