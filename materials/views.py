from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.permissions import IsModeratorPermission, IsOwnerPermission
from materials.serializers import (CourseSerializer, LessonSerializer,
                                   SubscriptionSerializer)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModeratorPermission,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                ~IsModeratorPermission | IsOwnerPermission,
            )
        self.permission_classes = (
            IsAuthenticated,
            IsModeratorPermission | IsOwnerPermission,
        )
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        ~IsModeratorPermission,
    )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class LessonRetrieveApiView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModeratorPermission | IsOwnerPermission,
    )


class LessonListApiView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModeratorPermission)


class LessonUpdateApiView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        IsModeratorPermission | IsOwnerPermission,
    )


class LessonDestroyApiView(DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (
        IsAuthenticated,
        ~IsModeratorPermission | IsOwnerPermission,
    )


class SubscriptionViewSet(APIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, format=None):
        """Если подписка текущего пользователя на указанный курс существует, удалить. Иначе - создать."""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            course_item = serializer.validated_data.get("course")
            subs_item = Subscription.objects.filter(
                course=course_item, user=request.user
            )
            if subs_item.exists():
                message = "подписка удалена"
                subs_item.delete()
                status_code = status.HTTP_204_NO_CONTENT
            else:
                message = "подписка добавлена"
                status_code = status.HTTP_201_CREATED
                serializer.validated_data["user"] = request.user
                serializer.save()
            return Response(
                {"message": message, "data": serializer.data}, status=status_code
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
