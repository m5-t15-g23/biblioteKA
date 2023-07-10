from copies.models import Copy


def create_copies(book) -> tuple[Copy]:
    [Copy.objects.create(book=book) for _ in range(3)]

    copies = Copy.objects.all()
    copy_one = copies[0]
    copy_two = copies[1]
    copy_three = copies[2]

    return copy_one, copy_two, copy_three
