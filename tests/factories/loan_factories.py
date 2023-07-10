from loans.models import Loan
from datetime import datetime as dt


def create_loan(student, copy) -> Loan:
    loan = Loan.objects.create(
        loan_return=dt.now(),
        user=student,
        copy=copy
    )

    return loan
