from django.core.mail import send_mail
from django.conf import settings


def send_mail_on_change(book_title, availability, recipient_list):
    subject = f'Yay! The book "{book_title}" is {availability}'
    message = f'The availability of the book "{book_title}" is {availability}'
    from_email = settings.EMAIL_HOST_USER
    # import ipdb
    # ipdb.set_trace()
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False
    )
