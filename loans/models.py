from datetime import datetime, timedelta
from django.db import models

def return_date():    
    return datetime.now() + timedelta(days=30)

class Loan(models.Model):
    
    loan_date = models.DateTimeField(auto_now_add=True)
    loan_return = models.DateTimeField(default=return_date)
    
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="loan"
    ) 
    copie = models.ForeignKey(
        "copie.Copie", on_delete=models.PROTECT, related_name="copie"
    )