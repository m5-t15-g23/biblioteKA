from django.db import models


class Copy(models.Model):
    is_avaliable = models.BooleanField(null=True, default=True)

    book = models.ForeignKey(
        "books.Book",
        on_delete=models.PROTECT,
        related_name="copies"
    )

    def __str__(self) -> str:
        return f"<Copy [{self.id}] -> {self.book.title}/{self.is_avaliable}>"

    class Meta:
        ordering = ["id"]
