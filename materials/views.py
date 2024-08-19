from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.permissions import IsModeratorPermission, IsOwnerPermission
from materials.serializers import CourseSerializer, LessonSerializer


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
