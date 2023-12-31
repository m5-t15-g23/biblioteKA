from django.db import models


class Loan(models.Model):
    loan_date = models.DateField(auto_now_add=True)
    loan_return = models.DateField()
    is_active = models.BooleanField(null=True, default=True)
    returned_at = models.DateField(null=True)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="loans"
    )
    copy = models.ForeignKey(
        "copies.Copy", on_delete=models.PROTECT, related_name="loans"
    )

    def __str__(self) -> str:
        return f"<Loan [{self.id}] -> {self.user}/{self.is_active}>"

    class Meta:
        ordering = ["id"]
