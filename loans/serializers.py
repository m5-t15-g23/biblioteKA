from rest_framework import serializers
from copies.serializers import CopySerializer
from loans.models import Loan
from users.serializers import UserSerializer


class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    copy = CopySerializer(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "loan_date",
            "loan_return",
            "user",
            "copy"
        ]
        read_only_fields = ["id", "user", "copy"]
