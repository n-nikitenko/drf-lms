from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    user_email = SerializerMethodField()

    @staticmethod
    def get_user_email(payment):
        return payment.user.email

    class Meta:
        model = Payment
        fields = ("course", "lesson", "user_email", "value", "method", "created_at")


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "session_id": {"read_only": True},
            "link": {"read_only": True},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "avatar", "phone", "is_active", "is_staff")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "avatar", "phone")
