from rest_framework import generics
from loans.models import Loan
from loans.serializers import LoanSerializer
from django.shortcuts import get_object_or_404
from copies.models import Copy


class LoanView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        copy_id = self.kwargs.get("pk")
        copy = get_object_or_404(Copy, pk=copy_id)

        serializer.save(
            user=self.request.user,
            copy_id=copy.id
        )
