from rest_framework import serializers
from datetime import datetime as dt, timedelta

from copies.serializers import CopySerializer
from loans.models import Loan
from users.serializers import UserSerializer


def return_date():
    date_format = "%d/%m/%Y"
    loan_date_return = dt.now() + timedelta(days=30)
    week_day = loan_date_return.weekday()

    if week_day == 5:
        loan_date_return = loan_date_return + timedelta(days=2)
    elif week_day == 6:
        loan_date_return = loan_date_return + timedelta(days=1)

    loan_date_return_str = loan_date_return.strftime(date_format)
    loan_date_return = dt.strptime(loan_date_return_str, date_format).date()

    return loan_date_return


class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    copy = CopySerializer(read_only=True)

    def validateIfALoanIsReturned(self, date_format):
        if self.fields.is_active is None:
            return self.fields.is_active
        else:
            return self.fields.is_active.strftime(date_format)

    def create(self, validated_data):
        loan_return = return_date()

        loan_to_create = {
            "loan_return": loan_return,
            "returned_at": None,
            **validated_data
        }
        return Loan.objects.create(**loan_to_create)

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "loan_date": instance.loan_date,
            "loan_return": instance.loan_return,
            "is_active": instance.is_active,
            "returned_at": (instance.returned_at
                            if instance.returned_at is not None
                            else None),
            "user_id": instance.user.id,
            "user_email": instance.user.email,
            "user_username": instance.user.username,
            "copy_id": instance.copy.id,
            "book_title": instance.copy.book.title
        }

    class Meta:
        model = Loan
        fields = [
            "id",
            "loan_date",
            "loan_return",
            "is_active",
            "returned_at",
            "user",
            "copy"
        ]
        read_only_fields = ["id", "user", "copy", "loan_return"]
