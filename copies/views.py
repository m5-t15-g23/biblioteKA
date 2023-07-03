from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Copy
from .serializers import CopySerializer
from users.permissions import IsColaborator


class CopyView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsColaborator]

    queryset = Copy.objects.all()
    serializer_class = CopySerializer
