from django.core.mail import send_mail
from django.conf import settings

#rapaziada isso é so uma ideia demoro, não ta pronto 

def send_mail_on_change(instance, book_title, availability, **kwargs):
    subject = f'Yay! The book "{book_title}" is {availability}'
    message = f'The availability of the book "{book_title}" is {availability}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['recipient_email@example.com']
    
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
    )