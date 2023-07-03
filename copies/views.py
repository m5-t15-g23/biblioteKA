from rest_framework import generics

from .models import Copy
from .serializers import CopySerializer
from users.permissions import IsColaborator


class CopyView(generics.ListAPIView):
    permission_classes = [IsColaborator]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer
