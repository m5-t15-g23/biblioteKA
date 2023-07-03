from django.db import models
from datetime import datetime


class Language(models.TextChoices):
    ENGLISH = 'english'
    PORTUGUESE = 'portuguese'
    SPANISH = 'spenish'
    FRENCH = 'french'
    ITALIAN = 'italian'
    GERMAN = 'german'
    NOTINFORMED = 'not informed'


class Book(models.Model):
    class Meta:
        ordering = ["id"]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    publication_year = models.DateTimeField(null=True, default=datetime.now())
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
