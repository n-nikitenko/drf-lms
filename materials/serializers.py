from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_links


class LessonSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_links])
    description = serializers.CharField(validators=[validate_links], required=False)
    video_url = serializers.CharField(validators=[validate_links], required=False)

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    is_current_user_subscribed = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    title = serializers.CharField(validators=[validate_links])
    description = serializers.CharField(validators=[validate_links], required=False)

    @staticmethod
    def get_lessons_count(course):
        return course.lessons.count()

    def get_is_current_user_subscribed(self, course):

        request = self.context.get("request", None)
        if request:
            return request.user.subscriptions.filter(course=course).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        read_only_fields = ("user",)
        fields = "__all__"
