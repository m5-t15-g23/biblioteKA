from django.db import models


class Loan(models.Model):
    loan_date = models.DateTimeField(auto_now_add=True)
    loan_return = models.DateTimeField()

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="loans"
    )
    copy = models.ForeignKey(
        "copies.Copy", on_delete=models.PROTECT, related_name="loans"
    )
