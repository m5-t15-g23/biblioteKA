from rest_framework import serializers

from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "student_id": instance.student.id,
            "student_username": instance.student.username,
            "book_followed_id": instance.book_followed.id,
            "book_followed_title": instance.book_followed.title,
        }

    class Meta:
        model = Follower
        fields = [
                "id",
                "student",
                "book_followed",
            ]
        read_only_fields = [
                "student",
                "book_followed",
            ]
