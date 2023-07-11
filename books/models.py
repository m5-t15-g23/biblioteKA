from django.db import models
from datetime import datetime as dt


class Language(models.TextChoices):
    ENGLISH = "English"
    PORTUGUESE = "Portuguese"
    SPANISH = "Spanish"
    FRENCH = "French"
    ITALIAN = "Italian"
    GERMAN = "German"
    NOTINFORMED = "Not Informed"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    publication_year = models.DateTimeField(null=True, default=dt.now())
    page_numbers = models.IntegerField()
    language = models.CharField(
        max_length=50,
        choices=Language.choices,
        default=Language.NOTINFORMED
    )
    genre = models.CharField(max_length=255)
    disponibility = models.BooleanField(null=True, default=True)
    copies_number = models.IntegerField()

    users = models.ManyToManyField(
        "users.User",
        related_name="books",
    )

    def __str__(self) -> str:
        return f"<Book [{self.id}] -> {self.title}>"

    class Meta:
        ordering = ["id"]
