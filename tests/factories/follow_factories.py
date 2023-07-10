from followers.models import Follower


def create_follower(book, student) -> Follower:
    follow = Follower.objects.create(student=student, book_followed=book)
    return follow
