from rest_framework import serializers
from datetime import timedelta
from django.utils import timezone

from copies.serializers import CopySerializer
from loans.models import Loan
from users.serializers import UserSerializer


def return_date():
    loan_date_return = timezone.now() + timedelta(days=30)
    week_day = loan_date_return.weekday()

    match week_day:
        case 5:
            loan_date_return = loan_date_return + timedelta(days=2)
        case 6:
            loan_date_return = loan_date_return + timedelta(days=1)

    return loan_date_return


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
        read_only_fields = ["id", "user", "copy", "loan_return"]

    def create(self, validated_data):
        loan_return = return_date()

        loan_to_create = {
            "loan_return": loan_return,
            **validated_data
        }
        return Loan.objects.create(**loan_to_create)

    def to_representation(self, instance):
        date_format = "%d/%m/%Y"
        return {
            "id": instance.id,
            "loan_date": instance.loan_date.strftime(date_format),
            "loan_return": instance.loan_return.strftime(date_format),
            "user_id": instance.user.id,
            "user_email": instance.user.email,
            "user_username": instance.user.username,
            "copy_id": instance.copy.id,
            "copy_title": instance.copy.book.title
        }
