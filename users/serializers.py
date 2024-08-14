from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.serializers import CourseSerializer, LessonSerializer
from users.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    user_email = SerializerMethodField()

    @staticmethod
    def get_user_email(payment):
        return payment.user.email

    class Meta:
        model = Payment
        fields = ("course", "lesson", "user_email", "value", "method", "created_at")
