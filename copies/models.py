from django.db import models


class Copy(models.Model):
    status_for_loan = models.BooleanField(null=True, default=True)

    book = models.ForeignKey(
        "books.Book",
        on_delete=models.PROTECT,
        related_name="copy"
    )
