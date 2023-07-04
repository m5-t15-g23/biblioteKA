from rest_framework import serializers
from .models import Follower

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = [
            "id",
            "user_id",
            "book_id",
        ]
        read_only_fields = [
            "user_id",
            "book_id",
        ]
