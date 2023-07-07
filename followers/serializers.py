from rest_framework import serializers

from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
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
