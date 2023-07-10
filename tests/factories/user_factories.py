from rest_framework_simplejwt.tokens import AccessToken

from users.models import User


def create_colaborator_with_token(colaborator_data) -> tuple[
    User,
    AccessToken
]:
    colaborator = User.objects.create_superuser(**colaborator_data)
    token = str(AccessToken.for_user(colaborator))

    return colaborator, token


def create_student_with_token(student_data) -> tuple[User, AccessToken]:

    student = User.objects.create_superuser(**student_data)
    token = str(AccessToken.for_user(student))

    return student, token
