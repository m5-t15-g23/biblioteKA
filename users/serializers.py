from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> User:
        is_colaborator = validated_data.get("is_colaborator")

        user = (
            User.objects.create_superuser(**validated_data)
            if is_colaborator is True
            else User.objects.create_user(**validated_data)
        )

        return user

    def update(self, instance: User, validated_data: dict) -> User:
        new_password = validated_data.pop("password", None)
        user = instance

        if new_password:
            user.set_password(new_password)

        for key, value in validated_data.items():
            setattr(user, key, value)

        user.save()
        return user

    def to_representation(self, instance):
        if instance.is_colaborator is True:
            return {
                "id": instance.id,
                "email": instance.email,
                "username": instance.username,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "is_colaborator": instance.is_colaborator,
            }
        else:
            return {
                "id": instance.id,
                "email": instance.email,
                "username": instance.username,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "is_colaborator": instance.is_colaborator,
                "status_for_loan": instance.status_for_loan,
            }

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_colaborator",
            "status_for_loan"
        ]
        extra_kwargs = {
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="Email already in use"
                    )
                ]
            },
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="Username already in use"
                    )
                ]
            },
            "password": {"write_only": True}
        }


class StudentStatusSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "email": instance.email,
            "username": instance.username,
            "status_for_loan": instance.status_for_loan
        }

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_colaborator",
            "status_for_loan"
        ]
        read_only_fields = ["status_for_loan"]
