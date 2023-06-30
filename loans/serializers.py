from rest_framework import serializers
from copies.serializers import CopieSerializer
from loans.models import Loan
from users.serializers import UserSerializer

class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    copie = CopieSerializer(read_only=True)

    class Meta: 
        model = Loan
        fields = [
            "id",
            "loan_date",
            "loan_return",
            "user",
            "copie"
        ]