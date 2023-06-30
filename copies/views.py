from rest_framework import generics

from .models import Copy
from .serializers import CopySerializer


class CopyView(generics.ListAPIView):
    queryset = Copy.objects.all()
    serializer_class = CopySerializer
