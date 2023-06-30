from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_colaborator = models.BooleanField(null=True, default=False)
    status_for_loan = models.BooleanField(null=True, default=True)

    def __str__(self) -> str:
        return f"<User [{self.id}] -> {self.first_name}>"
