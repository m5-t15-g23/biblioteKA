from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from loans.models import Loan
from loans.serializers import LoanSerializer
from copies.models import Copy


class LoanView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanCopyDetailView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        copy_id = self.kwargs.get("pk")
        copy = get_object_or_404(Copy, pk=copy_id)

        user = self.request.user

        serializer.save(
            user=user,
            copy=copy
        )
