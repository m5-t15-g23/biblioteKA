from django.core.mail import send_mail
from django.conf import settings


def send_mail_on_change(book_title, availability, recipient_list):
    status_for_book = "avaliable" if availability is True else "unavaliable"
    interaction = ":)" if availability is True else ":("

    subject = (f"We have news! The book {book_title} is "
               f"{status_for_book} {interaction}")
    message = (f"The availability of the book "
               f"{book_title} is {status_for_book}")
    from_email = settings.EMAIL_HOST_USER

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False
    )
