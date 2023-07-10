from django.db import models


class Follower(models.Model):
    student = models.ForeignKey(
        "users.User",
        related_name="followers",
        on_delete=models.CASCADE
    )
    book_followed = models.ForeignKey(
        "books.Book",
        related_name="book_followers",
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"<User [{self.id}] -> {self.student}/{self.book_followed}>"

    class Meta:
        ordering = ["id"]
